lib_uart change log
===================

3.2.0
-----

  * ADDED:   Support for XCommon CMake
  * CHANGED: Use XMOS Public Licence Version 1
  * CHANGED: Example applications run on xcore.ai hardware
  * FIXED: Added an idle state initialisation in uart_tx_streaming()
  * FIXED: Fixed ILLEGAL_INSTRUCTION exception when using multi_uart_rx()

  * Changes to dependencies:

    - lib_gpio: 1.1.0 -> 2.2.0

    - lib_logging: 2.1.0 -> 3.3.1

    - lib_xassert: 3.0.0 -> 4.3.1

3.1.0
-----

  * RESOLVED: Correct the documentation for the write() method of
    uart_tx_buffered_if
  * RESOLVED: Added calls to ready_to_transmit() to the uart_tx_buffered
    component
  * RESOLVED: Improved the uart_tx_buffered so that it can now drive at full
    data rate without clock drift. Before it was limited to about 0.5% less than
    the baud rate

  * Changes to dependencies:

    - lib_gpio: 1.0.0 -> 1.1.0

    - lib_logging: 2.0.0 -> 2.1.0

    - lib_xassert: 2.0.0 -> 3.0.0

3.0.3
-----

  * REMOVED: forward references to app notes

3.0.2
-----

  * CHANGE: Update to source code license and copyright

3.0.1
-----

  * CHANGE: Update fast rx and tx to match API prototypes & fix port directions
  * RESOLVED: Fixed order of ports in api calls from example program

3.0.0
-----

  * CHANGE: Restructued version

  * Changes to dependencies:

    - lib_gpio: Added dependency 1.0.0

    - lib_logging: Added dependency 2.0.0

    - lib_xassert: Added dependency 2.0.0

2.3.2
-----

  * CHANGE: Increment version for XPD release. Several minor docs bugs fixed.

2.3.1
-----

  * CHANGE: Tidied up uart_fast and targetted demo at L16 sliceKIT

3.0.0
-----

  * CHANGE: Major change to generic UART tx/rx components to use new xC features
    with different api.

2.3.0
-----

  * ADDED: RS485 component and apps

2.2.0
-----

  * CHANGE: Updated documents for xSOFTip requirements
  * ADDED: Metainfo and XPD items

2.1.0
-----

  * CHANGE: Documentation Updates

