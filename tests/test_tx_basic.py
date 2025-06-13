
import pytest
from uart_tx_checker import UARTTxChecker

# all nightly
@pytest.mark.parametrize("baud", [57600, 115200, 230400])
def test_tx_basic(baud, do_test):

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 128, 1, 8)

    do_test(checker)
