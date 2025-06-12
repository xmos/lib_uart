
import pytest
from uart_rx_checker import UARTRxChecker

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_rx_stopbits(baud, stopbits, do_test):

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, stopbits, 8)

    do_test(checker)
