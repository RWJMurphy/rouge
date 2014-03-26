import traceback

import urwid

import rouge.ui

__all__ = ["UrwidUI"]

class UrwidUI(object):
    def __init__(self, game):
        self.game = game
        self.main_view = MainView(game)
        self.main_loop = urwid.MainLoop(
            self.main_view,
            unhandled_input=self.game.keypress
        )

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            self.exit()

    def exit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self.main_loop.run()

class MainView(urwid.Pile):
    def __init__(self, game):
        self.map = MapWidget(game)
        self.status = StatusWidget(game)
        self.messages = MessageWidget(game)

        decorated_map = urwid.LineBox(
            urwid.Overlay(
                self.map,
                urwid.SolidFill(),
                align='center',
                width=('relative', 100),
                valign='middle',
                height=('relative', 100),
                min_width=10,
                min_height=10
            ),
            "Map"
        )
        decorated_status = urwid.LineBox(self.status, "Status")
        decorated_messages = urwid.LineBox(self.messages, "Messages")

        map_and_status = urwid.Columns([
            decorated_map,
            (20, decorated_status)
        ])
        map_and_status.focus_postition = 0  # Map

        super().__init__([
            map_and_status,
            (10, decorated_messages)
        ])
        self.game = game
        self.focus_position = 0  # Columns

class MessageWidget(urwid.ListBox):
    def __init__(self, game):
        super().__init__(urwid.SimpleFocusListWalker([
            self._widget("Welcome to {}!".format(game.config.name))
        ]))
        self.game = game

    def _widget(self, message, attr=None):
        if attr:
            widget = urwid.Text((attr, message))
        else:
            widget = urwid.Text(message)
        return widget

    def add_message(self, message, attr=None):
        self.body.insert(
            self.focus_position + 1,
            self._widget(message, attr)
        )


class StatusWidget(urwid.Pile):
    def __init__(self, game):
        super().__init__([])
        self.game = game


class MapWidget(urwid.Widget):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def render(self, size, focus=False):
        maxcol, maxrow = size
        midcol, midrow = maxcol//2, maxrow//2
        player_x, player_y = self.game.current_map.player_pos
        offset_x, offset_y = midcol - player_x, midrow - player_y

        rendermap = []
        for out_row in range(maxrow):
            the_row = []
            for out_col in range(maxcol):
                the_row.append(self.game.current_map.at(out_col - offset_x, out_row - offset_y).char)
            rendermap.append(the_row)

        rendermap[player_y + offset_y][player_x + offset_x] = b'@'
        rendermap = list(map(lambda row: b''.join(row), rendermap))
        canvas = urwid.TextCanvas(rendermap, maxcol=maxcol, check_width=True)
        return canvas
