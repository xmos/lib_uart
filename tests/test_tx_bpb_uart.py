
import pytest
import Pyxsim
from Pyxsim import testers
from uart_tx_checker import UARTTxChecker, Parity

# 115200 and even parity on smoke
@pytest.mark.parametrize("baud", [14400, 57600, 115200])
@pytest.mark.parametrize("parity", ['UART_PARITY_NONE', 'UART_PARITY_ODD', 'UART_PARITY_EVEN'])
@pytest.mark.parametrize("bpb", [5, 7, 8])
def test_tx_bpb_uart(baud, parity, bpb, capfd):
    build_opts = [f"BAUD={baud}", f"PARITY={parity}", f"BPB={bpb}"]
    bin_path = f"app_uart_test_bpb/bin/{baud}_{parity}_{bpb}/app_uart_test_bpb_{baud}_{parity}_{bpb}.xe"
    sim_args = []

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity[parity], baud, 4, 1, bpb)

    file = open('expect/test_tx_bpb_uart.expect')
    expected = [x.strip() for x in file.readlines()]
    expected = [x.strip() for x in expected if x != ""]

    tester = testers.ComparisonTester(expected, regexp=True)
    assert Pyxsim.run_on_simulator(bin_path, simthreads=[checker], tester=tester, 
                                    simargs=sim_args,capfd=capfd, build_options=build_opts)
