import socket
import threading
from src.log import logger
from config import conf
from src.ssh import SSHServer
from src.connect import SSHConnection


class Manager():

    def __init__(self):
        self.mansion = None
        self.ssh_server_client: SSHServer = None
        self.ssh_server_terminal: SSHServer = None

    def get_ssh_connection(self, sock, port):
        conn = SSHConnection(sock)
        self.mansion.get_connection(conn, port)

    def start_ssh_server(self):
        self.create_ssh_server(self.ssh_server_client, conf.SSH_SERVER_LISTENING_CLIENT_PORT)
        self.create_ssh_server(self.ssh_server_terminal, conf.SSH_SERVER_LISTENING_TERMINIAL_PORT)

    def create_ssh_server(self, var, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("", port))
        try:
            listener.listen()
            logger.info('SSH.start listening port:%s  OK ...' % port)
        except:
            logger.error(
                'SSH.start listening port:%s Error, Exit...' % port)
        var = SSHServer()
        var.manager = self
        var.listener = listener
        var._port = port
        var.thread_run()



