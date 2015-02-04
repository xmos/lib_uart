import xmostest
import os
from xmostest.xmostest_subprocess import call
from uart_tx_checker import UARTTxChecker, Parity


def do_test(baud):
    myenv = {'baud':baud}
    path = "app_uart_test_parity"
    resources = xmostest.request_resource("xsim")

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity[parity], baud, 4, 0xC0)
    tester  = xmostest.ComparisonTester(open('test_parity_uart.expect'),
                                        "lib_uart", "sim_regression", "parity", myenv,
                                        regexp=True)

    # Only want no parity @ 115200 baud for smoke tests
    if baud != 115200:
        tester.set_min_testlevel('nightly')
    if tester.test_required() != True:
        return

    xmostest.build(path, env = myenv, do_clean = True)

    xmostest.run_on_simulator(resources['xsim'],
        'app_uart_test_parity/bin/smoke/app_uart_test_parity_smoke.xe',
        simthreads = [checker],
        xscope_io=True,
        tester = tester)

def runtests():
    for baud in [14400, 57600, 115200, 230400]:
        do_test(baud, parity)