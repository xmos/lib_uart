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
output = xmostest.run_on_simulator(resources['xsim'],
                                   'app_uart_test/bin/app_uart_test.xe',
                                   xscope_io=True,
                                   loopback=[{'from':'tile[0]:XS1_PORT_1A',
                                              'to':'tile[1]:XS1_PORT_1B'}])

xmostest.interpret_results(output, product = "lib_uart", group = "sim_regression")

xmostest.finish()
