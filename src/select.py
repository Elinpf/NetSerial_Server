from functools import wraps
import string


class Select():

    def __init__(self, rlist_keys, conn):
        self._rlist_keys = rlist_keys
        self._conn = conn

    def process(self):
        """
        ask terminal, select a room, and give a username
        """
        self.banner()
        recv_id = self.send_room_id_line()

        while not self.check_room_id(recv_id):
            self.error_msg('No Room, Please check the room id.')
            recv_id  = self.send_room_id_line()

        username = self.send_username_line()
        return (recv_id, username)
        

    def banner(self):
        self.send("************************\r\n")
        self.send("NetSerial by Elin\r\n")
        self.send("************************\r\n")

    def send(self, c):
        self._conn.send(c)

    def recv(self):
        return self._coon.recv_bytes()

    def send_room_id_line(self):
        self.send("room id: ")
        recv_id = self.recv_input()
        return recv_id

    def send_username_line(self):
        self.send("username: ")
        username = self.recv_input()
        return username

    def check_room_id(self, room_id):
        return room_id in self._rlist_keys

    def error_msg(self, msg):
        self.send("Get Error!\r\n")
        self.send("%s \r\n" % msg)
        self.send_line()

    def send_line(self):
        self.send("\r\n")

    def recv_input(self):
        """
        recv user input data, enter is end
        """
        _str = ""
        c = ""
        while True:
            c = self.recv()
            if c in (string.ascii_letters + string.digits):
                if len(_str) <= 10:  # max length is 10 char
                    self.send(c)  # echo
                    _str += c
            elif c == '\r':  # TODO: join back key
                break

        return _str
