
import pytest
from uart_rx_checker import UARTRxChecker

# 115200 on smoke
@pytest.mark.parametrize("baud", [57600, 115200])
def test_rx_intermittent(baud, do_test):
    bin_path = f"app_uart_test_rx_intermittent/bin/{baud}/app_uart_test_rx_intermittent_{baud}.xe"
    expect_path = "expect/test_rx_intermittent_uart.expect"

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B",
                            "UART_PARITY_BAD", baud, 1, 8,
                            data=range(50), intermittent=True)

    do_test(bin_path, expect_path, checker)
