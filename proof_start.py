import ptvsd
from src.variable import gvar
from src.manager import Manager
from src.mansion import Mansion

gvar.manager = Manager()
gvar.mansion = Mansion()

gvar.manager.mansion = gvar.mansion

gvar.manager.start_ssh_server()

gvar.manager.waiting_keyboard_interrupt()