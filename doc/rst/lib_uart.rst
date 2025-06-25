#################################
lib_uart: UART peripheral library
#################################

***********
Inroduction
***********

A software defined, industry-standard, UART (Universal Asynchronous
Receiver/Transmitter) library
that allows the user to control a UART serial connection via the
xcore GPIO ports. This library is controlled
via XC using the XMOS multicore extensions.

|newpage|

``lib_uart`` components
=======================

There are four ways to use the UART library detailed in the table below.

.. list-table::
 :widths: 20 80 
 :header-rows: 1

 * - UART type
   - Description
 * - Standard
   - Standard UARTs provide a flexible, fully configurable UART for
     speeds up to 115200 baud. The UART connects to ports via the GPIO
     library so can be used with single bits of
     multi-bit ports. Transmit can be buffered or unbuffered. The UART
     components run on a logical core but are combinable so can be
     run with other tasks on the same core (though the timing may be affected).
 * - Fast/streaming
   - The fast/streaming UART components provide a fixed configuration
     fast UART that streams data in and out via a streaming channel.
 * - Half-duplex
   - The half-duplex component performs receive and transmit on the
     same data line. The application controls the direction of the
     UART at runtime. It is particularly useful for RS485 connections.
 * - Multi-UART
   - The multi-UART components efficiently run several UARTS on the
     same core using a multibit port.

Using ``lib_uart``
==================

``lib_uart`` is intended to be used with the `XCommon CMake <https://www.xmos.com/file/xcommon-cmake-documentation/?version=latest>`_
, the `XMOS` application build and dependency management system.

To use this library, include ``lib_uart`` in the application's ``APP_DEPENDENT_MODULES`` list in
`CMakeLists.txt`, for example:

.. code-block:: cmake

    set(APP_DEPENDENT_MODULES "lib_uart")

Applications should then include the ``uart.h`` header file.

***************************
External signal description
***************************

The UART signals used by the library are high in their idle state. The
transmission of a character start with a *start bit* when the line
transitions from high to low. Then the data bits of the character are
then transmitted followed by an optional parity bit and a number of
stop bits (where the line is driven high). This sequence is shown in
:ref:`uart_waveform`. The data is driven least significant bit first.

.. _uart_waveform:

.. figure:: images/data_sequence.png
   :width: 100%

   UART data sequence

The start bit, data bits, parity bit and stop bits are all the same
length (``tBIT`` in :ref:`uart_waveform`). This length is give by the BAUD
rate which is the number of bits per second.

Connecting to the `xcore` device
================================

If using the standard UART Rx/Tx components then the UART line
can be connected to a bit of any port. The other bits of the port can
be shared using the GPIO library. Please refer to the GPIO library
user guide for restrictions on sharing bits of a port (for example,
all bits of a port need to be in the same direction - so UART rx and
UART tx cannot be put on the same port, see :ref:`connect_standard`).

.. _connect_standard:

.. figure:: images/connect_standard.*

   UART Rx and Tx connections

The half duplex UART needs to be connected to a 1-bit port (:ref:`connect_half_duplex`).

.. _connect_half_duplex:

.. figure:: images/connect_half_duplex.*

   UART half duplex connection

The fast/streaming UART also needs to be connect to a 1-bit port for
TX or RX (:ref:`connect_fast`).

.. _connect_fast:

.. figure:: images/connect_fast.*

   Fast/Streaming UART connections
  
|newpage|

The multi-UARTs need to be connected to 8-bit ports. If fewer than 8
UARTs are required then an 8-bit port must still be used with some of
the pins of the port not connected (:ref:`connect_multi`).

.. _connect_multi:

.. figure:: images/connect_multi.*

   Multi UART connections

For multi-UART receive, an incoming clock is required to acheive
standard baud rates. The clock should be a multiple of the maximum
BAUD rate required e.g. a 1843200 Hz oscillator is a multiple of
115200 baud (and lower rates also). The maximum allowable incoming
signal is 1843200 Hz.

For multi-UART transmit, an incoming clock can also be used. The same
clock signal can be shared between receive and transmit (i.e. only a
single 1-bit port need be used).

|newpage|

