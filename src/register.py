from src.exceptions import StructError
from src.protocol import Protocol
from src.log import logger
from src.config import conf


class Register():
    """
    base first code is 0x1
    second code blow:
    |0x0| => request
    |0x1| => room id
    |0x2| => fin room id
    |0xe| => ERROR ROOM ID
    |0xf| => ERROR

    status:
    0x0 : init
    0x1 : get a request
    0x2 : wait room id
    0x4 : full
    """

    INIT_STATUS = 0x1
    WAIT_ROOM_ID_STATUS = 0x2
    FULL_STATUS = 0x4

    def __init__(self, room):
        self._room = room
        self.status = self.INIT_STATUS

    def recv(self, msg):
        try:
            r = Protocol(msg)
            head = r.get_int8()
            if head != 0x1:
                return

            code = r.get_int8()
            if code == 0x0:
                self.get_request()

            elif code == 0x2:
                self.get_fin_room_id(r)

            elif code == 0xe:
                logger.error('Bad Room ID')
                self.send_error()

            elif code == 0xf:
                self.send_error()

            else:
                self.send_error()
        except StructError:
            self.send_error()

    def get_request(self):
        if not self.status == self.INIT_STATUS:
            self.send_error()
            return

        else:
            self.send_room_id()

    def get_fin_room_id(self, pro: Protocol):
        if not self.status == self.WAIT_ROOM_ID_STATUS:
            self.send_error()
            return

        room_id = pro.get_str()
        if not self._room.id == room_id:
            self.send_error()
            return
        self.status = self.FULL_STATUS
        logger.debug('Register: Full Status')

    def send_room_id(self):
        """
        | 0x1 | room_id | server terminal listening port |
        """
        bs = self.get_protocol_head(0x1)
        bs.add_str(self._room.id)
        bs.add_str(str(conf.SSH_SERVER_LISTENING_TERMINIAL_PORT))
        self.send(bs)
        self.status = self.WAIT_ROOM_ID_STATUS
        logger.debug('Register: send room id: %s' % bs.get_packet())

    def send_error(self):
        """
        if get error, then send error
        """
        bs = self.get_protocol_head(0xf)
        self.send(bs)
        self.status = self.INIT_STATUS
        logger.error('Register Get an Error')

    def get_protocol_head(self, code: int):
        bs = Protocol()
        bs.add_int8(0x1)
        bs.add_int8(code)
        return bs

    def send(self, bs: Protocol):
        msg = bs.get_packet()
        self._room.send_to_channel(msg)

    def is_full(self):
        return (self.status == self.FULL_STATUS)
