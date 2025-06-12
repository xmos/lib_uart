
import pytest
from uart_tx_checker import UARTTxChecker

# 115200 and even parity on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("parity", ["UART_PARITY_NONE", "UART_PARITY_ODD", "UART_PARITY_EVEN"])
@pytest.mark.parametrize("bits_per_byte", [5, 7, 8])
def test_tx_bpb(baud, parity, bits_per_byte, do_test):
    
    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", parity, baud, 4, 1, bits_per_byte)

    do_test(checker)
