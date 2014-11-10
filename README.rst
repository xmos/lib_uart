UART library
============

.. rheader::

   UART |version|

Summary
-------

A software defined, industry-standard, UART (Universal Asynchronous
Receiver/Transmitter) library
that allows you to control an UART serial connection via the
xCORE GPIO hardware-response ports. This library is controlled
via C using the XMOS multicore extensions.

Features
........

 * UART receive and transmit
 * Supports speeds up to 10MBit/s
 * Half-duplex handshaking mode (applicable to RS485)
 * Efficient multi-uart mode for implementing multiple connections

How many UARTS are available?
.............................

XMOS devices work by using the I/O pins to implement peripherals. So
the number of UARTs only depends on how many I/O pins there are and
how much processing is available. The UART components take 1 pin per
input and output and can fit up to 8 receivers or transmitters per
logical core of the device.

Operating Modes
...............

 * Standard UART - fully flexible usage up to 115200 baud.
 * Fast streaming UART - speeds up to 10MBit/s.
 * Half duplex UART - suitable for RS485 links.
 * Multi-UART - efficient implementation of multiple UARTs.

