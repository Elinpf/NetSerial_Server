import socket
import threading
import paramiko
from paramiko.py3compat import b, u, decodebytes

paramiko.util.log_to_file('proof_server.log')

host_key = paramiko.RSAKey(filename='server_rsa')

class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'bar') and (password == 'foo'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True
    
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


DoGSSAPIKkeyExchange = True

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 2200))

except Exception as e:
    print("Bind Error: " + str(e))
    exit()

try:
    sock.listen()
    print("Listening for connection ...")
    client, addr = sock.accept()
except Exception as e:
    print("Listening/ accept Error: " + str(e))

print("Got a connection")

t = paramiko.Transport(client, gss_kex=DoGSSAPIKkeyExchange)
t.set_gss_host(socket.getfqdn(""))

t.load_server_moduli()

t.add_server_key(host_key)
server = Server()

try:
    t.start_server(server=server)
except paramiko.SSHException:
    print("SSH negotiation failed.")
    exit()


chan = t.accept(20)
if chan is None:
    print("No channel")
    exit()
print("Authenticatied!")

server.event.wait(10)
if not server.event.is_set():
    print("Client never asked for a shell.")
    exit()

chan.send('Username: ')
# f = chan.makefile('rU')
# username = f.readline().strip("\r\n")
# chan.send('\r\nI Like you, ' + username + ".\r\n")
# chan.close()

while True:
    if chan.recv_ready():
        print(chan.recv(10))