PARITY_NONE = None
DEFAULT_TIMEOUT = 1000
DEFAULT_BAUDRATE = 38400
DEFAULT_BYTESIZE = 8
DEFAULT_STOPBITS = 1

try:
    # if using pyBoard
    from pyb import UART as uart_base
except:
    from serial import Serial as uart_base

    PARITY_NONE = "N"
    DEFAULT_TIMEOUT = 1


class UART(object):
    def __init__(self):
        self.bus_name = uart_base.__name__
        self.bus = None
        self.map = {}

    def connection(self, port, baudrate=DEFAULT_BAUDRATE, bytesize=DEFAULT_BYTESIZE, parity=PARITY_NONE,
                   stopbits=DEFAULT_STOPBITS, timeout=DEFAULT_TIMEOUT):
        try:
            self.bus = uart_base(port, baudrate, bytesize, parity, stopbits, timeout)
            self._mapping()
        except Exception as err:
            print(err)
            # logging exception
            return None

        return self

    def __getattr__(self, item):
        def args_wrapper(*args, **kwargs):
            try:
                response = getattr(self.bus, item)(*args, **kwargs)
            except AttributeError:
                response = self._invoke_mapping(item, *args, **kwargs)
            return response

        return args_wrapper

    def _invoke_mapping(self, method, *args, **kwargs):
        try:
            item = self.map[self.bus_name][method]
            return getattr(self.bus, item)(*args, **kwargs) if item else None
        except KeyError:
            raise Exception("Unregistered method or attribute {}".format(method))

    def _mapping(self):
        self.map = {
            "UART": {
                "close": "deinit",
                "flushInput": "",
                "flushOutput": ""
            },
        }

