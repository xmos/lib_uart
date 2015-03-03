// Copyright (c) 2011, XMOS Ltd., All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>
#include <xs1.h>
#include <platform.h>
#include <uart.h>
#include <debug_print.h>

// These ports are configures assuming the multi-UART slice is
// connected to the SQUARE slot. For other slots the ports will
// need to be changed.
in  buffered port:32 p_uart_rx = XS1_PORT_8A;
out buffered port:8 p_uart_tx  = XS1_PORT_8B;
in  port p_uart_clk            = XS1_PORT_1F;

clock clk_uart = XS1_CLKBLK_4;

void loopback(streaming chanend c_rx, client multi_uart_rx_if i_rx,
              chanend c_tx, client multi_uart_tx_if i_tx)
{
  size_t slot;
  i_rx.init(c_rx);
  i_tx.init(c_tx);
  while (1) {
    select {
    case multi_uart_data_ready(c_rx, slot):
      uint8_t data;
      if (i_rx.read(slot, data) == UART_RX_VALID_DATA) {
        if (i_tx.is_slot_free(slot)) {
          i_tx.write(slot, data);
        }
        else {
          debug_printf("Warning: TX buffer overflow on channel %d\n",
                       slot);
        }
      }
      break;
    }
  }
}

int main(void)
{
  interface multi_uart_rx_if i_rx;
  streaming chan c_rx;
  chan c_tx;
  interface multi_uart_tx_if i_tx;
  configure_clock_src(clk_uart, p_uart_clk);
  start_clock(clk_uart);
  par {
    multi_uart_rx(c_rx, i_rx, p_uart_rx, 8,
                  1843200,
                  115200, UART_PARITY_NONE, 8, 1);
    multi_uart_tx(c_tx, i_tx, p_uart_tx, 8,
                  1843200,
                  115200, UART_PARITY_NONE, 8, 1);
    loopback(c_rx, i_rx, c_tx, i_tx);
  }
  return 0;
}
