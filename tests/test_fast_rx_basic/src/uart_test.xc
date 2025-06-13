// Copyright (c) 2015-2016, XMOS Ltd, All rights reserved

#include <xs1.h>
#include <platform.h>
#include <stdlib.h>
#include <stdio.h>
#include "debug_print.h"
#include "xassert.h"
#include "uart.h"

#define BITTIME(x) (XS1_TIMER_HZ / (x))

port p_rx = on tile[0] : XS1_PORT_1A;
out port p_tx = on tile[0] : XS1_PORT_1B;

static void uart_test(streaming chanend stream, unsigned baud_rate)
{
  debug_printf("TEST CONFIG:{'baud rate':%d}\n", baud_rate);
  debug_printf("Performing rx test.\n");
  // Output on TX so the test framework knows the client is up
  p_tx <: 1;
  int t;
  timer tmr;
  tmr :> t;
  uint8_t data;

  for(int i = 0; i < 4;){
    select 
    {
      // Default timeout of 20 bit times
      case tmr when timerafter(t + BITTIME(baud_rate)*40) :> void:
        _Exit(0);
        return;

      case uart_rx_streaming_read_byte(stream, data):
        printf("0x%02x\n", data);
        i++;
        tmr :> t;
        break;
    }
  }

  _Exit(0);
}

int main() {
  streaming chan stream;
  par {
    on tile[0] : uart_rx_streaming(p_rx, stream, BITTIME(BAUD));
    on tile[0] : {
        uart_test(stream, BAUD);
     }
   }
   return 0;
 }


