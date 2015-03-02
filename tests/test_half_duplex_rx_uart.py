import xmostest
from uart_rx_checker import UARTRxChecker, Parity as RxParity
from uart_tx_checker import UARTTxChecker, Parity as TxParity


def do_test(baud):
    myenv = {'baud': baud}
    path = "app_uart_test_half_duplex_rx"
    resources = xmostest.request_resource("xsim")

    rx_checker = UARTRxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", RxParity['UART_PARITY_NONE'], baud, 4, 1, 8)
    # tx_checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1A", TxParity['UART_PARITY_NONE'], baud, 4, 1, 8)

    tester = xmostest.ComparisonTester(open('test_half_duplex_rx_uart.expect'),
                                       "lib_uart", "sim_regression", "half_duplex_tx_simple", myenv,
                                       regexp=True)

    # Only want no parity @ 230400 baud for smoke tests
    if baud != 115200:
        tester.set_min_testlevel('nightly')
    if not tester.test_required():
        return

    xmostest.build(path, env=myenv, do_clean=True)

    xmostest.run_on_simulator(resources['xsim'],
                              'app_uart_test_half_duplex_rx/bin/smoke/app_uart_test_half_duplex_rx_smoke.xe',
                              simthreads=[rx_checker],
                              xscope_io=True,
                              tester=tester,
                              simargs=["--vcd-tracing", "-tile tile[0] -ports -o trace.vcd"])


def runtests():
    for baud in [115200]:
        do_test(baud)
