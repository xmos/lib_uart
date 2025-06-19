# Copyright 2015-2025 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from Pyxsim import SimThread

class UARTClockDevice(SimThread):
    def __init__(self, clock_port, clock_frequency):
        """
        Create a clock input to a given port for the XCore.

        :param: clock_port        Port to clock
        :param: clock_frequency   Frequency in Hz of the clock
        """
        self._clock_port = clock_port
        self._clock_frequency = clock_frequency

    def run(self):
        xsi = self.xsi
        time = xsi.get_time()

        # (1s/(freq))/2 = T for 1 edge. 1s = 1e15fs, 0.5s = 5e14fs
        half_period_fs = float(5e14) / self._clock_frequency
        while True:
            xsi.drive_port_pins(self._clock_port, 1)
            self.wait_until(time + half_period_fs)
            time += half_period_fs

            xsi.drive_port_pins(self._clock_port, 0)
            self.wait_until(time + half_period_fs)
            time += half_period_fs
