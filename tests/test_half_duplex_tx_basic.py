
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and parity none on smoke
@pytest.mark.parametrize("baud", [115200, 57600, 28800])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE","UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_half_duplex_tx_basic(baud, parity, do_test):

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1A", parity, baud, 4, 1, 8)

    do_test(checker)
