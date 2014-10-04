#!/usr/bin/python

class MNG_Score(object):

    def __init__(self):
        from Utility.MNG_JSON       import MNG_JSON
        from Utility.Print_Control  import Print_Control
        from MNG_Player             import MNG_Player

        self.__json_obj             = MNG_JSON()
        self.__print_control_obj    = Print_Control()
        self.__mng_playr_obj        = MNG_Player()

    def updt_score_delta(self,p_game_dict,p_score_delta):
        v_msg = "There is a score difference of %s" %(p_score_delta)
        self.__print_control_obj.exe_print_msg(v_msg)
        v_player_up = p_game_dict['player_up']

        v_score_detla_amt_dict = self.get_score_detla_amt_dict(p_game_dict,p_score_delta)

        if v_player_up == 1:
            v_player1_balls_made = p_game_dict['player1_balls_made'] + v_score_detla_amt_dict['player_up_add_score']
            v_player2_balls_made = p_game_dict['player2_balls_made'] + v_score_detla_amt_dict['player_not_up_add_score']
        else:
            v_player1_balls_made = p_game_dict['player1_balls_made'] + v_score_detla_amt_dict['player_not_up_add_score']
            v_player2_balls_made = p_game_dict['player2_balls_made'] + v_score_detla_amt_dict['player_up_add_score']

        p_game_dict['player1_balls_made']=v_player1_balls_made
        p_game_dict['player2_balls_made']=v_player2_balls_made
        self.__json_obj.write_json('game',p_game_dict)

    def get_score_detla_amt_dict(self,p_game_dict,p_score_delta):
        v_player_up_nm              = self.__mng_playr_obj.get_player_up_nm(p_game_dict)
        v_player_not_up_nm          = self.__mng_playr_obj.get_player_not_up_nm(p_game_dict)

        v_chk_plyr_up_add_scrore = 0
        while v_chk_plyr_up_add_scrore == 0:
            v_input_str                 = "How many of %s points does %s get " %(p_score_delta,v_player_up_nm)
            v_player_up_add_score_res   = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
            try:
                v_player_up_add_score = int(v_player_up_add_score_res)
                if v_player_up_add_score >=0 and v_player_up_add_score <= p_score_delta:
                    v_msg = "Adding %s points to %s's score" %(v_player_up_add_score,v_player_up_nm)
                    self.__print_control_obj.exe_print_msg(v_msg)
                    v_player_not_up_add_score = p_score_delta - v_player_up_add_score
                    if v_player_not_up_add_score > 0:
                        v_input_str = "Add %s points %s's score correct? " %(v_player_not_up_add_score,v_player_not_up_nm)
                        v_add_flg   = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
                        if v_add_flg == "Y":
                            v_chk_plyr_up_add_scrore = 1
                        else:
                            v_msg = "Let's try again"
                            self.__print_control_obj.exe_print_msg(v_msg)
                    else:
                        v_chk_plyr_up_add_scrore = 1
                else:
                    v_msg = "Please enter a number between 0 and %s " %(p_score_delta)
                    self.__print_control_obj.exe_print_msg(v_msg)
            except ValueError:
                v_msg = "Please enter a number between 0 and %s " %(p_score_delta)
                self.__print_control_obj.exe_print_msg(v_msg)

        v_score_detla_amt_dict = {}
        v_score_detla_amt_dict['player_up_add_score']       = v_player_up_add_score
        v_score_detla_amt_dict['player_not_up_add_score']   = v_player_not_up_add_score

        return v_score_detla_amt_dict

    def add_foul(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm      = self.__mng_playr_obj.get_player_up_nm(p_game_dict)
        v_foul_flg = "?"
        while v_foul_flg == "?":
            v_input_str = "Did %s commit a foul? " %(v_player_up_nm)
            v_foul_res  = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
            if v_foul_res == "Y":
                if v_player_up == 1:
                    p_game_dict['player1_fouls'] = p_game_dict['player1_fouls'] + 1
                else:
                    p_game_dict['player2_fouls'] = p_game_dict['player2_fouls'] + 1
                v_foul_flg = v_foul_res
            elif v_foul_res == "N":
                v_foul_flg = v_foul_res
            else:
                v_msg = "Please enter a 'Y' or a 'N'"
                self.__print_control_obj.exe_print_msg(v_msg)
        self.__json_obj.write_json('game',p_game_dict)
