
import pytest
from uart_rx_checker import UARTRxChecker

# 230400 on smoke
@pytest.mark.parametrize("baud", [230400, 460800, 921600])
def test_fast_rx_basic(baud, do_test):

    expect_path = "expect/test_rx_basic.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 1, 8)

    do_test(checker, expect_path)
