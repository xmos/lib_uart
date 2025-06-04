
import pytest
import Pyxsim
from Pyxsim import testers
from uart_tx_checker import UARTTxChecker, Parity

# 115200 and even on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200, 230400])
@pytest.mark.parametrize("parity", ['UART_PARITY_NONE', 'UART_PARITY_EVEN', 'UART_PARITY_ODD'])
def test_tx_parity_uart(baud, parity, capfd):
    build_opts = [f"BAUD={baud}", f"PARITY={parity}"]
    bin_path = f"app_uart_test_parity/bin/{baud}_{parity}/app_uart_test_parity_{baud}_{parity}.xe"
    sim_args = []

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity[parity], baud, 4, 1, 8)

    file = open('expect/test_tx_parity_uart.expect')
    expected = [x.strip() for x in file.readlines()]
    expected = [x.strip() for x in expected if x != ""]

    tester = testers.ComparisonTester(expected, regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
