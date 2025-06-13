
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_tx_stopbits(baud, stopbits, do_test):
    expect_path = "expect/test_tx_parity.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 4, stopbits, 8)

    do_test(checker, expect_path)
