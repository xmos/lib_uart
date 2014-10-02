UART library
============

Summary
-------

A software defined, industry-standard, UART (Universal Asynchronous
Receiver/Transmitter) library
that allows you to control an UART serial connection via the
xCORE GPIO hardware-response ports. This library is controlled
via C using the XMOS multicore extensions and can either act as UART master or slave.

Features
........

 * UART receive and transmit
 * Supports speeds up to 10MBit/s
 * Half-duplex handshaking mode (applicable to RS485)
 * Efficient multi-uart mode for implementing multiple connections

Components
..........

 * Standard UART mode
 * Fast streaming UART mode
 * Multi-UART mode

