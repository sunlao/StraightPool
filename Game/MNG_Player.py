#!/usr/bin/python

class MNG_Player(object):

    def get_player_up_nm(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm_key  = "player_%s_nm" %(v_player_up)
        v_player_up_nm      = p_game_dict[v_player_up_nm_key]

        return v_player_up_nm

    def get_player_not_up_nm(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        if  v_player_up == 1:
           v_player_not_up = 2
        else:
            v_player_not_up = 1
        v_player_not_up_nm_key      = "player_%s_nm" %(v_player_not_up)
        v_player_not_up_nm          = p_game_dict[v_player_not_up_nm_key]

        return v_player_not_up_nm
