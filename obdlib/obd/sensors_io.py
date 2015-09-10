from obdlib.logging import logger
from obdlib.utils import bitwise_pids


class CommandIO(object):
    __slots__ = ['__call']

    def __init__(self, call_obd):
        self.__call = call_obd

    def check_pids(self):
        pids = self["01"]("00")  # 01 00
        if hasattr(pids, '__iter__') and len(pids):
            pids = bitwise_pids(pids.pop()).values()
            return True if True in pids else False

    def __getitem__(self, mode):
        def get_pid(pid='00'):
            response = None
            try:
                response = self.__call(mode + pid).raw_value
            except Exception as err:
                # logging
                logger.error(err)
            return response

        return get_pid
