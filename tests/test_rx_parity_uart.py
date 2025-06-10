
import pytest
from uart_rx_checker import UARTRxChecker


# 115200 and no parity on smoke
@pytest.mark.parametrize("baud", [14400, 28800, 57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_rx_parity_uart(baud, parity, do_test):
    bin_path = f"app_uart_test_rx_parity/bin/{baud}_{parity}/app_uart_test_rx_parity_{baud}_{parity}.xe"
    expect_path = "expect/test_rx_parity_uart.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 1, 8)

    do_test(bin_path, expect_path, checker)
