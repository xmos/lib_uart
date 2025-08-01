// Copyright 2015-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.

#include <xs1.h>
#include <platform.h>
#include <stdlib.h>
#include <stdio.h>
#include "debug_print.h"
#include "xassert.h"
#include "uart.h"

#define BUFFER_SIZE 64
port p_uart    = on tile[0] : XS1_PORT_1A;
port sim_notif = on tile[0] : XS1_PORT_1B;

static void uart_test(client uart_rx_if i_uart_rx, 
                      client uart_tx_buffered_if i_uart_tx,
                      client uart_control_if i_control,
                      unsigned baud_rate)
{
  debug_printf("TEST CONFIG:{'baud rate':%d}\n", baud_rate);
  debug_printf("Performing combined test.\n");

  if (i_uart_tx.write(0x7f) != 0) printstrln("Write failed.");
  if (i_uart_tx.write(0x00) != 0) printstrln("Write failed.");
  if (i_uart_tx.write(0x2f) != 0) printstrln("Write failed.");
  if (i_uart_tx.write(0xff) != 0) printstrln("Write failed.");

  timer tmr;
  int t;
  tmr :> t;
  tmr when timerafter(t+((XS1_TIMER_HZ/baud_rate)*20*4)) :> void;
  i_control.set_mode(UART_RX_MODE);
  sim_notif <: 1;


  printf("0x%02x\n", i_uart_rx.wait_for_data_and_read());
  printf("0x%02x\n", i_uart_rx.wait_for_data_and_read());
  printf("0x%02x\n", i_uart_rx.wait_for_data_and_read());
  printf("0x%02x\n", i_uart_rx.wait_for_data_and_read());

  _Exit(0);
} 

int main() {
  interface uart_rx_if i_rx;
  interface uart_control_if i_control;
  interface uart_tx_buffered_if i_tx;

  par {
    on tile[0] : uart_half_duplex(i_tx, i_rx, i_control, NULL, BUFFER_SIZE, BUFFER_SIZE, BAUD, PARITY, 8, 1, p_uart);
    on tile[0] : uart_test(i_rx, i_tx, i_control, BAUD);
  }

  return 0;
}
