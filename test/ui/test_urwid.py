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
        for x in rouge.UI.__dict__:
            yield self.check_interface_member, x

    def check_interface_member(self, member):
        assert_in(member, rouge.UrwidUI.__dict__.keys())
