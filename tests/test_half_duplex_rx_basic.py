
import pytest
from uart_rx_checker import UARTRxChecker

@pytest.mark.parametrize("baud", [115200])
def test_half_duplex_rx_basic(baud, do_test):

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 1, 8)

    do_test(checker)
