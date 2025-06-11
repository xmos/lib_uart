
import pytest
from uart_rx_checker import UARTRxChecker

# all nightly
@pytest.mark.parametrize("baud", [57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_ODD", "UART_PARITY_EVEN"])
def test_rx_large_uart(baud, parity, do_test):
    bin_path = f"app_uart_test_rx_large/bin/{baud}_{parity}/app_uart_test_rx_large_{baud}_{parity}.xe"
    expect_path = "expect/test_rx_large_uart.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 1, 8, range(128))

    do_test(bin_path, expect_path, checker)
