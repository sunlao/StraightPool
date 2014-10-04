#!/usr/bin/python

import  os
import  sys
from    Game.MNG_Game_Play   import MNG_Game_Play

v_app_path      = os.path.dirname(os.path.abspath(__file__))
sys.path.append(v_app_path)

game_play_obj   = MNG_Game_Play()

game_play_obj.exe_game()
