
import pytest
import Pyxsim
from Pyxsim import testers
from uart_tx_checker import UARTTxChecker, Parity

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_tx_stopbits_uart(baud, stopbits, capfd):
    build_opts = [f"BAUD={baud}", f"STOPBITS={stopbits}"]
    bin_path = f"app_uart_test_stopbits/bin/{baud}_{stopbits}/app_uart_test_stopbits_{baud}_{stopbits}.xe"
    sim_args = []

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity['UART_PARITY_NONE'], baud, 4, stopbits, 8)

    file = open('expect/test_tx_parity_uart.expect')
    expected = [x.strip() for x in file.readlines()]
    expected = [x.strip() for x in expected if x != ""]

    tester = testers.ComparisonTester(expected, regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
