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
        self.ssh_server_client = SSHServer()
        self.ssh_server_client.manager = self

        self.ssh_server_client.start_listening(
            conf.SSH_SERVER_LISTENING_CLIENT_PORT)
        self.ssh_server_client.thread_run()
