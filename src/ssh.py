import socket
import threading
import select
import paramiko
from src.config import conf
from src.log import logger
from src.variable import gvar


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

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
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

            if self.listener._closed:
                return

            for _ in ready:  # establish new TCP session
                try:
                    _socket, addr = self.listener.accept()
                    if self.manager:
                        gvar.thread.function(
                            target=self.manager.get_ssh_connection, args=(_socket, self._port), name='Got a SSH Connection')
                except Exception as e:
                    logger.error('a bad socket %s ' % e)

    def thread_stop(self):
        self._thread_stop = True

    def thread_run(self):
        self._thread_stop = False
        th = threading.Thread(target=self.run, name="SSH Server Listening")
        th.start()
        gvar.thread.append(th)
        logger.info('thread start -> SSHServer.run()')

    def close(self):
        self.thread_stop()
        self.listener.close()
