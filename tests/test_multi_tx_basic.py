# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import pytest
from uart_tx_checker import UARTTxChecker
from uart_clock_device  import UARTClockDevice

# 115200 on smoke
@pytest.mark.parametrize("baud", [115200, 57600])
@pytest.mark.parametrize("internal_clock", [1, 0])
def test_multi_tx_basic(baud, internal_clock, do_test):
    # internal_clock is only used for xmake which is handled in a fixture

    tx_checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_8B.1", "UART_PARITY_NONE", baud, 4, 1, 8)
    uart_clock = UARTClockDevice("tile[0]:XS1_PORT_1F", 230400)

    do_test([tx_checker, uart_clock])
