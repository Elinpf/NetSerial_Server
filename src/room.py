from src.control import Control
from src.register import Register
from src.channel import Channel

class Room():

    def __init__(self, _id):
        self._channel:Channel = None
        self._control = Control(self)
        self.register = Register(self)
        self.id = _id

    def channel(self, conn):
        self._channel = Channel(self, conn)
        conn._control = self._channel  # this is Connection control
        conn.thread_run()

    channel = property(None, channel)

    def add_connection(self, conn):
        self._control.append(conn)

    def recv_from_control(self, msg):
        """
        recv from control, then send to channel
        """
        self.send_to_channel(msg)

    def recv_from_channel(self, msg):
        """
        recv from channel, then send to control
        if register status is not full, then send to register
        """
        if not self.register.is_full:
            self.register.recv(msg)
        else:
            self.send_to_control(msg)

    def send_to_control(self, msg):
        self._control.send(msg)

    def send_to_channel(self, msg):
        self._channel.send(msg)

    def close(self):
        """
        Close all connection in the Room
        """
        self._channel.close()
        self._control.close()