*****
Usage
*****

The following sections describe the four ways to use the UART library.

Standard UART usage
===================

UART components are instantiated as parallel tasks that run in a
``par`` statement. The application
can connect via an interface connection using the ``uart_rx_if`` (for
the UART Rx component) or the  ``uart_tx_if`` (for the UART Tx
component), see :ref:`uart_task_diag` for details.
Both components also have an optional configuration
interface that lets the application change the speed and properties of
the UART at run time.

.. _uart_task_diag:

.. figure:: images/uart_task_diag.*

  UART task diagram

For example, the following code instantiates a UART rx and UART tx
component and connects to them:

.. code-block:: C

  // Port declarations
  port p_uart_rx = on tile[0] : XS1_PORT_1A;
  port p_uart_tx = on tile[0] : XS1_PORT_1B;

  #define RX_BUFFER_SIZE 20

  int main() {
    interface uart_rx_if i_rx;
    interface uart_tx_if i_tx;
    input_gpio_if i_gpio_rx[1];
    output_gpio_if i_gpio_tx[1];
    par {
      on tile[0]: output_gpio(i_gpio_tx, 1, p_uart_tx, null);
      on tile[0]: uart_tx(i_tx, null,
                          115200, UART_PARITY_NONE, 8, 1,
                          i_gpio_tx[0]);
      on tile[0].core[0] : input_gpio_with_events(i_gpio_rx, 1, p_uart_rx, null);
      on tile[0].core[0] : uart_rx(i_rx, null, RX_BUFFER_SIZE,
                                   115200, UART_PARITY_NONE, 8, 1,
                                   i_gpio_rx[0]);
      on tile[0]: app(i_tx, i_rx);
    }
    return 0;
  }

The ``output_gpio`` task and ``input_gpio_with_events`` tasks are part
of the GPIO library for flexible use of multi-bit ports.
See the `GPIO library user guide <https://www.xmos.com/file/lib_gpio>`_ for details.

The application can use the client end of the interface connection to
perform UART operations e.g.:

.. code-block:: C

  void my_application(client uart_tx_if uart_tx,
                      client uart_rx_if uart_rx) {
     // Write a byte to the UART
     uart_tx.write(0xff);

     // Wait for a byte to
     select {
       case uart_rx.data_ready():
          uint8_t data = uart_rx.read();
          printf("Data received %d\n", data);
          // ...
          break;
     }
  }

UART configuration
------------------

The ``uart_config_if`` connection can be optionally connected to
either the UART Rx or Tx task e.g.:

