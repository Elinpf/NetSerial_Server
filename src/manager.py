import socket
from src.log import logger
from src.config import conf
from src.ssh import SSHServer
from src.connect import SSHConnection


class Manager():

    def __init__(self):
        self.mansion = None
        self.ssh_servers = []

    def get_ssh_connection(self, sock, port):
        conn = SSHConnection(sock)
        self.mansion.get_connection(conn, port)

    def close_connection(self, conn):
        self.mansion.close_connection(conn)

    def start_ssh_server(self):
        self.create_ssh_server(conf.SSH_SERVER_LISTENING_CLIENT_PORT)
        self.create_ssh_server(conf.SSH_SERVER_LISTENING_TERMINIAL_PORT)

    def create_ssh_server(self, port):
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
        self.ssh_servers.append(var)

    def close_ssh_server(self):
        for s in self.ssh_servers:
            s.close()

    def close_mansion(self):
        self.mansion.close()

    def waiting_keyboard_interrupt(self):
        import time
        try:
            while True:
                time.sleep(100)

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        import sys
        logger.info('shutdown the programe.')
        self.close_ssh_server()
        self.close_mansion()
        logger.info('bye!')
        sys.exit(0)
