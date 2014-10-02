// Copyright (c) 2011, XMOS Ltd, All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>

#include "uart.h"
#include <xs1.h>
#include <stdio.h>
#include <stdlib.h>
#include <print.h>
#include <xscope.h>
#include "xassert.h"

enum uart_tx_state {
  WAITING_FOR_DATA,
  OUTPUTTING_DATA_BIT,
  OUTPUTTING_PARITY_BIT,
  OUTPUTTING_STOP_BIT
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

static inline void init_transmit(unsigned char buffer[buf_length], unsigned buf_length,
                                 int &rdptr, int &wrptr, out port p_txd,
                                 enum uart_tx_state &state,
                                 unsigned &bit_count, int &t,
                                 int bit_time,
                                 unsigned &byte)
{
  timer tmr;
  if (state != WAITING_FOR_DATA || rdptr == wrptr)
    return;
  byte = buffer[rdptr];

  // Trace the outgoing data
  xscope_char(UART_TX_VALUE, byte);

  rdptr++;
  if (rdptr == buf_length)
    rdptr = 0;
  state = OUTPUTTING_DATA_BIT;
  bit_count = 0;
  // Output start bit
  p_txd <: 0;
  tmr :> t;
  t += bit_time;
}

[[combinable]]
void uart_tx_buffered(server interface uart_tx_buffered_if i,
                      server interface uart_config_if ?config,
                      const static unsigned buf_length,
                      unsigned baud,
                      uart_parity_t parity,
                      unsigned bits_per_byte,
                      unsigned stop_bits,
                      port p_txd)
{
  unsigned char buffer[buf_length];
  int bit_time = XS1_TIMER_HZ / baud;
  enum uart_tx_state state = WAITING_FOR_DATA;
  unsigned byte;
  timer tmr;
  int rdptr = 0, wrptr = 0;
  unsigned bit_count, stop_bit_count;

  stop_bits += 1;

  int t;
  p_txd <: 1;
  while (1) {
    select {
    case (state != WAITING_FOR_DATA) => tmr  when timerafter(t) :> void:
      switch (state) {
      case OUTPUTTING_DATA_BIT:
        p_txd <: (byte >> bit_count);
        t += bit_time;
        bit_count++;
        if (bit_count == bits_per_byte) {
          if (parity != UART_PARITY_NONE) {
            state = OUTPUTTING_PARITY_BIT;
          } else {
            stop_bit_count = stop_bits;
            state = OUTPUTTING_STOP_BIT;
          }
        }
        break;
      case OUTPUTTING_PARITY_BIT:
        int val = parity32(byte, parity);
        p_txd <: val;
        t += bit_time;
        stop_bit_count = stop_bits;
        state = OUTPUTTING_STOP_BIT;
        break;
      case OUTPUTTING_STOP_BIT:
        p_txd <: 1;
        t += bit_time;
        stop_bit_count--;
        if (stop_bit_count == 0) {
          state = WAITING_FOR_DATA;
          init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                        bit_count, t, bit_time, byte);
        }
        break;
      }
    break;
    // Handle client interaction with the component
    case i._output_byte(unsigned char data) -> int buffer_was_full:
      if (buffer_full(rdptr, wrptr, buf_length)) {
        buffer_was_full = 1;
        return;
      }
      buffer_was_full = 0;
      buffer[wrptr] = data;
      wrptr++;
      if (wrptr == buf_length)
        wrptr = 0;

      init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                    bit_count, t, bit_time, byte);
      break;

    case i.get_available_buffer_size(void) -> size_t available:
      int size = rdptr - wrptr;
      if (size < 0)
        size += buf_length;
      available = size;
      break;

    case !isnull(config) => config.set_baud_rate(unsigned baud_rate):
      bit_time = XS1_TIMER_HZ / baud_rate;
      state = WAITING_FOR_DATA;
      init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                    bit_count, t, bit_time, byte);
      break;
    case !isnull(config) => config.set_parity(uart_parity_t new_parity):
      parity = new_parity;
      state = WAITING_FOR_DATA;
      init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                    bit_count, t, bit_time, byte);

      break;
    case !isnull(config) => config.set_stop_bits(unsigned new_stop_bits):
      stop_bits = new_stop_bits + 1;
      state = WAITING_FOR_DATA;
      init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                    bit_count, t, bit_time, byte);
      break;
    case !isnull(config) => config.set_bits_per_byte(unsigned bpb):
      bits_per_byte = bpb;
      state = WAITING_FOR_DATA;
      init_transmit(buffer, buf_length, rdptr, wrptr, p_txd, state,
                    bit_count, t, bit_time, byte);
      break;
    }
  }
}
