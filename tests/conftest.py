# Copyright 2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import pytest
import Pyxsim
from Pyxsim import testers

param_dict = {
    "baud": "BAUD",
    "parity": "PARITY",
    "bits_per_byte": "BPB",
    "stopbits": "STOPBITS",
    "internal_clock": "INTERNAL_CLOCK"
}

@pytest.fixture(scope="function")
def do_test(request, capfd):
    params = request.node.callspec.params
    build_opts = []
    _capfd = capfd
    test_name = request.function.__name__
    test_vars_str = ""

    for k, v in param_dict.items():
        if k in params:
            build_opts.append(f"{param_dict[k]}={params[k]}")
            test_vars_str += f"{params[k]}_"

    test_vars_str = test_vars_str[:-1]  # remove trailing underscore
    bin_path = f"{test_name}/bin/{test_vars_str}/{test_name}_{test_vars_str}.xe"
    _expect_path = f"expect/{test_name}.expect"

    def run_xsim(simthreads=[], expect_path=_expect_path, sim_args=[], tester=None):
        # can pass as a single value
        if not isinstance(simthreads, list):
            simthreads = [simthreads]

        # if tester is none, use the expected file
        if tester == None:
            # remove empty lines as pyxsim does that for capfd
            file = open(expect_path)
            expected = [x.strip() for x in file.readlines()]
            expected = [x.strip() for x in expected if x != ""]
            tester = testers.ComparisonTester(expected, regexp=True)
        else:
            tester = tester

        assert Pyxsim.run_on_simulator(bin_path, simthreads=simthreads, tester=tester, 
                                    simargs=sim_args,capfd=_capfd, build_options=build_opts)

    return run_xsim
