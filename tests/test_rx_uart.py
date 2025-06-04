
import pytest
import Pyxsim
from Pyxsim import testers
from uart_rx_checker import UARTRxChecker, Parity

# 115200 on smoke
@pytest.mark.parametrize("baud", [14400, 28800, 57600, 115200])
def test_rx_uart(baud, capfd):
    build_opts = [f"BAUD={baud}"]
    bin_path = f"app_uart_test_rx/bin/{baud}/app_uart_test_rx_{baud}.xe"
    sim_args = []
    
    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity["UART_PARITY_NONE"], baud, 1, 8)
    tester = testers.ComparisonTester(open('expect/test_rx_uart.expect'), regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
