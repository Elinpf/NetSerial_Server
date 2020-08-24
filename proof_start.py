import ptvsd
from src.manager import Manager
from src.mansion import Mansion

manager = Manager()
mansion = Mansion()

manager.mansion = mansion

manager.start_ssh_server()