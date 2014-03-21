import traceback

import urwid

import rouge.ui

__all__ = ["UrwidUI"]

class UrwidUI(object):
    def __init__(self, game):
        self.main_loop = urwid.MainLoop(MainView(game), unhandled_input=self.exit_on_q)

    def exit_on_q(self, key):
        if key.lower() == "q":
            self.exit()

    def exit(self):
        raise urwid.ExitMainLoop()
    
    def run(self):
        self.main_loop.run()


class MainView(urwid.Pile):
    def __init__(self, game):
        super().__init__([
            urwid.Columns([
                urwid.LineBox(
                    urwid.Overlay(
                        MapWidget(game),
                        urwid.SolidFill(),
                        align='center',
                        width=('relative', 100),
                        valign='middle',
                        height='pack',
                        min_width=10,
                        min_height=10
                    ),
                    "Map"
                ),
                (20, urwid.LineBox(StatusWidget(game), "Status")),
            ]),
            (10, urwid.LineBox(MessageWidget(game), "Messages"))
        ])
        self.game = game
        self.focus_position = 0  # MapWidget


class MessageWidget(urwid.ListBox):
    log_levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'TRACE']
    def __init__(self, game):
        super().__init__(urwid.SimpleFocusListWalker([
            self._widget('INFO', "Welcome to {}!".format(game.name))
        ]))
        self.game = game

    def _widget(self, level, message):
        return urwid.Text(("LOG_" + level, message))

    def add(self, widget):
        self.body.insert(self.focus_position + 1, widget)

    def log(self, level, message):
        if level not in MessageWidget.log_levels:
            self.error("Log level {} not in {}".format(level, Messagewidget.log_levels))
            self.trace(traceback.format_tb())
            return False

        self.add(self._widget(level, message))

    def debug(self, message):
        self.log('DEBUG', message)

    def info(self, message):
        self.log('INFO', message)

    def warn(self, message):
        self.log('WARN', message)

    def error(self, message):
        self.log('ERROR', message)

    def trace(self, message):
        self.log('TRACE', message)



class StatusWidget(urwid.Pile):
    def __init__(self, game):
        super().__init__([])
        self.game = game


class MapWidget(urwid.Text):
    def __init__(self, game):
        super().__init__("@", "center")
        self.game = game

