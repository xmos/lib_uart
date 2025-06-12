
import pytest
from uart_tx_checker import UARTTxChecker

# 230400 on smoke
@pytest.mark.parametrize("baud", [57600, 115200, 230400])
def test_tx_intermittent(baud, do_test):

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", 'UART_PARITY_NONE', baud, 64, 1, 8)

    do_test(checker)
