
import pytest
from uart_rx_checker import UARTRxChecker

@pytest.mark.parametrize("baud", [115200])
def test_half_duplex_rx_uart(baud, do_test):
    bin_path = f"app_uart_test_half_duplex_rx/bin/{baud}/app_uart_test_half_duplex_rx_{baud}.xe"
    expect_path = "expect/test_half_duplex_rx_uart.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 1, 8)

    do_test(bin_path, expect_path, checker)
