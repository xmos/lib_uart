
import pytest
from uart_rx_checker import UARTRxChecker

# 115200 and no parity on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_ODD", "UART_PARITY_EVEN"])
@pytest.mark.parametrize("bits_per_byte", [5, 7, 8])
def test_rx_bpb(baud, parity, bits_per_byte, do_test):
    
    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B",
                            parity, baud, 1, bits_per_byte,
                            [0x00, 0x1a, 0x07, 0x12])

    do_test(checker)
