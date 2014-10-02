// Copyright (c) 2011, XMOS Ltd, All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>
#include <xs1.h>
#include <platform.h>
#include <print.h>
#include <uart.h>
#include <stddef.h>

// Port declarations
port p_uart_rx = on tile[0] : XS1_PORT_1A;
port p_uart_tx = on tile[0] : XS1_PORT_1B;

#define BAUD_RATE 115200
#define RX_BUFFER_SIZE 64

/* This function performs the main "application" that outputs and reads
   some bytes over UART */
void app(client uart_tx_if uart_tx, client uart_rx_if uart_rx)
{
  uint8_t byte;
  printstrln("Test started");
  byte = 0;
  for (size_t i = 0; i < 20; i++) {
      printstr("Echo 10 bytes... ");
      for(size_t j = 0; j < 10; j++) {
          uart_tx.output_byte(byte);
          byte = byte + 1;
      }
      for(size_t j = 0; j < 10; j++) {
          printhex(uart_rx.input_byte());
      }
  }
  printstrln(". Done.");
}

void test() { while (1);}

/* "main" function that sets up two uarts and the application */
int main() {
  interface uart_rx_if i_rx;
  interface uart_tx_if i_tx;
  par {
    on tile[0]: test();
    on tile[0]: uart_tx(i_tx, null,
                        BAUD_RATE, UART_PARITY_NONE, 8, 1,
                        p_uart_tx);
    on tile[0]: uart_rx(i_rx, null, RX_BUFFER_SIZE,
                        BAUD_RATE, UART_PARITY_NONE, 8, 1,
                        p_uart_rx);
    on tile[0]: app(i_tx, i_rx);
  }
  return 0;
}
