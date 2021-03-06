class Control():
    """
    this class connection with Terminial client
    """

    def __init__(self, room):
        self._clist = []
        self._room = room

    def append(self, conn):
        self._clist.append(conn)
        conn._control = self
        conn.thread_run()

    def notice(self, msg):
        self._room.recv_from_control(msg)

    def send(self, msg):
        for conn in self._clist:
            conn.send(msg)

    def close(self):
        try:
            for conn in self._clist:
                conn.close()
        except EOFError:
            pass

    def remove(self, conn):
        self._clist.remove(conn)
        conn.close()

    def room_id(self):
        return self._room.id
