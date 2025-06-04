
import pytest
import Pyxsim
from Pyxsim import testers
from uart_tx_checker import UARTTxChecker, Parity

# all nightly
@pytest.mark.parametrize("baud", [57600, 115200, 230400])
def test_tx_uart(baud, capfd):
    build_opts = [f"BAUD={baud}"]
    bin_path = f"app_uart_test_tx/bin/{baud}/app_uart_test_tx_{baud}.xe"
    sim_args = []
    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity['UART_PARITY_NONE'], baud, 128, 1, 8)

    file = open('expect/test_tx_uart.expect')
    expected = [x.strip() for x in file.readlines()]
    expected = [x.strip() for x in expected if x != ""]

    tester = testers.ComparisonTester(expected, regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
