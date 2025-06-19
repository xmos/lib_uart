# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

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
def test_loopback(baud, do_test):
    # baud is only used for xmake which is handled in the fixture
    sim_args = ["--plugin", "LoopbackPort.dll", "-port tile[0] XS1_PORT_1A 1 0 -port tile[1] XS1_PORT_1B 1 0"]

    tester = UartTester()
    do_test(sim_args = sim_args, tester = tester)
