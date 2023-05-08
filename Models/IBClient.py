from Singleton import *
from ib_insync.ib import IB


class IBClient(metaclass=Singleton):
    def __init__(self, host="127.0.0.1", port=7497, client_id=123):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()

    def try_connect(self) -> [bool]:
        if not self.ib.isConnected():
            try:
                self.ib.connect(self.host, self.port, self.client_id, 60)
            except Exception as e:
                return [False, str(e)]
        return [True]
