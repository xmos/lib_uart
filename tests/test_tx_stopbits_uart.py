
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_tx_stopbits_uart(baud, stopbits, do_test):
    bin_path = f"app_uart_test_stopbits/bin/{baud}_{stopbits}/app_uart_test_stopbits_{baud}_{stopbits}.xe"
    expect_path = "expect/test_tx_parity_uart.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", "UART_PARITY_NONE", baud, 4, stopbits, 8)

    do_test(bin_path, expect_path, checker)
