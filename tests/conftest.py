
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
    _build_opts = []
    _capfd = capfd
    for k, v in params.items():
        _build_opts.append(f"{param_dict[k]}={v}")

    def run_xsim(bin_path, expect_path=None, simthreads=[], sim_args=[], tester=None):
        # can pass as a single value
        if not isinstance(simthreads, list):
            simthreads = [simthreads]

        # can pass either a expect file and will use a ComparisonTester
        # or a custom tester object with a callable .run method
        if expect_path != None and tester == None:
            # remove empty lines as pyxsim does that for capfd
            file = open(expect_path)
            expected = [x.strip() for x in file.readlines()]
            expected = [x.strip() for x in expected if x != ""]
            tester = testers.ComparisonTester(expected, regexp=True)
        elif expect_path == None and tester != None:
            tester = tester
        else:
            assert 0, "need to pass either expected file path or the tester object"

        assert Pyxsim.run_on_simulator(bin_path, simthreads=simthreads, tester=tester, 
                                    simargs=sim_args,capfd=_capfd, build_options=_build_opts)

    return run_xsim
