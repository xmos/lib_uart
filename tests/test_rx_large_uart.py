
import pytest
import Pyxsim
from Pyxsim import testers
from uart_rx_checker import UARTRxChecker, Parity

# all nightly
@pytest.mark.parametrize("baud", [57600, 115200])
@pytest.mark.parametrize("parity", ['UART_PARITY_NONE', 'UART_PARITY_ODD', 'UART_PARITY_EVEN'])
def test_rx_large_uart(baud, parity, capfd):
    build_opts = [f"BAUD={baud}", f"PARITY={parity}"]
    bin_path = f"app_uart_test_rx_large/bin/{baud}_{parity}/app_uart_test_rx_large_{baud}_{parity}.xe"
    sim_args = []

    checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity[parity], baud, 1, 8, range(128))
    tester = testers.ComparisonTester(open('expect/test_rx_large_uart.expect'), regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
