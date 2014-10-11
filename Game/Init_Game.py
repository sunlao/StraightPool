#!/usr/bin/python

class Init_Game(object):

    def __init__(self):
        from Utility.Config         import Config
        from Utility.MNG_JSON       import MNG_JSON
        from Utility.Print_Control  import Print_Control

        config_obj                  = Config()
        self.__json_obj             = MNG_JSON()
        self.__print_control_obj    = Print_Control()
        self.__deflt_end_score      = config_obj.get_value('deflt_end_score')

    def init_game(self):
        v_player_1_nm       = self.get_player_1_nm()
        v_player_2_nm       = self.get_player_2_nm(v_player_1_nm)
        v_score_end         = self.get_score_end()
        v_score_fouls_true  = self.get_score_fouls_true()

        v_game_dict = {}
        v_game_dict['player_1_nm']          = v_player_1_nm
        v_game_dict['player_2_nm']          = v_player_2_nm
        v_game_dict['score_end']            = v_score_end
        v_game_dict['score_fouls_true']     = v_score_fouls_true
        v_game_dict['game_status']          = 'New'
        v_game_dict['inning_no']            = 1
        v_game_dict['player_up']            = 1
        v_game_dict['turn_stat']            = 'Up'
        v_game_dict['balls_on_table']       = 15
        v_game_dict['player1_balls_made']   = 0
        v_game_dict['player2_balls_made']   = 0
        v_game_dict['player1_fouls']        = 0
        v_game_dict['player2_fouls']        = 0

        self.__json_obj.write_json('game',v_game_dict)

    def get_player_1_nm(self):
        v_input_str     = "Input Player One's Name: "
        v_player_1_nm   = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
        if v_player_1_nm == "":
            v_player_1_nm = "Player One"
        else:
            v_player_1_nm = v_player_1_nm[0:29].title()

        return v_player_1_nm

    def get_player_2_nm(self,p_player_1_nm):
        v_input_str     = "Input Player Two's Name: "
        v_player_2_nm   = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
        if v_player_2_nm == "":
            v_player_2_nm = "Player Two"
        else:
            v_player_2_nm = v_player_2_nm[0:29].title()
        while v_player_2_nm == p_player_1_nm:
            v_input_str     = "Player Two's Name must be different than Player One's Name: "
            v_player_2_nm   = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
            if v_player_2_nm == "":
                v_player_2_nm = "Player Two"
            else:
                v_player_2_nm = v_player_2_nm[0:29].title()

        return v_player_2_nm

    def get_score_end(self):
        v_input_str = "What score are you playing to? "
        v_def_score_end = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
        if v_def_score_end == "":
            v_score_end = self.__deflt_end_score
        else:
            try:
                v_score_end = int(v_def_score_end)
            except ValueError:
                v_score_end = 0
            while v_score_end < 15 or v_score_end > 500:
                v_input_str         = "Please enter a number between 15 and 500: "
                v_chk_int_score_end = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
                try:
                    v_score_end = int(v_chk_int_score_end)
                except ValueError:
                    v_score_end = 0

        return v_score_end

    def get_score_fouls_true(self):
        v_score_fouls_true = "X"
        v_input_str = "Are we keeping track of fouls? "
        v_chk_score_fouls_true = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
        if v_chk_score_fouls_true == "":
            v_chk_score_fouls_true = "Y"
        v_chk_score_fouls_true = v_chk_score_fouls_true.upper()

        while v_score_fouls_true == "X":
            if  v_chk_score_fouls_true == "Y" or v_chk_score_fouls_true == "N":
                v_score_fouls_true = v_chk_score_fouls_true
            else:
                v_msg = "Please enter a Y or N to indicate if we are keeping track of fouls."
                self.__print_control_obj.exe_print_msg(v_msg)
                v_input_str = "Are we keeping track of fouls? "
                v_chk_score_fouls_true = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
                v_chk_score_fouls_true = v_chk_score_fouls_true.upper()

        return v_score_fouls_true
