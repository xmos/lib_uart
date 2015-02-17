// Copyright (c) 2015, XMOS Ltd, All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>

#include <xclib.h>
#include <xs1.h>

// Assertions Header
#include "xassert.h"

// UART API Header
#include "uart.h"

static inline void wait_when_pins_eq(port pin, char value);
static inline void event_when_pins_eq(port pin, char value);

// TODO: Move these into header
unsigned baud = 115200;
unsigned stop_bits = 1;
unsigned bits_per_byte = 8;
enum uart_parity_t parity = UART_PARITY_NONE;
enum uart_tx_state {
  WAITING_FOR_DATA,
  OUTPUTTING_DATA_BIT,
  OUTPUTTING_PARITY_BIT,
  OUTPUTTING_STOP_BIT,
  TX_INACTIVE
};
enum uart_rx_state {
  WAITING_FOR_INPUT,
  WAITING_FOR_HIGH,
  TESTING_START_BIT,
  INPUTTING_DATA_BIT,
  INPUTTING_PARITY_BIT,
  INPUTTING_STOP_BIT,
  RX_INACTIVE
};



static inline int parity32(unsigned x, uart_parity_t parity)
{
  // To compute even / odd parity the checksum should be initialised
  // to 0 / 1 respectively. The values of the art_tx_parity have been
  // chosen so the parity can be used to initialise the checksum
  // directly.
  assert(UART_PARITY_EVEN == 0);
  assert(UART_PARITY_ODD == 1);
  crc32(x, parity, 1);
  return (x & 1);
}

static inline int buffer_full(int rdptr, int wrptr, int buf_length)
{
    wrptr++;
    if (wrptr == buf_length)
        wrptr = 0;
    return (wrptr == rdptr);
}

static inline void init_transmit(unsigned char buffer[buf_length],
                                 unsigned buf_length,
                                 unsigned &rdptr, unsigned &wrptr,
                                 out port p, enum uart_tx_state &state,
                                 unsigned &bit_count, int &t, int bit_time,
                                 unsigned &byte)
{
    timer tmr;
    if (state != WAITING_FOR_DATA || rdptr == wrptr)
    return;
        byte = buffer[rdptr];

    // Trace the outgoing data
//    xscope_char(UART_TX_VALUE, byte);

    rdptr++;
    if (rdptr == buf_length)
    rdptr = 0;
    state = OUTPUTTING_DATA_BIT;
    bit_count = 0;
    // Output start bit
    p <: 0;
    tmr :> t;
    t += bit_time;
}


static inline int add_to_buffer(unsigned char buffer[n], unsigned n,
                                unsigned &rdptr, unsigned &wrptr,
                                unsigned char data)
{
  int new_wrptr = wrptr + 1;

  if (new_wrptr >= n)
    new_wrptr = 0;

  if (new_wrptr == rdptr) {
    // buffer full
    return 0;
  }

  // Output tracing information of the values entering the buffer
//  xscope_char(UART_RX_VALUE, data);

  buffer[wrptr] = data;
  wrptr = new_wrptr;
  return 1;
}



