import random
import time
from src.config import conf
from src.room import Room
from src.log import logger
from src.select import Select


class Mansion():

    def __init__(self):
        self._rlist = {}

    def create_room(self, conn):
        logger.info('createing a room...')
        while True:
            i = self.random_id()
            if self.check_id(i):
                break

        logger.info('random a room id -> %s', i)

        room = Room(i)
        room.channel = conn
        self._rlist[i] = room

    def del_room_by_id(self, i: int):
        room = self._rlist.pop(i)  # ! if not exist
        room.close()
        del room

    def del_room(self, room: Room):
        """
        Delete Room instance
        """
        i = room.id
        self.del_room_by_id(i)

    def get_channel_connection(self, conn):
        """
        get a client connection, create a room
        """
        logger.info('Got a client connection, create a room...')
        self.create_room(conn)

    def get_control_connection(self, conn):
        """
        get a terminal connection, select which room
        """
        logger.info('Got a terminal connection, select a room')
        self.select_room(conn)

    def get_connection(self, conn, port):
        if port == conf.SSH_SERVER_LISTENING_CLIENT_PORT:
            self.get_channel_connection(conn)

        elif port == conf.SSH_SERVER_LISTENING_TERMINIAL_PORT:
            self.get_control_connection(conn)

        else:
            logger.error('ssh listening port is not CONFIGURATION port')
            raise AttributeError

    def close_connection(self, conn):
        """
        close a connection
        """
        if not conn.in_room():  # if not in a room
            conn.close()
            return

        rid = conn.room_id()
        self._rlist[rid].close_connection(conn)

    def random_id(self):
        s = conf.ROOM_ID_STRING
        s = random.sample(s, conf.ROOM_ID_LENGTH)
        return ''.join(s)

    def check_id(self, i):
        return not(i in self._rlist.keys())

    def select_room(self, conn):
        """
        Enter a room, need select a room ID, and give a username
        """
        logger.info("into select room process...")
        se = Select(self._rlist.keys(), conn)
        room_id, username = se.process()

        logger.info('get room_id: %s, username: %s' % (room_id, username))
        room = self._rlist[room_id]
        conn.username = username
        room.add_connection(conn)
        del se

    def close(self):
        try:
            for (_, room) in self._rlist.items():
                room.close()
        except RuntimeError:
            logger.error("can't close room now, try again")
            time.sleep(0.2)
            self.close()
