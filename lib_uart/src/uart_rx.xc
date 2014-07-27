// Copyright (c) 2011, XMOS Ltd, All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>

#include "uart.h"
#include "xassert.h"
#include <xs1.h>
#include <stdio.h>
#include <print.h>
#include <xscope.h>

#ifdef __uart_rx_conf_h_exists__
#include "uart_rx_conf.h"
#endif

enum uart_rx_state {
  WAITING_FOR_INPUT,
  WAITING_FOR_HIGH,
  TESTING_START_BIT,
  INPUTTING_DATA_BIT,
  INPUTTING_PARITY_BIT,
  INPUTTING_STOP_BIT,
};

static inline int parity32(unsigned x, enum uart_parity_t parity)
{
  // To compute even / odd parity the checksum should be initialised
  // to 0 / 1 respectively. The values of the uart_parity_t have been
  // chosen so the parity can be used to initialise the checksum
  // directly.
  assert(UART_PARITY_EVEN == 0);
  assert(UART_PARITY_ODD == 1);
  crc32(x, parity, 1);
  return (x & 1);
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
  xscope_char(UART_RX_VALUE, data);

  buffer[wrptr] = data;
  wrptr = new_wrptr;
  return 1;
}



void uart_rx(server interface uart_rx_if c,
             server interface uart_config_if ?config,
             const static unsigned n,
             unsigned baud,
             enum uart_parity_t parity,
             unsigned bits_per_byte,
             unsigned stop_bits,
             port p_rxd0)
{
  unsigned char buffer[n];
  int data_bit_count;
  timer tmr;
  int data_trigger = 1;
  enum uart_rx_state state = WAITING_FOR_HIGH;
  int t;
  unsigned bit_time = (XS1_TIMER_HZ / baud);
  int stop_bit_count;
  unsigned data;
  unsigned rdptr = 0, wrptr = 0;
  port * movable pp_rxd0 = &p_rxd0;
  in buffered port:1 * movable pp_rxd = reconfigure_port(move(pp_rxd0),
                                                         in buffered port:1);
  in buffered port:1 &p_rxd = *pp_rxd;
  while (1) {
    #pragma ordered
    select {
    // The following cases implement the uart state machine
    case (state == WAITING_FOR_INPUT || state == WAITING_FOR_HIGH) =>
         p_rxd when pinseq(data_trigger) :> void:
      tmr :> t;
      switch (state) {
      case WAITING_FOR_HIGH:
        data_trigger = 0;
        state = WAITING_FOR_INPUT;
        break;
      case WAITING_FOR_INPUT:
        t += bit_time/2;
        state = TESTING_START_BIT;
      break;
      }
      break;
    case (state != WAITING_FOR_INPUT && state != WAITING_FOR_HIGH) =>
      tmr when timerafter(t) :> void:
      switch (state) {
      case TESTING_START_BIT:
        // We should now be half way through the start bit
        // Test it is not a glitch
        int level_test;
        p_rxd :> level_test;
        if (level_test == 0) {
          data_bit_count = 0;
          t += bit_time;
          data = 0;
          state = INPUTTING_DATA_BIT;
        }
        else {
          data_trigger = 1;
          state = WAITING_FOR_HIGH;
        }
        break;
      case INPUTTING_DATA_BIT:
        p_rxd :> >> data;
        data_bit_count++;
        t += bit_time;
        if (data_bit_count == bits_per_byte) {
          data >>= CHAR_BIT * sizeof(data) - bits_per_byte;
          if (parity != UART_PARITY_NONE) {
            state = INPUTTING_PARITY_BIT;
          } else {
            if (add_to_buffer(buffer, n, rdptr, wrptr, data))
              c.data_ready();
            if (stop_bits != 0) {
              stop_bit_count = stop_bits;
              state = INPUTTING_STOP_BIT;
            }
            else {
              state = WAITING_FOR_INPUT;
              data_trigger = 0;
            }
          }
        }
        break;
      case INPUTTING_PARITY_BIT:
        int bit;
        p_rxd :> bit;
        if (bit == parity32(data, parity)) {
          if (add_to_buffer(buffer, n, rdptr, wrptr, data))
            c.data_ready();
          if (stop_bits != 0) {
            stop_bit_count = stop_bits;
            state = INPUTTING_STOP_BIT;
          }
          else {
            data_trigger = 0;
            state = WAITING_FOR_INPUT;
          }
        }
        else {
          data_trigger = 1;
          state = WAITING_FOR_HIGH;
        }
        t += bit_time;
        break;
      case INPUTTING_STOP_BIT:
        int level_test;
        p_rxd :> level_test;
        if (level_test == 0) {
          data_trigger = 1;
          state = WAITING_FOR_HIGH;
        }
        stop_bit_count--;
        t += bit_time;
        if (stop_bit_count == 0) {
          data_trigger = 0;
          state = WAITING_FOR_INPUT;
        }
        break;
      }
      break;
    case c._input_byte() -> unsigned char data:
      if (rdptr == wrptr)
        break;
      data = buffer[rdptr];
      rdptr++;
      if (rdptr == n)
        rdptr = 0;
      if (rdptr != wrptr)
        c.data_ready();
      break;
    case c.has_data() -> int res:
      res = (rdptr != wrptr);
      break;
    // Handle client interaction with the component
    case !isnull(config) => config.set_baud_rate(unsigned baud_rate):
      bit_time = XS1_TIMER_HZ / baud_rate;
      data_trigger = 1;
      state = WAITING_FOR_HIGH;
      break;
    case !isnull(config) => config.set_parity(enum uart_parity_t new_parity):
      parity = new_parity;
      data_trigger = 1;
      state = WAITING_FOR_HIGH;
      break;
    case !isnull(config) => config.set_stop_bits(unsigned new_stop_bits):
      stop_bits = new_stop_bits;
      data_trigger = 1;
      state = WAITING_FOR_HIGH;
      break;
    case !isnull(config) => config.set_bits_per_byte(unsigned bpb):
      bits_per_byte = bpb;
      data_trigger = 1;
      state = WAITING_FOR_HIGH;
      break;
    }
  }
}

extends client interface uart_rx_if : {
  extern inline unsigned char input_byte(client uart_rx_if i);
}