void uart_half_duplex(server interface uart_tx_buffered_if i_tx,
                      server interface uart_rx_if i_rx,
                      server interface uart_control_if i_control,
                      server interface uart_config_if ?i_config,
                      const static unsigned tx_buf_length,
                      const static unsigned rx_buf_length,
                      port p_uart)
{
    // Initialise the server.
    unsigned char rx_buffer[rx_buf_length], tx_buffer[tx_buf_length];
    int bit_time = XS1_TIMER_HZ / baud;

    // State machine intitial state.
    enum uart_tx_state tx_state  = WAITING_FOR_DATA;
    enum uart_rx_state rx_state  = RX_INACTIVE;
    uart_half_duplex_mode_t mode = UART_TX_MODE;

    // Locals
    char switch_mode = 0;
    unsigned byte, data = 0, data_bit_count = 0;
    timer tmr;
    int t;

    unsigned tx_rdptr = 0, tx_wrptr = 0;
    unsigned rx_rdptr = 0, rx_wrptr = 0;
    unsigned bit_count, stop_bit_count;

    // State machine
    while(1)
    {
        switch(mode) {
            // tx mode
            case UART_TX_MODE:
            {
                select {
                    // If we're not in the waiting state, go through state
                    //  machine once per bit time
                    case (tx_state != WAITING_FOR_DATA) => tmr  when timerafter(t) :> void:
                    {
                        switch(tx_state)
                        {
                            case OUTPUTTING_DATA_BIT:
                            {
                                p_uart <: (byte >> bit_count);
                                t += bit_time;
                                bit_count++;
                                if (bit_count == bits_per_byte)
                                {
                                    if (parity != UART_PARITY_NONE)
                                    {
                                        tx_state = OUTPUTTING_PARITY_BIT;
                                    }
                                    else
                                    {
                                        stop_bit_count = stop_bits;
                                        tx_state = OUTPUTTING_STOP_BIT;
                                    }
                                }
                                break;
                            }

                            case OUTPUTTING_PARITY_BIT:
                            {
                                int val = parity32(byte, parity);
                                p_uart <: val;
                                t += bit_time;
                                stop_bit_count = stop_bits;
                                tx_state = OUTPUTTING_STOP_BIT;
                                break;
                            }

                            case OUTPUTTING_STOP_BIT:
                            {
                                p_uart <: 1;
                                t += bit_time;
                                stop_bit_count--;
                                if (stop_bit_count == 0) {
                                    tx_state = WAITING_FOR_DATA;

                                    // If a mode switch has been indicated...
                                    if(switch_mode)
                                    {
                                        mode = UART_RX_MODE;
                                        tx_state = TX_INACTIVE;
                                        rx_state = WAITING_FOR_INPUT;
                                        switch_mode = 0;
                                        break;
                                    }
                                    init_transmit(tx_buffer, tx_buf_length,
                                        tx_rdptr, tx_wrptr, p_uart, tx_state,
                                        bit_count, t, bit_time, byte);
                                }
                                break;
                            }
                        }
                        break;
                    }

                    case i_tx.write(unsigned char data) -> int buffer_was_full:
                    {
                        if (buffer_full(tx_rdptr, tx_wrptr, tx_buf_length))
                        {
                          buffer_was_full = 1;
                          return;
                        }
                        buffer_was_full = 0;
                        tx_buffer[tx_wrptr] = data;
                        tx_wrptr++;
                        if (tx_wrptr == tx_buf_length)
                          tx_wrptr = 0;

                        init_transmit(tx_buffer, tx_buf_length, tx_rdptr,
                                tx_wrptr, p_uart, tx_state, bit_count, t,
                                bit_time, byte);
                        break;
                    }

                    case i_tx.get_available_buffer_size(void) -> size_t available:
                    {
                        int size = tx_rdptr - tx_wrptr;
                        if (size <= 0)
                            size += tx_buf_length - 1;
                        available = size;
                        break;
                    }

                    case i_control.set_mode(uart_half_duplex_mode_t n_mode):
                    {
                        // If this is actually a mode change...
                        if(mode != n_mode)
                        {
                            // If we're not in an idle state, set a flag for the
                            //  mode the be change after outputting the current
                            //  byte
                            if(tx_state != WAITING_FOR_DATA)
                            {
                                switch_mode = 1;
                            }
                            else // Otherwise, just change mode
                            {
                                mode = UART_RX_MODE;
                                tx_state = TX_INACTIVE;
                                rx_state = WAITING_FOR_INPUT;
                                switch_mode = 0;
                            }
                        }
                        break;
                    }
                }
                break;
            }

            // rx mode
            case UART_RX_MODE:
            {
                select
                {
                    case (rx_state == WAITING_FOR_HIGH || rx_state == WAITING_FOR_INPUT) => p_uart when pinseq(0) :> void:
                    {
                        tmr :> t;
                        switch (rx_state) {
                            case WAITING_FOR_HIGH:
                            {
                                p_uart when pinseq(0) :> void;
                                rx_state = WAITING_FOR_INPUT;
                                break;
                            }
                            case WAITING_FOR_INPUT:
                            {
                                t += bit_time/2;
                                rx_state = TESTING_START_BIT;
                                break;
                            }
                        }
                        break;
                    }

                    case (rx_state != WAITING_FOR_INPUT && rx_state != WAITING_FOR_HIGH) => tmr when timerafter(t) :> void:
                    {
                        switch (rx_state) {
                            case TESTING_START_BIT:
                            {
                                // We should now be half way through the start bit
                                // Test it is not a glitch
                                int level_test;
                                p_uart :> level_test;
                                if (level_test == 0)
                                {
                                    data_bit_count = 0;
                                    t += bit_time;
                                    data = 0;
                                    rx_state = INPUTTING_DATA_BIT;
                                }
                                else
                                {
                                    event_when_pins_eq(p_uart, 1);
                                    rx_state = WAITING_FOR_HIGH;
                                }
                                break;
                            }

                            case INPUTTING_DATA_BIT:
                            {
                                int bit;
                                p_uart :> bit;
                                data = data << 1 | bit;
                                data_bit_count++;
                                t += bit_time;
                                if (data_bit_count == bits_per_byte) {
                                    data = bitrev(data) >> (CHAR_BIT * sizeof(unsigned) - bits_per_byte);
                                    if (parity != UART_PARITY_NONE)
                                    {
                                        rx_state = INPUTTING_PARITY_BIT;
                                    }
                                    else
                                    {
                                        if (add_to_buffer(rx_buffer, rx_buf_length, rx_rdptr, rx_wrptr, data))
                                            i_rx.data_ready();
                                        if (stop_bits != 0)
                                        {
                                            stop_bit_count = stop_bits;
                                            rx_state = INPUTTING_STOP_BIT;
                                        }
                                        else
                                        {
                                            rx_state = WAITING_FOR_INPUT;
                                            event_when_pins_eq(p_uart, 0);
                                        }
                                    }
                                }
                                break;
                            }

                            case INPUTTING_PARITY_BIT:
                            {
                                int bit;
                                p_uart :> bit;
                                if (bit == parity32(data, parity))
                                {
                                    if (add_to_buffer(rx_buffer, rx_buf_length, rx_rdptr, rx_wrptr, data))
                                        i_rx.data_ready();
                                    if (stop_bits != 0)
                                    {
                                        stop_bit_count = stop_bits;
                                        rx_state = INPUTTING_STOP_BIT;
                                    }
                                    else
                                    {
                                        event_when_pins_eq(p_uart, 0);
                                        rx_state = WAITING_FOR_INPUT;
                                    }
                                }
                                else {
                                    event_when_pins_eq(p_uart, 1);
                                    rx_state = WAITING_FOR_HIGH;
                                }
                                t += bit_time;
                                break;
                            }

                            case INPUTTING_STOP_BIT:
                            {
                                int level_test;
                                p_uart :> level_test;
                                if (level_test == 0) {
                                    event_when_pins_eq(p_uart, 1);
                                    rx_state = WAITING_FOR_HIGH;
                                }
                                stop_bit_count--;
                                t += bit_time;
                                if (stop_bit_count == 0) {
                                    event_when_pins_eq(p_uart, 0);
                                    rx_state = WAITING_FOR_INPUT;
                                }
                                break;
                            }
                        }
                        break;
                    }

                    case i_rx.read() -> unsigned char data:
                    {
                        if (rx_rdptr == rx_wrptr)
                            break;
                        data = rx_buffer[rx_rdptr];
                        rx_rdptr++;
                        if (rx_rdptr == rx_buf_length)
                            rx_rdptr = 0;
                        if (rx_rdptr != rx_wrptr)
                            i_rx.data_ready();
                        break;
                    }

                    case i_rx.has_data() -> int res:
                    {
                        res = (rx_rdptr != rx_wrptr);
                        break;
                    }
                }
                break;
            }
        }
    }
}

static inline void event_when_pins_eq(port pin, char value)
{
    // TODO: what do?
    return;
}

static inline void wait_when_pins_eq(port pin, char value)
{
    char current;
    do {
        pin :> current;
    } while (current != value);
}
