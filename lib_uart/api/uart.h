// Copyright (c) 2011, XMOS Ltd, All rights reserved
// This software is freely distributable under a derivative of the
// University of Illinois/NCSA Open Source License posted in
// LICENSE.txt and at <http://github.xcore.com/>

#ifndef _uart_h_
#define _uart_h_
#include <stdint.h>
#include <stddef.h>
#include <xs1.h>

// This component will only work in xC.
#ifdef __XC__

/** Type representing the parity of a UART */
typedef enum uart_parity_t {
  UART_PARITY_EVEN = 0, ///< Even parity
  UART_PARITY_ODD = 1,  ///< Odd parity
  UART_PARITY_NONE      ///< No parity
} uart_parity_t;

/** UART configuration interface.
 *
 *  This interfaces enables dynamic reconfiguration of a UART.
 */
typedef interface uart_config_if {
  /** Set the baud rate of a UART.
   */
  void set_baud_rate(unsigned baud_rate);

  /** Set the parity of a UART.
   */
  void set_parity(enum uart_parity_t parity);

  /** Set number of stop bits used by a UART.
   */
  void set_stop_bits(unsigned stop_bits);

  /** Set number of bits per byte used by a UART.
   */
  void set_bits_per_byte(unsigned bpb);
} uart_config_if;


/** UART RX interface.
 *
 *   This interface provides clients access to buffer uart receive
 *   functionality.
 */
typedef interface uart_rx_if {
  /** Get a byte from the receive buffer.
   *
   *   This function should be called after receiving a data_ready()
   *   notification. If these is no data in the buffer (for example, this
   *   function is called before receiving a notification) then the return
   *   value is undefined.
   */
  [[clears_notification]] uint8_t _input_byte(void);

  /** Notification that data is in the receive buffer.
   *
   *   This notification function can be selected on by the client and
   *   will event when the is data in the receive buffer. After this
   *   notification the client should call the input_byte() function.
   */
  [[notification]] slave void data_ready(void);

  /** Returns whether there is data in the buffer.
   */
  int has_data();
} uart_rx_if;


extends client interface uart_rx_if : {

  /** Get a byte from the receive buffer.
   *
   *   This function will wait until there is data in the receive buffer
   *   of the uart and then fetch that data. On getting the data, it
   *   will clear the notification flag on the interface.
   */
  inline uint8_t input_byte(client uart_rx_if i) {
    if (!i.has_data()) {
      select {
      case i.data_ready():
        break;
      }
    }
    return i._input_byte();
  }
}

/** UART RX component.
 *
 *    This function runs a uart receiver.
 *    Bytes received by the server are buffered in the provided buffer array.
 *    When the buffer is full further incoming bytes of data will be dropped.
 *    The function never returns and will run the server indefinitely.
 *
 *    \param i             the interface connection to the server
 *    \param buffer_size   the size of the buffer
 *    \param baud          the initial baud rate
 *    \param parity        the intiial parity setting
 *    \param bits_per_byte the initial number of bits per byte
 *    \param stop_bits     the intiial number of stop bits
 *    \param p_rxd         the 1 bit port to input data on
 */
[[combinable]]
void uart_rx(server interface uart_rx_if i,
             server interface uart_config_if ?i_config,
             const static unsigned buffer_size,
             unsigned baud,
             enum uart_parity_t parity,
             unsigned bits_per_byte,
             unsigned stop_bits,
             port p_rxd);

/** Fast/Streaming UART RX server function.
 *
 * This function implements a fast UART. It needs an unbuffered 1-bit
 * port, a streaming channel end, and a number of port-clocks to wait
 * between bits. It receives a start bit, 8 bits, and a stop bit, and
 * transmits the 8 bits over the streaming channel end as a single token.
 * On a 62.5 MIPS thread this function should be able to keep up with a 10
 * MBit UART sustained (provided that the streaming channel can keep up
 * with it too).
 *
 * This function does not return.
 *
 * \param p      input port, 1 bit port on which data comes in
 *
 * \param c      output streaming channel - read bytes of this channel (or
 *               words if you want to read 4 bytes at a time)
 *
 * \param clocks number of clock ticks between bits. This number depends on the clock
 *               that you have attached to port p; assuming it is the standard 100 Mhz
 *               reference clock then clocks should be at least 10.
 */
void uart_rx_streaming(in port p, streaming chanend c, int clocks);

/** Receive a byte from a streaming UART receiver.
 *
 *  This function receives a byte from the fast/streaming UART component. It is
 *  "select handler" so can be used within a select e.g.
 *
    \verbatim
     uint8_t byte;
     size_t index;
     select {
       case uart_rx_streaming_receive_byte(c, byte):
            // use sample and index here...
            ...
            break;
     ...
    \endverbatim
 *
 *   The case in this select will fire when the UART component has data ready.
 *
 *   \param c       chanend connected to the S/PDIF receiver component
 *   \param data    This reference parameter gets set with the incoming
 *                  data
 */
#pragma select handler
void uart_rx_streaming_receive_byte(streaming chanend c, uint8_t &data);

/* TX */
typedef interface uart_tx_if {
  void output_byte(uint8_t data);
} uart_tx_if;

typedef interface uart_tx_buffered_if {

  size_t get_available_buffer_size(void);

  [[notification]]
  slave void ready_to_transmit(void);

  [[clears_notification]]
  int _output_byte(uint8_t data);
} uart_tx_buffered_if;

[[distributable]]
void uart_tx(server interface uart_tx_if i,
             server interface uart_config_if ?i_config,
             unsigned baud,
             uart_parity_t parity,
             unsigned bits_per_byte,
             unsigned stop_bits,
             port p_txd);


[[combinable]]
void uart_tx_buffered(server interface uart_tx_buffered_if i,
                      server interface uart_config_if ?config,
                      const static unsigned buf_length,
                      unsigned baud,
                      uart_parity_t parity,
                      unsigned bits_per_byte,
                      unsigned stop_bits,
                      port p_txd);

/* HALF DUPLEX */

// TODO

/* MULTI UARTS */

typedef interface multi_uart_rx_if {

  [[clears_notification]]
  uint8_t get_data(size_t &index, int &is_valid);

  [[notification]] slave void data_ready(void);

} multi_uart_rx_if;

void multi_uart_rx(server interface multi_uart_rx_if i,
                   port p, clock clk,
                   uart_parity_t parity, unsigned bits_per_byte,
                   unsigned stop_bits);

#if 0
#define multi_uart_rx(i, p, clk, baud, parity, bits, stop_bits) \
  {interface multi_uart_rx_buf_if i_buf; \
    par { \
      multi_uart_rx_buffer(i, i_buf); \
      multi_uart_rx_pins(i_buf, p, clk, baud, parity, bits, stop_bits); \
    } \
  }
#endif

typedef interface multi_uart_tx_if {
  [[notification]] slave void tx_slot_available(void);

  [[clears_notification]]
  int is_tx_slot_free(size_t index);

  [[clears_notification]]
  void output_byte(size_t index, uint8_t data);

} multi_uart_tx_if;


void multi_uart_tx(server interface multi_uart_tx_if i,
                   port p, clock clk,
                   uart_parity_t parity, unsigned bits_per_byte,
                   unsigned stop_bits);


#endif // __XC__

#endif /* _uart_h_ */
