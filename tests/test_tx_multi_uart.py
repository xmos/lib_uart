
import pytest
from uart_tx_checker import UARTTxChecker
from uart_clock_device  import UARTClockDevice

# 115200 on smoke
@pytest.mark.parametrize("baud", [115200, 57600])
@pytest.mark.parametrize("internal_clock", [1, 0])
def test_tx_multi_uart(baud, internal_clock, do_test):
    bin_path = f"app_uart_test_multi_tx/bin/{baud}_{internal_clock}/app_uart_test_multi_tx_{baud}_{internal_clock}.xe"
    expect_path = "expect/test_tx_multi_uart.expect"

    tx_checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_8B.1", "UART_PARITY_NONE", baud, 4, 1, 8)
    uart_clock = UARTClockDevice("tile[0]:XS1_PORT_1F", 230400)

    do_test(bin_path, expect_path, [tx_checker, uart_clock])
