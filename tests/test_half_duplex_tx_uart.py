
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and parity none on smoke
@pytest.mark.parametrize("baud", [115200, 57600, 28800])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE","UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_half_duplex_tx_uart(baud, parity, do_test):
    bin_path = f"app_uart_test_half_duplex/bin/{baud}_{parity}/app_uart_test_half_duplex_{baud}_{parity}.xe"
    expect_path = "expect/test_half_duplex_tx_uart.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1A", parity, baud, 4, 1, 8)

    do_test(bin_path, expect_path, checker)
