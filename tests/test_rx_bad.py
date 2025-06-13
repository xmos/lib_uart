
import pytest
from uart_rx_checker import UARTRxChecker

# 115200 on smoke
@pytest.mark.parametrize("baud", [57600, 115200])
def test_rx_bad(baud, do_test):

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_BAD", baud, 1, 8)

    do_test(checker)
