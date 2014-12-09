#!/usr/bin/env python
import xmostest

xmostest.init()

xmostest.register_group("lib_uart",
                        "sim_regression",
                        "Uart Simulator Regression",
"""
Several tests are performed in simulation with a loopback between the UART Tx
and Rx ports. This tests the features of the individual components,
verifying them against each other. The various options and use cases of the
components are tested.
""")

xmostest.build("app_uart_test")

resources = xmostest.request_resource("xsim")

class UartTester(xmostest.Tester):

    def __init__(self):
        super(xmostest.Tester, self).__init__()
        self.register_test("lib_uart","sim_regression","loopback_test", {})

    def run(self, output):
        result = True
        for line in output:
            if line.find("FAIL") != -1:
                result = False
        xmostest.set_test_result("lib_uart", "sim_regression", "loopback_test",
                                 {}, result, output=''.join(output))



xmostest.run_on_simulator(resources['xsim'],
                          'app_uart_test/bin/smoke/app_uart_test_smoke.xe',
                          xscope_io=True,
                          loopback=[{'from':'tile[0]:XS1_PORT_1A',
                                     'to':'tile[1]:XS1_PORT_1B'}],
                          tester = UartTester())

xmostest.finish()
