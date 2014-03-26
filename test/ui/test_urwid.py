from nose.tools import *

import rouge

class TestUrwidUI():
    @classmethod
    def setup_class(cls):
        cls.urwid_ui = rouge.UrwidUI(rouge.Game('test/data/game/'))

    @classmethod
    def teardown_class(cls):
        pass

    def test_interface(self):
        for member in rouge.UI.__dict__:
            if member[0] != '_':
                yield self.check_interface_member, member

    def check_interface_member(self, member):
        assert_in(member, rouge.UrwidUI.__dict__.keys())

    def test_mw_init(self):
        assert_equal(self.urwid_ui.main_view.messages.body[0].text, "Welcome to Test game!")

    def test_message_order(self):
        add_message = self.urwid_ui.main_view.messages.add_message
        for x in range(10):
            add_message(str(x))
        
        self.test_mw_init()
        assert_equal(self.urwid_ui.main_view.messages.body[-1].text, str(x))
