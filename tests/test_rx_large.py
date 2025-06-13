
import pytest
from uart_rx_checker import UARTRxChecker

# all nightly
@pytest.mark.parametrize("baud", [57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_ODD", "UART_PARITY_EVEN"])
def test_rx_large(baud, parity, do_test):

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 1, 8, range(128))

    do_test(checker)
