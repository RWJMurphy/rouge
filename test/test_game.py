from nose.tools import *
import yaml

import rouge

class TestGame():
    @classmethod
    def setup_class(cls):
        cls.game = rouge.Game('test/data/game/')
        cls.game_config = yaml.load(open('test/data/game/game.yml', 'r').read())['game']

    @classmethod
    def teardown_class(cls):
        pass

    def test_name(self):
        assert_equal(self.game.name, self.game_config['name'])
