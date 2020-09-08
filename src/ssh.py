import socket
import threading
import select
import paramiko
from paramiko.py3compat import b, u, decodebytes
from config import conf
from src.log import logger


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == conf.SSH_SERVER_USERNAME) and (password == conf.SSH_SERVER_PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True


class SSHServer():

    def __init__(self):
        self.listener: socket.socket = None
        self._thread_stop = False
        self._port = None
        self.manager = None

    def start_listening(self, port):
        self._port = port
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(("", self._port))

        try:
            self.listener.listen()
            logger.info('SSH.start listening port:%s  OK ...' % self._port)
        except:
            logger.error(
                'SSH.start listening port:%s Error, Exit...' % self._port)

    def run(self):
        while not self._thread_stop:
            ready = select.select([self.listener], [], [], None)[0]

            if self.listener._closed: return

            for _ in ready:  # establish new TCP session
                try:
                    _socket, addr = self.listener.accept()
                except Exception as e:
                    logger.error('a bad socket %s ' % e)

                if self.manager:
                    self.manager.get_ssh_connection(_socket, self._port)

    def thread_stop(self):
        self._thread_stop = True

    def thread_run(self):
        self._thread_stop = False
        th = threading.Thread(target=self.run, name="SSH Server Listening")
        th.start()
        logger.info('thread start -> SSHServer.run()')

    def close(self):
        self.thread_stop()
        self.listener.close()