.. code-block:: C

    // ...
    interface uart_tx_if i_tx;
    interface uart_cfg_if i_tx_cfg;
    input_gpio_if i_gpio_rx[1];
    par {
      // ...
      on tile[0]: uart_tx(i_tx, i_tx_cfg,
                          115200, UART_PARITY_NONE, 8, 1,
                          i_gpio_tx[0]);
      on tile[0]: app(i_tx, i_rx_cfg);
      // ...

The application can use this interface to dynamically reconfigure the
UART e.g.:

.. code-block:: C

   void app(client uart_tx_if uart_tx,
            client uart_config_if uart_tx_cfg) {
       // Configure the UART to 9600 BAUD
       uart_tx_cfg.set_baud_rate(9600);
       // Write to the UART
       uart_tx.write(0xff);
       // ...

If runtime configuration is not required then ``null`` can be passed
into the task instead of an interface connection.

Transmit buffering
------------------

There are two types of standard UART tx task: buffered and
un-buffered.

The buffered UART will buffer characters written to the
UART. It requires a separate logical core to feed characters from the
buffer to the UART pin. This frees the application to perform other
processing. The buffered UART will inform the application that data has been
transmitted and that there is more space in the buffer by calling the
:c:func:`ready_to_transmit` notification.

The unbuffered UART does not take its own logical core but calls to
``write`` will block until the character has been sent.

|newpage|

Fast/Streaming UART usage
=========================

The fast/streaming UART components are
instantiated as parallel tasks that run in a
``par`` statement and connected to the application via streaming channels (:ref:`fast_uart_task_diag`).

.. _fast_uart_task_diag:

.. figure:: images/fast_uart_task_diag.*

  Fast/streaming UART task diagram

For example, the following code instantiates a strreaming UART rx and UART tx
component and connects to them:

.. code-block:: C

  // Port declarations
  in port p_uart_rx = on tile[0] : XS1_PORT_1A;
  out port p_uart_tx = on tile[0] : XS1_PORT_1B;

  #define TICKS_PER_BIT 20

  int main() {
    streaming chan c_rx;
    streaming chan c_tx;
    par {
      on tile[0]: uart_tx_streaming(p_uart_tx, c_tx, TICKS_PER_BIT);
      on tile[0]: uart_rx_streaming(p_uart_rx, c_rx, TICKS_PER_BIT);
      on tile[0]: app(c_tx, c_rx);
    }
    return 0;
  }

The streaming channel has a limited amount of buffering
(~8 characters) but in general the application must deal with incoming
data as soon as it arrives.

The application can interact with the component using the
fast/streaming UART functions (see :ref:`fast_uart_api`) e.g.:

.. code-block:: C

  void app(streaming chanend c_tx, streaming chanend c_rx)
  {
     uart_tx_streaming_write_byte(c_tx, 0xff);
     uint8_t byte;
     uart_rx_streaming_read_byte(c_rx, byte);
     printf("Received: %d\n", byte);
     ...

|newpage|

Half-duplex UART usage
======================

The half-duplex components are instantiated as parallel tasks that run in a
``par`` statement. The application
connects via three interface connections: the ``uart_rx_if`` (for
receiving data), the ``uart_tx_if`` (for transmitting data) and the
``uart_control_if`` (for controlling the current direction of the UART)(:ref:`half_duplex_task_diag`).
The component also has an optional configuration
interface that lets the application change the speed and properties of
the UART at run time.

.. _half_duplex_task_diag:

.. figure:: images/half_duplex_task_diag.*

  Half-duplex UART task diagram

For example, the following code instantiates a half-duplex UART
component and connects to it:

.. code-block:: C

  #define TX_BUFFER_SIZE 16
  #define RX_BUFFER_SIZE 16

  port p_uart = on tile[0] : XS1_PORT_1A;

  int main() {
    interface uart_rx_if i_rx;
    interface uart_control_if i_control;
    interface uart_tx_buffered_if i_tx;

    par {
      on tile[0] : uart_half_duplex(i_tx, i_rx, i_control, null,
                                    TX_BUFFER_SIZE, RX_BUFFER_SIZE,
                                    115200, UART_PARITY_NONE, 8, 1, p_uart);

      on tile[0] : app(i_rx, i_tx, i_control);
    }

The application can use the interfaces in the same manner as a
standard UART. The control interface can be used to change direction e.g.:

.. code-block:: C

  void app(client uart_rx_if i_uart_rx,
           client uart_tx_buffered_if i_uart_tx,
           client uart_control_if i_control) {
     uint8_t byte;
     i_control.set_mode(UART_RX_MODE);
     byte = i_uart_rx.read();
     i_control.set_mode(UART_TX_MODE);
     i_uart_tx.write(byte);
     ...

|newpage|

Multi-UART usage
================

Multi-UART components are instantiated as parallel tasks that run in a
``par`` statement. The application
can connect via a combination of a channel and
an interface connection using the ``multi_uart_rx_if``
(for the UART Rx component) or the  ``multi_uart_tx_if`` (for the UART Tx
component). These interfaces handle data for all the UARTs and runtime
configuration (:ref:`multi_uart_task_diag`).

.. _multi_uart_task_diag:

.. figure:: images/multi_uart_task_diag.*

  Multi-UART task diagram

For example, the following code instantiates a multi-UART RX and multi-UART TX
component and connects to them:

.. code-block:: C

  in  buffered port:32 p_uart_rx = XS1_PORT_8A;
  out buffered port:8 p_uart_tx  = XS1_PORT_8B;
  in  port p_uart_clk            = XS1_PORT_1F;

  clock clk_uart = XS1_CLKBLK_4;

  int main(void)
  {
    interface multi_uart_rx_if i_rx;
    streaming chan c_rx;
    chan c_tx;
    interface multi_uart_tx_if i_tx;

    // Set the rx and tx lines to be clocked off the clk_uart clock block
    configure_in_port(p_uart_rx, clk_uart);
    configure_out_port(p_uart_tx, clk_uart, 0);

    // Configure an external clock for the clk_uart clock block
    configure_clock_src(clk_uart, p_uart_clk);
    start_clock(clk_uart);

    // Start the rx/tx tasks and the application task
    par {
      multi_uart_rx(c_rx, i_rx, p_uart_rx, 8, 1843200, 115200, UART_PARITY_NONE, 8, 1);
      multi_uart_tx(c_tx, i_tx, p_uart_tx, 8, 1843200, 115200, UART_PARITY_NONE, 8, 1);
     app(c_rx, i_rx, c_tx, i_tx);
    }
  }

|newpage|
The application communicates with all the UARTs via the single
multi-UART interfaces e.g.:

.. code-block:: C

  void loopback(streaming chanend c_rx, client multi_uart_rx_if i_rx,
                chanend c_tx, client multi_uart_tx_if i_tx)
  {
    size_t uart_num;

    // Configure each task with a chanend
    i_rx.init(c_rx);
    i_tx.init(c_tx);

    while (1) {
      select {
      case multi_uart_data_ready(c_rx, uart_num):
        uint8_t data;
        if (i_rx.read(uart_num, data) == UART_RX_VALID_DATA) {
          if (i_tx.is_slot_free(uart_num)) {
            i_tx.write(uart_num, data);
          }
          else {
            debug_printf("Warning: TX buffer overflow on channel %d\n",
                         uart_num);
          }
        }
        break;
      }
    }
  }

Note that the ``init`` function on the interface must be called once
before any use of the interface.

Configuring clocks for multi-UARTs
----------------------------------

The ports used for the multi-UART components need to have their clocks
configured. For example, the following code configures the multi-UART
RX port to run of a clock that is sourced by an incoming port:

.. code-block:: C

    // Set the rx line to be clocked off the clk_uart clock block
    configure_in_port(p_uart_rx, clk_uart);

    // Configure an external clock for the clk_uart clock block
    configure_clock_src(clk_uart, p_uart_clk);
    start_clock(clk_uart);

For more information on configuring ports, please refer to the
`XMOS Programming Guide` for more details.

The multi-UART components take an argument which is the speed of the
underlying clock. This way the component can attain the correct BAUD
rate.

The multi-UART RX component must be clocked of a rate which is a
multiple of the BAUD rates required.

If a port is not explicitly configured, then it will be clocked of the
reference 100Mhz clock of the xcore. The TX component can also work
with this clock rate.

|newpage|

Runtime configuration of the Multi-UARTs
----------------------------------------

The re-configuration of a one of the UARTS in the multi-UART is done
via the main ``multi_uart_tx_if`` or ``multi_uart_rx_if``. In both
cases, the user must call the ``pause`` function of the interface,
then a reconfiguration function and then the ``restart`` function
e.g.:

.. code-block:: C

  void app(streaming chanend c_rx, client multi_uart_rx_if i_rx)
    // ...
    i_rx.pause();
    // Set UART number 2 to baud rate 9600
    i_rx.set_baud_rate(2, 9600);
    i_rx.restart();
    // ...

********
Examples
********

Various example application are provided alongside the ``lib_uart`` which demonstrates the use of the different UART components. 
These examples can be found in the ``examples`` directory of the library.
All examples provided run on `XK-EVK-XU316 <https://www.xmos.com/xk-evk-xu316>`_ board.

Basic and Streaming UART examples
=================================

The basic and streaming UART examples demonstrate the use of the API to loopback data
between the UART Tx and Rx components. The examples are designed to be run on a
single tile with the UART connection between the *XS1_PORT_1J* and *XS1_PORT_1M* ports (shared with *WIFI MOSI* and *WIFI MISO* on *XK-EVK-XU316*).
So make sure to connect these pins with a jumper wire for the example to work.

Multi-UART example
==================

The multi-UART example demonstrates the use of the multi-UART API to loopback data between multi-UART Tx and Rx components .
This example requires two 8-bit ports and a shared clock.
The ports chosen are *XS1_PORT_8B* on tile 0 (*X0D14* - *X0D21* in the top left header) and *XS1_PORT_8A* on tile 1 (*X1D02* - *X1D08* in the bottom left header and *CODEC RST_N* which is *X1D09*).
The application will generate a PLL clock on *MCLK* (*X1D11*) which needs to be shared with tile 0 *XS1_PORT_1A* (*X0D00*) port.
Make sure to connect 8-bit ports and the share the clock for the example to work.

Running the examples
====================

This section will describe how to build and run the example applications provided with the ``lib_uart`` library. 
The application chosen for this section is the ``app_uart_demo`` which demonstrates the use of the standard UART API.
For other examples, the process is similar, but the application/folder name will change.

Building
--------

The following section assumes that the `XMOS XTC tools <https://www.xmos.com/software-tools/>`_ has
been downloaded and installed (see `README` for required version).

Installation instructions can be found `here <https://xmos.com/xtc-install-guide>`_. Particular
attention should be paid to the section `Installation of required third-party tools
<https://www.xmos.com/documentation/XM-014363-PC-10/html/installation/install-configure/install-tools/install_prerequisites.html>`_.

The application uses the `XMOS` build and dependency system, `xcommon-cmake <https://www.xmos.com/file/xcommon-cmake-documentation/?version=latest>`_. `xcommon-cmake` is bundled with the `XMOS` XTC tools.

To configure the build, run the following from an XTC command prompt:

.. code-block:: console

  cd examples
  cd app_uart_demo
  cmake -G "Unix Makefiles" -B build

Any missing dependencies will be downloaded by the build system at this configure step.

Finally, the application binaries can be built using ``xmake``:

.. code-block:: console

  xmake -j -C build

Running the application
-----------------------

To run the application return to the ``/examples/app_uart_demo`` directory and run
the following command:

.. code-block:: console

  xrun --xscope bin/app_uart_demo.xe

As application runs and loopbacks data between the UART Tx and Rx components, it will print the received data to the console.

*********
UART APIs
*********

Standard UART API
=================

UART configuration interface
----------------------------

.. doxygengroup:: uart_config_if
  :no-link:

.. doxygenenum:: uart_parity_t

|newpage|

UART receiver component
-----------------------

.. doxygenfunction:: uart_rx

|newpage|

UART receive interface
----------------------

.. doxygengroup:: uart_rx_if
  :no-link:

|newpage|

UART transmitter components
---------------------------

.. doxygenfunction:: uart_tx
.. doxygenfunction:: uart_tx_buffered

|newpage|

UART transmit interface
-----------------------

.. doxygengroup:: uart_tx_if
  :no-link:

UART transmit interface (buffered)
----------------------------------

.. doxygengroup:: uart_tx_buffered_if
  :no-link:

|newpage|

.. _fast_uart_api:

Fast/Streaming API
==================

Streaming receiver
------------------

.. doxygenfunction:: uart_rx_streaming
.. doxygenfunction:: uart_rx_streaming_read_byte

|newpage|

Streaming transmitter
---------------------

.. doxygenfunction:: uart_tx_streaming
.. doxygenfunction:: uart_tx_streaming_write_byte

|newpage|

Half-Duplex API
===============

Half-duplex component
---------------------

.. doxygenfunction:: uart_half_duplex

Half-duplex control interface
-----------------------------

.. doxygenenum:: uart_half_duplex_mode_t

.. doxygengroup:: uart_control_if
  :no-link:

|newpage|

Multi-UART API
==============

Multi-UART receiver
-------------------

.. doxygenfunction:: multi_uart_rx

|newpage|

Multi-UART receive interface
----------------------------

.. doxygenenum:: multi_uart_read_result_t

.. doxygengroup:: multi_uart_rx_if
  :no-link:

|newpage|

Multi-UART transmitter
----------------------

.. doxygenfunction:: multi_uart_tx

|newpage|

Multi-UART transmit interface
-----------------------------

.. doxygengroup:: multi_uart_tx_if
  :no-link:
