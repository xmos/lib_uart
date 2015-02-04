import xmostest
from array import array

Parity = dict(
    UART_PARITY_EVEN = 0,
    UART_PARITY_ODD  = 1,
    UART_PARITY_NONE = 2,
)

class UARTTxChecker(xmostest.SimThread):
    """
    This simulator thread will act as a UART device, and will check sent and 
    transations caused by the device, by looking at the tx pins.
    """

    def __init__(self, rx_port, tx_port, parity, baud, length, stop_bits, bpb):
        self._rx_port           = rx_port
        self._tx_port           = tx_port
        self._parity            = parity
        self._baud              = baud
        self._timed_transitions = []
        self._length            = length
        self._stop_bits         = stop_bits
        self._bits_per_byte     = bpb
        # Hex value of stop bits, as MSB 1st char, e.g. 0b11 : 0xC0


    def get_port_val(self, xsi, port):
        "Sample port, modelling the pull up"
        is_driving = xsi.is_port_driving(port)
        if not is_driving:
            return 1
        else:
            return xsi.sample_port_pins(port);

    def get_bit_time(self):
        "Time per bit is 1/baud"
        # Return float value in ns
        return (1.0/self._baud) * 1e9

    def wait_baud_time(self, xsi):
        self.wait_until(xsi.get_time() + self.get_bit_time())
        return True

    def wait_half_baud_time(self, xsi):
        self.wait_until(xsi.get_time() + (self.get_bit_time() / 2))


    def read_packet(self, xsi, parity, length = 4):
        packet = []
        start_time = 0
        got_start_bit = False
        for x in range(length):
            packet.append(chr(self.read_byte(xsi, parity)))
        return packet

    def read_byte(self, xsi, parity):
        byte = 0
        val = 0

        # Recv start bit
        print "tx starts high: %s" % ("True" if self.get_port_val(xsi, self._tx_port) else "False")
        self.wait_for_port_pins_change([self._tx_port])

        # The tx line should go low for 1 bit time
        if self.get_val_timeout(xsi, self._tx_port) == 0: 
            print "Start bit recv'd"
        else:
            return False

        # This should be the 1st byte?!?
        self.get_val_timeout(xsi, self._tx_port)
        
        # recv the byte
        crc_sum = 0
        for j in range(self._bits_per_byte):
            val = self.get_val_timeout(xsi, self._tx_port)
            # print val
            byte += (val << (j))
            crc_sum += val

        # Check the parity if needs be
        self.check_parity(xsi, crc_sum, parity)

        # Get the stop bit
        self.check_stopbit(xsi)

        # Print a new line to split bytes in output
        print ""

        return byte

    def check_parity(self, xsi, crc_sum, parity):
        if parity < 2:
            if self.get_val_timeout(xsi, self._tx_port) == (crc_sum + parity) % 2:
                print "Parity bit correct"
            else:
                print "Parity bit incorrect"
        else:
            print "Parity bit correct"
    
    # TODO: Look at self._stop_bits
    def check_stopbit(self, xsi):
        print "tx ends high: %s" % ("True" if (self.get_port_val(xsi, self._tx_port)) else "False")

    def get_val_timeout(self, xsi, port):
        timeout = self.get_bit_time() * 0.99
        short_timeout = self.get_bit_time() * 0.005

        # Allow for rise time
        self.wait_until(xsi.get_time() + short_timeout)

        # Get val
        K = self.wait_time_or_pin_change(xsi, timeout, port)


        # Allow for rise time
        self.wait_until(xsi.get_time() + short_timeout)
        return K

    def wait_time_or_pin_change(self, xsi, timeout, port):
        start_time = xsi.get_time()
        start_val  = self.get_port_val(xsi, port)
        transitioned_during_wait = False

        def _continue(_timeout, _start_time, _start_val):
            if(xsi.get_time() >= _start_time + _timeout):
                return True
            if(self.get_port_val(xsi, port) != _start_val):
                transitioned_during_wait = True
                return True
            return False
        wait_fun = (lambda x: _continue(timeout, start_time, start_val))
        self.wait(wait_fun)

        # Start value should *not* have changed during timeout
        if transitioned_during_wait:
            print "FAIL :: Unexpected Transition."

        return start_val



    def run(self):
        # Wait for the xcore to bring the uart tx port up
        self.wait((lambda x: True if self.xsi.is_port_driving(self._tx_port) else False))

        K = self.read_packet(self.xsi, self._parity, self._length)

        # Print each member of K as a hex byte
        # inline lambda function mapped over a list? awh yiss.
        print ", ".join(map((lambda x: "0x%02x" % ord(x)), K))
