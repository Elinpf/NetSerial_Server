from src.thread import Thread


class gloabl_variable():

    def __init__(self):
        # src.manager.Manger
        self.manager = None

        # src.mansion.Mansion
        self.mansion = None

        # manager threads
        self.thread = Thread()


gvar = gloabl_variable()
