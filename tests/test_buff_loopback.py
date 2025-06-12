
import pytest
from uart_rx_checker import UARTRxChecker
from uart_tx_checker import UARTTxChecker

# 115200 on smoke
@pytest.mark.parametrize("baud", [115200, 57600, 28800, 14400])
def test_buff_loopback(baud, do_test):

    rx_checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B",
                               "UART_PARITY_NONE", baud, 1, 8)

    tx_checker = UARTTxChecker("tile[0]:XS1_PORT_1D", "tile[0]:XS1_PORT_1C",
                               "UART_PARITY_NONE", baud, 4, 1, 8)

    do_test([rx_checker, tx_checker])
