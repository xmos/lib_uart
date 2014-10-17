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

tester = xmostest.extract_test_results("lib_uart", "sim_regression")

xmostest.run_on_simulator(resources['xsim'],
                          'app_uart_test/bin/smoke/app_uart_test_smoke.xe',
                          xscope_io=True,
                          loopback=[{'from':'tile[0]:XS1_PORT_1A',
                                     'to':'tile[1]:XS1_PORT_1B'}],
                          tester = tester)

if xmostest.get_testrun_type() != 'smoke':
    xmostest.run_on_simulator(resources['xsim'],
                              'app_uart_test/bin/full/app_uart_test_full.xe',
                              xscope_io=True,
                              loopback=[{'from':'tile[0]:XS1_PORT_1A',
                                         'to':'tile[1]:XS1_PORT_1B'}],
                              tester = tester)
else:
    xmostest.note_skipped_tests()


xmostest.finish()
