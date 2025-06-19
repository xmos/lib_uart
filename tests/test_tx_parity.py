# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and even on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200, 230400])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_tx_parity(baud, parity, do_test):

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 4, 1, 8)

    do_test(checker)
