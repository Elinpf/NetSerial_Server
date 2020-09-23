import threading
import paramiko
import socket
import select
from src.config import conf
from src.log import logger
from src.ssh import Server
from src.variable import gvar
from src.exceptions import SSHException


class Connection():

    def __init__(self, socket):
        self._socket = socket
        self._thread_stop = False
        self.address = None
        self.username = None

    def init_tcp(self):
        raise NotImplementedError

    def send(self):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

    def fileno(self):
        self._socket.fileno()

    def thread_stop(self):
        self._thread_stop = True

    def run(self):
        raise NotImplementedError

    def thread_run(self):
        self._thread_stop = False
        th = threading.Thread(target=self.run, name='connection run')
        th.start()
        gvar.thread.append(th)
        logger.info('thread start -> Connection.recv()')

    def close(self):
        raise NotImplementedError

    def notice_close(self):
        gvar.manager.close_connection(self)


class SSHConnection(Connection):

    def __init__(self, socket):
        super().__init__(socket)
        self._tp = None
        self._control = None  # src.control or src.channel
        self._channel: paramiko.channel.Channel = None

        self._thread_stop = False
        logger.info('establish a new ssh session.')

        self.init_tcp()

    def init_tcp(self):
        self._tp = paramiko.Transport(self._socket, gss_kex=True)
        self._tp.set_gss_host(socket.getfqdn(""))

        self._tp.load_server_moduli()

        host_key = paramiko.RSAKey(filename=conf.SSH_SERVER_RSA_EKY)
        self._tp.add_server_key(host_key)
        server = Server()
        logger.debug('Create Server Class')

        try:
            self._tp.start_server(server=server)
        except paramiko.SSHException:
            logger.error("SSH negotiation failed.")
            raise SSHException

        self._channel = self._tp.accept(200)

        if self._channel is None:
            logger.error('No channel')
            exit()

        logger.info('Authenticatied!')

    def send(self, msg):
        self._channel.send(msg)

    def recv(self):
        """
        threading
        """
        while not self._thread_stop:
            ready = select.select([self._channel], [], [], None)[0]

            if ready[0].closed:
                self.notice_close()

            if self._channel.recv_ready():
                c = self._channel.recv(50)
                if self._control:
                    self._control.notice(c)

    def recv_bytes(self):
        """
        get bytes one time
        """
        c = ""
        while not c:
            ready = select.select([self._channel], [], [], None)[0]

            if ready[0].closed:
                self.notice_close()

            if self._channel.recv_ready():
                c = self._channel.recv(50)

        return c

    def run(self):
        """
        alias self.recv()
        """
        self.recv()

    def in_room(self):
        """
        determine if this Connection is in a room
        """
        return self._control is not None

    def room_id(self):
        return self._control.room_id()

    def close(self):
        self.thread_stop()
        self._socket.close()

    def thread_stop(self):
        self._thread_stop = True
