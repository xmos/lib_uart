
import pytest
from uart_rx_checker import UARTRxChecker


# 115200 and no parity on smoke
@pytest.mark.parametrize("baud", [14400, 28800, 57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_rx_parity(baud, parity, do_test):

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 1, 8)

    do_test(checker)
