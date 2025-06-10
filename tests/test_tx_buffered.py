
import pytest
from uart_tx_checker import UARTTxChecker

# all nightly
@pytest.mark.parametrize("baud", [230400, 115200, 57600])
def test_tx_buffered(baud, do_test):
    bin_path = f"app_uart_test_tx_buffered/bin/{baud}/app_uart_test_tx_buffered_{baud}.xe"
    expect_path = "expect/test_tx_buffered.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 128, 1, 8)

    do_test(bin_path, expect_path, checker)
