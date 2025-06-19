# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import pytest
from uart_rx_checker import DriveHigh, UARTRxChecker
from uart_clock_device  import UARTClockDevice

# 115200 and on smoke
@pytest.mark.parametrize("baud", [115200, 57600])
def test_multi_rx_basic(baud, do_test):

    rx_checker = UARTRxChecker("tile[0]:XS1_PORT_8B.0", "tile[0]:XS1_PORT_1A", "UART_PARITY_NONE", baud, 1, 8, data=[0x7f, 0x00, 0x2f, 0xff])
    rx_checker2 = UARTRxChecker("tile[0]:XS1_PORT_8B.2", "tile[0]:XS1_PORT_1A", "UART_PARITY_NONE", baud/2, 1, 8, data=[0xaa, 0x01, 0xfc, 0x8e])
    uart_clock = UARTClockDevice("tile[0]:XS1_PORT_1L", 1843200)

    drive_high0 = DriveHigh("tile[0]:XS1_PORT_8B.1")

    do_test([drive_high0, rx_checker, rx_checker2, uart_clock])
