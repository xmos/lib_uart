
import pytest
from uart_tx_checker import UARTTxChecker

# 230400 on smoke
@pytest.mark.parametrize("baud", [230400, 460800, 921600])
def test_fast_tx_basic(baud, do_test):
    if baud == 921600:
        pytest.xfail("There's a bug related to how fast we get into the idle state (1). May be a test bug")

    expect_path = "expect/test_tx_basic.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 128, 1, 8)

    do_test(checker, expect_path)
