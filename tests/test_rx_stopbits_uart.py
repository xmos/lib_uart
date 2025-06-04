
import pytest
import Pyxsim
from Pyxsim import testers
from uart_rx_checker import UARTRxChecker, Parity

# 115200 and 2 are smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("stopbits", [1, 2, 3])
def test_rx_stopbits_uart(baud, stopbits, capfd):
    build_opts = [f"BAUD={baud}", f"STOPBITS={stopbits}"]
    bin_path = f"app_uart_test_rx_stopbits/bin/{baud}_{stopbits}/app_uart_test_rx_stopbits_{baud}_{stopbits}.xe"
    sim_args = []

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity["UART_PARITY_NONE"], baud, stopbits, 8)
    tester = testers.ComparisonTester(open('expect/test_rx_stopbits_uart.expect'), regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
