UART library
============

.. xsoftip:: UART
   :version: 3.0.0

UART library
------------

A software defined, industry-standard, UART (**U** |-| niversal **A**
|-| synchronous **R** |-| eceiver/**T** |-| ransmitter) library
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

Resource Usage
..............

.. list-table::
   :header-rows: 1
   :class: wide vertical-borders horizontal-borders

   * - Configuration
     - Pins
     - Ports
     - Clocks
     - Ram
     - Logical cores
   * - Standard RX
     - 1
     - 1 x 1-bit
     - 0
     - ~1.2k
     - 1
   * - Standard TX
     - 1
     - 1 x 1-bit
     - 0
     - ~1.2k
     - 0 :sup:`1`
   * - Fast/Streaming RX
     - 1
     - 1 x 1-bit
     - 1
     - ~1.2k
     - 1
   * - Fast/Streaming TX
     - 1
     - 1 x 1-bit
     - 1
     - ~1.2k
     - 1
   * - Multi-UART RX
     - 1
     - 1 x 1-bit
     - 1
     - ~1.2k
     - 1
   * - Multi-UART TX
     - 1
     - 1 x 1-bit
     - 1
     - ~1.2k
     - 1

:sup:`1` By default the stanard UART TX configuration does not take any
logical cores of its own but requires processing on the core the
application is running on.


Hardware characteristics
------------------------

TODO

API
---

TODO
