:orphan:

#################################
lib_uart: UART peripheral library
#################################

:vendor: XMOS
:version: 3.2.0
:scope: General Use
:description: UART peripheral library
:category: General Purpose
:keywords: IO, UART, serial
:devices: xcore-200, xcore.ai

*******
Summary
*******

A software defined, industry-standard, UART (Universal Asynchronous
Receiver/Transmitter) library
that allows the user to control a UART serial connection via the
xcore GPIO ports. This library is controlled
via XC using the XMOS multicore extensions.

********
Features
********

* UART receive and transmit
* Supports speeds up to 10MBit/s
* Half-duplex mode (applicable to RS485)
* Efficient multi-uart mode for implementing multiple connections

************
Known issues
************

* None

****************
Development repo
****************

* `lib_uart <https://www.github.com/xmos/lib_uart>`_

**************
Required tools
**************

* XMOS XTC Tools: 15.3.1

*********************************
Required libraries (dependencies)
*********************************

* lib_gpio (www.github.com/xmos/lib_gpio)
* lib_logging (www.github.com/xmos/lib_logging)
* lib_xassert (www.github.com/xmos/lib_xassert)

*************************
Related application notes
*************************

* None

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at
`www.xmos.com/support <https://www.xmos.com/support>`_
