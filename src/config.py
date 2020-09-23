import string
import json
import os
import sys
from src.log import logger


class config():

    # set ssh server username
    SSH_SERVER_USERNAME = 'bar'

    # set ssh server password
    SSH_SERVER_PASSWORD = 'foo'

    # set ssh server listening from client port
    SSH_SERVER_LISTENING_CLIENT_PORT = 2200

    # set ssh server listening from terminal port
    SSH_SERVER_LISTENING_TERMINIAL_PORT = 2300

    # set ssh server rsa key path
    SSH_SERVER_RSA_EKY = 'server_rsa'

    # set paramiko log path
    SSH_PARAMIKO_LOG_PATH = 'log/ssh_server.log'

    # set room id length
    ROOM_ID_LENGTH = 4

    # set room random string
    # ROOM_ID_STRING = string.ascii_lowercase + string.digits
    ROOM_ID_STRING = string.digits

    def _get_variables(self):
        return [c for c in dir(self) if c[0] != '_']

    def _upgrade(self, custom: str):
        local_var = self._get_variables()

        local_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        json_path = os.path.join(local_dir, custom)
        if not os.path.exists(json_path):
            return

        with open(json_path) as f:
            j_var = json.load(f)
            logger.info('loading custom configuration....')

        for (key, val) in j_var.items():
            if not key in local_var:
                continue

            self.__dict__[key] = val

        logger.info('loading done')
        return self


conf = config()
conf._upgrade('custom.json')
