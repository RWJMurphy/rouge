from rouge.ui.urwid import UrwidUI

class UI(object):
    def __init__(self, game):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

    def invalidate(self):
        raise NotImplementedError()
