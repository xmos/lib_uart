// Copyright 2014-2025 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.

#include <xs1.h>
#include <xclib.h>
#include <uart.h>

void uart_rx_fast_init(in port p, const clock clkblk){
    //set port into clocked mode
	configure_in_port_no_ready(p, clkblk);
	//clear the receive buffer
    clearbuf(p);
}

void uart_rx_streaming_read_byte(streaming chanend c, uint8_t &byte)
{
  c :> byte;
}

void uart_rx_streaming(in port pIn, streaming chanend cOut, int clocks) {
    int dt2 = (clocks * 3)>>1; //one and a half bit times
    int dt = clocks;
    int t;
    unsigned int data = 0;
    while (1) {
        pIn when pinseq(0) :> int _ @ t; //wait until falling edge of start bit
        t += dt2;
#pragma loop unroll(8)
        for(int i = 0; i < 8; i++) {
            pIn @ t :> >> data; //sample value when port timer = t
            					//inlcudes post right shift
            t += dt;
        }
        data >>= 24;			//shift into MSB
        cOut <: (unsigned char) data; //send to client
        pIn @ t :> int _;
        data = 0;
    }
}

