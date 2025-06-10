
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and even on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200, 230400])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_tx_parity_uart(baud, parity, do_test):
    bin_path = f"app_uart_test_parity/bin/{baud}_{parity}/app_uart_test_parity_{baud}_{parity}.xe"
    expect_path = "expect/test_tx_parity_uart.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 4, 1, 8)

    do_test(bin_path, expect_path, checker)
