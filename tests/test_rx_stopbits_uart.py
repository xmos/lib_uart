
import pytest
from uart_rx_checker import UARTRxChecker

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_rx_stopbits_uart(baud, stopbits, do_test):
    bin_path = f"app_uart_test_rx_stopbits/bin/{baud}_{stopbits}/app_uart_test_rx_stopbits_{baud}_{stopbits}.xe"
    expect_path = "expect/test_rx_stopbits_uart.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, stopbits, 8)

    do_test(bin_path, expect_path, checker)
