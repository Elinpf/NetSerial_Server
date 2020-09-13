import string

class conf():

    # set ssh server username
    SSH_SERVER_USERNAME = 'bar'

    # set ssh server password
    SSH_SERVER_PASSWORD = 'foo'

    # set ssh server listening from client port
    SSH_SERVER_LISTENING_CLIENT_PORT = 2200

    # set ssh server listening from terminal port
    SSH_SERVER_LISTENING_TERMINIAL_PORT = SSH_SERVER_LISTENING_CLIENT_PORT + 100

    # set ssh server rsa key path
    SSH_SERVER_RSA_EKY = 'server_rsa'

    # set paramiko log path
    SSH_PARAMIKO_LOG_PATH = 'log/ssh_server.log'

    # set room id length
    ROOM_ID_LENGTH = 4

    # set room random string
    # ROOM_ID_STRING = string.ascii_lowercase + string.digits
    ROOM_ID_STRING = string.digits 