import xmostest
from uart_rx_checker import UARTRxChecker, Parity as RxParity
from uart_clock_device  import UARTClockDevice


def do_test(baud):
    myenv = {'baud': baud}
    path = "app_uart_test_multi_rx"
    resources = xmostest.request_resource("xsim")

    rx_checker = UARTRxChecker("tile[0]:XS1_PORT_8B.0", "tile[0]:XS1_PORT_1A", RxParity['UART_PARITY_NONE'], baud, 4, 1, 8, clear_multibit=True, multibit_port="tile[0]:XS1_PORT_8B")
    uart_clock = UARTClockDevice("tile[0]:XS1_PORT_1L", 1843200)

    tester = xmostest.ComparisonTester(open('test_rx_multi_uart.expect'),
                                       "lib_uart", "sim_regression", "multi_rx_simple", myenv,
                                       regexp=True)

    # Only want no parity @ 230400 baud for smoke tests
    if baud != 115200:
        tester.set_min_testlevel('nightly')

    xmostest.run_on_simulator(resources['xsim'],
                              'app_uart_test_multi_rx/bin/smoke/app_uart_test_multi_rx_smoke.xe',
                              simthreads=[rx_checker, uart_clock],
                              xscope_io=True,
                              tester=tester,
                              simargs=["--trace-to", "trace", "--vcd-tracing", "-tile tile[0] -pads -o trace.vcd"],
                              clean_before_build=True,
                              build_env=myenv)


def runtests():
    for baud in [57600, 115200]:
        do_test(baud)
