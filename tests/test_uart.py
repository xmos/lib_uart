
import sys
import pytest

class UartTester():
    def run(self, output):
        for line in output:
            if line.find("FAIL") != -1:
                sys.stderr.write(line)
                return False
        return True

# 115200 on smoke
@pytest.mark.parametrize("baud", [2400, 9600, 19200, 115200])
@pytest.mark.skip(reason="""currently hangs at "Reconfiguring parity to odd" test""")
def test_uart(baud, do_test):
    bin_path = f"app_uart_test/bin/{baud}/app_uart_test_{baud}.xe"
    sim_args = ["--plugin", "LoopbackPort.dll", "-port tile[0] XS1_PORT_1A 1 0 -port tile[1] XS1_PORT_1B 1 0"]

    tester = UartTester()
    do_test(bin_path, sim_args = sim_args, tester = tester)
