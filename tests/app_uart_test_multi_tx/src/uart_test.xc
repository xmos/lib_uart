// Copyright (c) 2011, XMOS Ltd., All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>
#include <xs1.h>
#include <platform.h>
#include <stdlib.h>
#include <uart.h>

#include "debug_print.h"


in  buffered port:32 p_uart_rx = XS1_PORT_8A;
out buffered port:8 p_uart_tx  = XS1_PORT_8B;
in  port p_uart_clk            = XS1_PORT_1F;

clock clk_uart = XS1_CLKBLK_4;

void test(chanend c_tx, client multi_uart_tx_if i_tx)
{
  debug_printf("TEST CONFIG:{'baud rate':%d}\n", BAUD);
  debug_printf("Performing multi_uart tx test.\n");
  i_tx.init(c_tx);

  i_tx.write(1, 0X7f);
  i_tx.write(1, 0x00);
  i_tx.write(1, 0x2f);
  i_tx.write(1, 0xff);

  timer tmr;
  int t;
  tmr :> t;
  tmr when timerafter(t+(4*(XS1_TIMER_HZ/BAUD)*20)) :> void;
  _Exit(0);
}

int main(void)
{
  chan c_tx;
  interface multi_uart_tx_if i_tx;

  configure_clock_src(clk_uart, p_uart_clk);
  configure_out_port(p_uart_tx, clk_uart, 0);

  start_clock(clk_uart);

  par {
    multi_uart_tx(c_tx, i_tx, p_uart_tx, 8, 230400, BAUD, UART_PARITY_NONE, 8, 1);
    test(c_tx, i_tx);
  }
  return 0;
}