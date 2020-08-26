from functools import wraps
import string
from src.log import logger


class Select():

    def __init__(self, rlist_keys, conn):
        self._rlist_keys = rlist_keys
        self._conn = conn

    def process(self):
        """
        ask terminal, select a room, and give a username
        """
        self.banner()
        recv_id = self.input_room_id()

        while not self.check_room_id(recv_id):
            self.error_msg('No Room, Please check the room id.')
            recv_id  = self.input_room_id()

        username = self.input_username()
        self.done_select_room()
        return (recv_id, username)
        

    def banner(self):
        self.send("************************\r\n")
        self.send("NetSerial by Elin\r\n")
        self.send("************************\r\n")
        self.send_line()

    def done_select_room(self):
        self.send_line()
        self.send('join the room, connection the remote console.\r\n')
        self.send('*'*80 +  '\r\n')
        self.send_line()


    def send(self, c):
        self._conn.send(c)

    def recv(self):
        return self._conn.recv_bytes()

    def input_room_id(self):
        return self.wait_input("room id: ")

    def input_username(self):
        return self.wait_input("username: ")

    def wait_input(self, msg):
        self.send(msg)
        return self.recv_input()

    def check_room_id(self, room_id):
        return room_id in self._rlist_keys

    def error_msg(self, msg):
        self.send("\r\n%s \r\n" % msg)
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
            c = self.recv().decode()  # to str
            if c in (string.ascii_letters + string.digits):
                if len(_str) <= 10:  # max length is 10 char
                    self.send(c)  # echo
                    _str += c
            elif c == '\r':  # TODO: join back key
                break
            
        logger.info('input room id -> %s' % _str)
        return _str
