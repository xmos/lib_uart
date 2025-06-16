UART library
============

Summary
-------

A software defined, industry-standard, UART (Universal Asynchronous
Receiver/Transmitter) library
that allows you to control a UART serial connection via the
xCORE GPIO ports. This library is controlled
via C using the XMOS multicore extensions.

Features
........

 * UART receive and transmit
 * Supports speeds up to 10MBit/s
 * Half-duplex mode (applicable to RS485)
 * Efficient multi-uart mode for implementing multiple connections


Resource Usage
..............

.. list-table::
  :widths: 20 20 25 25 6 6
  :header-rows: 1

  * - configuration
    - globals
    - locals
    - function
    - pins
    - ports

  * - Standard TX
    - none
    - output_gpio_if i_gpio_tx; interface uart_tx_if i_tx;
    - uart_tx()
    - 1
    - 1

  * - Standard TX (buffered)
    - none
    - output_gpio_if i_gpio_tx; interface uart_tx_buffered_if i_tx;
    - uart_tx_buffered()
    - 1
    - 1

  * - Standard RX
    - none
    - input_gpio_if i_gpio_rx; interface uart_rx_if i_rx;
    - uart_rx()
    - 1
    - 1

  * - Fast/streaming TX
    - out port p_uart_tx = XS1_PORT_1A;
    - streaming chan c;
    - uart_tx_streaming()
    - 1
    - 1

  * - Fast/streaming RX
    - in port p_uart_tx = XS1_PORT_1A;
    - streaming chan c;
    - uart_rx_streaming()
    - 1
    - 1

  * - Multi-UART TX (8 UARTs)
    - out buffered port:8 p_uart_tx  = XS1_PORT_8B;
    - interface multi_uart_tx_if i_tx;  chan c_tx;
    - multi_uart_tx()
    - 8
    - 1

  * - Multi-UART RX (8 UARTs)
    - in buffered port:32 p_uart_rx  = XS1_PORT_8B;
    - interface multi_uart_rx_if i_rx;  streaming chan c_rx;
    - multi_uart_rx()
    - 8
    - 1

  * - Half Duplex
    - port p_uart = XS1_PORT_1A;
    - interface uart_tx_buffered_if i_tx; uart_rx_if i_rx;  uart_control_if i_ctl;
    - uart_half_duplex()
    - 1
    - 1

