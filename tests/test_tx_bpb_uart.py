
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and even parity on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_ODD", "UART_PARITY_EVEN"])
@pytest.mark.parametrize("bits_per_byte", [5, 7, 8])
def test_tx_bpb_uart(baud, parity, bits_per_byte, do_test):
    bin_path = f"app_uart_test_bpb/bin/{baud}_{parity}_{bits_per_byte}/app_uart_test_bpb_{baud}_{parity}_{bits_per_byte}.xe"
    expect_path = "expect/test_tx_bpb_uart.expect"

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 4, 1, bits_per_byte)

    do_test(bin_path, expect_path, checker)
