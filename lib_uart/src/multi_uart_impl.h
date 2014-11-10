#ifndef __MULTI_UART_IMPL_H__
#define __MULTI_UART_IMPL_H__

#define multi_uart_rx(i, p, clk, baud, parity, bits, stop_bits) \
  {interface multi_uart_rx_buf_if i_buf; \
    par { \
      multi_uart_rx_buffer(i, i_buf); \
      multi_uart_rx_pins(i_buf, p, clk, baud, parity, bits, stop_bits); \
    } \
  }


#endif // __MULTI_UART_IMPL_H__
