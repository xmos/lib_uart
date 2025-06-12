
import pytest
from uart_half_duplex_checker import UARTHalfDuplexChecker

# 115200 and parity none on smoke
@pytest.mark.parametrize("baud", [115200, 57600])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_EVEN", "UART_PARITY_ODD"])
def test_half_duplex_loopback(baud, parity, do_test):

    checker = UARTHalfDuplexChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B",
                                       parity, baud, 4, 1, 8)
    
    do_test(checker)
