.. include:: ../../../README.rst

Resource Usage
..............

TODO


Hardware characteristics
------------------------

TODO

Usage
-----

The are four ways to use the UART library detailed in the table below.

.. list-table::
 :header-rows: 1

 * - UART type
   - Description
 * - Standard
   - Standard UARTs provide a flexible, fully configurable UART for
     speeds up to 115200 baud. The UART connects to ports via the GPIO
     library (reference??) so can be used with single bits of
     multi-bit ports. Transmit can be buffered or unbuffered. The UART
     components runs on a logical core but are combinable so can be
     run with other tasks on the same core (though the timing may be affected).
 * - Fast/streaming
   - The fast/streaming UART components provide a fixed configuration
     fast UART that streams data in and out via a streaming channel.
 * - Half-duplex
   - The half-duplex component performs receive and transmit on the
     same data line. The application controls the direction of the
     UART at runtime. It is particularly useful for RS485 connections (link?)
 * - Multi-UART
   - The multi-UART components efficiently run several UARTS on the
     same core using a multibit port.

Standard UART usage
...................

TODO

Fast/Streaming UART usage
.........................

TODO

Half-duplex UART usage
......................

TODO

Multi-UART usage
................

TODO

Standard UART API
-----------------

UART configuration interface
............................

.. doxygeninterface:: uart_config_if

|newpage|

.. doxygenenum:: uart_parity_t

|newpage|

UART receiver component
.......................

.. doxygenfunction:: uart_rx

|newpage|

UART receive interface
......................

.. doxygeninterface:: uart_rx_if

|newpage|

UART transmitter components
...........................

.. doxygenfunction:: uart_tx

|newpage|

.. doxygenfunction:: uart_tx_buffered

|newpage|

UART transmit interface
......................

.. doxygeninterface:: uart_tx_if

|newpage|

UART transmit interface (buffered)
..................................

.. doxygeninterface:: uart_tx_buffered_if

|newpage|

Fast/Streaming API
-----------------------

Streaming receiver
..................

.. doxygenfunction:: uart_rx_streaming
.. doxygenfunction:: uart_rx_streaming_read_byte

Streaming transmitter
.....................

.. doxygenfunction:: uart_tx_streaming
.. doxygenfunction:: uart_tx_streaming_write_byte

Half-Duplex API
---------------

Half-duplex component
.....................

.. doxygenfunction:: uart_half_duplex

|newpage|

Half-duplex control interface
.............................

.. doxygenenum:: uart_half_duplex_mode_t

.. doxygeninterface:: uart_control_if


Multi-UART API
--------------

Multi-UART receiver
...................

.. doxygenfunction:: multi_uart_rx

|newpage|

Multi-UART receive interface
............................

.. doxygeninterface:: multi_uart_rx_if

|newpage|

Multi-UART transmitter
......................

.. doxygenfunction:: multi_uart_tx

|newpage|

Multi-UART transmit interface
............................

.. doxygeninterface:: multi_uart_tx_if
