#!/usr/bin/env python
import cgitb
import sys
sys.path.insert(0, './lib')

import rouge

def main():
    game = rouge.Game('data/game/')
    game.run()

def handle_exception(exc_type, exc_value, trace):
    cgitb.Hook(format="text")(exc_type, exc_value, trace)

if __name__ == "__main__":
    sys.excepthook = handle_exception
    main()
