
import pytest
from uart_tx_checker import UARTTxChecker

# all nightly
@pytest.mark.parametrize("baud", [230400, 115200, 57600])
def test_buff_tx_basic(baud, do_test):

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 128, 1, 8)

    do_test(checker)
