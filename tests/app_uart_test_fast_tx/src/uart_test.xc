// Copyright (c) 2015-2016, XMOS Ltd, All rights reserved

#include <xs1.h>
#include <platform.h>
#include <stdlib.h>
#include "debug_print.h"
#include "xassert.h"
#include "uart.h"

#define BITTIME(x) (XS1_TIMER_HZ / (x))

static void uart_test(streaming chanend stream, unsigned baud_rate)
{
  debug_printf("TEST CONFIG:{'baud rate':%d}\n", baud_rate);
  debug_printf("Performing tx test.\n");

  for(int i = 0; i < 128; i++)
    uart_tx_streaming_write_byte(stream, i);

  timer tmr;
  int t;
  tmr :> t;
  tmr when timerafter(t+(1000000/baud_rate)*10000+50000) :> void;
  _Exit(0);
}

port p_rx = on tile[0] : XS1_PORT_1A;
out port p_tx = on tile[0] : XS1_PORT_1B;


#define BUFFER_SIZE 64
int main() {
  streaming chan stream;
  par {
    on tile[0] : uart_tx_streaming(p_tx, stream, BITTIME(BAUD));
    on tile[0] : {
        uart_test(stream, BAUD);
     }
   }
   return 0;
 }


