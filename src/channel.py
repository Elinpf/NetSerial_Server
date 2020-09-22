
class Channel():
    """
    this class channel with Client.
    """

    def __init__(self, room, conn):
        self._room = room
        self._conn = conn

    def notice(self, msg):
        """
        SSHConnction notice message, then notice room
        """
        self._room.recv_from_channel(msg)

    def send(self, msg):
        try:
            self._conn.send(msg)
        except AttributeError:
            raise OSError

    def close(self):
        self._conn.close()

    def room_id(self):
        return self._room.id

    def has_connection(self, conn):
        return self._conn is conn
