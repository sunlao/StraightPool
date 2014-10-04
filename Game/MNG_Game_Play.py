#!/usr/bin/python

class MNG_Game_Play(object):

    def __init__(self):
        from Utility.MNG_JSON       import MNG_JSON
        from Init_Game              import Init_Game
        from Utility.Print_Control  import Print_Control

        self.__json_obj             = MNG_JSON()
        self.__init_game_obj        = Init_Game()
        self.__print_control_obj    = Print_Control()

    def exe_game(self):
        try:
            v_game_dict = self.__json_obj.get_dict('game')
        except IOError:
            self.start_new_game()
        else:
            if  v_game_dict['game_status']=='over':
                self.start_new_game()
            else:
                v_game_cont_flg = "?"
                while v_game_cont_flg == "?":
                    v_input_str = "A game exists.  Would you like to continue? (Y/N) "
                    v_cont_game = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
                    if  v_cont_game == 'N':
                        v_msg = "Lets start a new game!"
                        self.__print_control_obj.exe_print_msg(v_msg)
                        self.start_new_game()
                        v_game_cont_flg = v_cont_game
                    elif v_cont_game == 'Y':
                        v_msg = "Last Game Loaded"
                        self.__print_control_obj.exe_print_msg(v_msg)
                        v_game_dict = self.__json_obj.get_dict('game')
                        self.chk_game_over(v_game_dict)
                        self.play_game(v_game_dict)
                        v_game_cont_flg = v_cont_game
                    else:
                        v_msg = "Please enter a 'Y' to load previous game or a 'N' to start a new game"
                        self.__print_control_obj.exe_print_msg(v_msg)

    def start_new_game(self):
        self.__init_game_obj.init_game()
        v_game_dict = self.__json_obj.get_dict('game')
        v_game_dict['game_status'] = 'play'
        self.__json_obj.write_json('game',v_game_dict)
        self.play_game(v_game_dict)

    def play_game(self,p_game_dict):
        v_game_status   = p_game_dict['game_status']
        while v_game_status != 'over':
            self.show_game_status(p_game_dict)
            self.post_end_turn(p_game_dict)
            self.chk_game_over(p_game_dict)
            v_game_status = p_game_dict['game_status']

    def show_game_status(self,p_game_dict):
        v_game_status   = p_game_dict['game_status']
        if v_game_status != 'over':
            v_player_up_nm      = self.get_player_up_nm(p_game_dict)
            v_turn_stat     = p_game_dict['turn_stat']
            v_msg = "--%s's turn is %s" %(v_player_up_nm,v_turn_stat)
            self.__print_control_obj.exe_print_msg(v_msg)
            v_inning_no = p_game_dict['inning_no']
            v_msg = "--It is inning number %s" %(v_inning_no)
            self.__print_control_obj.exe_print_msg(v_msg)
            self.chk_ball_count(p_game_dict)


    def chk_game_over(self,p_game_dict):
        v_player_1_nm           = p_game_dict['player_1_nm']
        v_player_2_nm           = p_game_dict['player_2_nm']
        v_player1_balls_made    = p_game_dict['player1_balls_made']
        v_player2_balls_made    = p_game_dict['player2_balls_made']
        v_player1_fouls         = p_game_dict['player1_fouls']
        v_player2_fouls         = p_game_dict['player2_fouls']
        v_score_fouls_true      = p_game_dict['score_fouls_true']
        v_score_end             = p_game_dict['score_end']

        if v_score_fouls_true == "Y":
            v_player1_score = v_player1_balls_made - v_player1_fouls
            v_player2_score = v_player2_balls_made - v_player2_fouls
            v_msg1 = "**%s's has made %s balls and has committed %s fouls and has a score of %s" %(v_player_1_nm,v_player1_balls_made,v_player1_fouls,v_player1_score)
            v_msg2 = "**%s's has made %s balls and has committed %s fouls and has a score of %s" %(v_player_2_nm,v_player2_balls_made,v_player2_fouls,v_player2_score)
        else:
            v_player1_score = v_player1_balls_made
            v_player2_score = v_player2_balls_made
            v_msg1 = "**%s's has made %s balls has a score of %s" %(v_player_1_nm,v_player1_balls_made,v_player1_score)
            v_msg2 = "**%s's has made %s balls has a score of %s" %(v_player_2_nm,v_player2_balls_made,v_player2_score)

        if v_player1_score >= v_score_end or v_player2_score >= v_score_end:
            p_game_dict['game_status'] = "over"
            self.__json_obj.write_json('game',p_game_dict)
            v_msg = "Game is over"
            self.__print_control_obj.exe_print_msg(v_msg)

        self.__print_control_obj.exe_print_msg(v_msg1)
        self.__print_control_obj.exe_print_msg(v_msg2)

    def chk_ball_count(self,p_game_dict):
        v_balls_on_table = p_game_dict['balls_on_table']

        v_chk_ball_count_flg = "?"
        while v_chk_ball_count_flg == "?":
            v_msg = "--There should be %s balls on the table" %(v_balls_on_table)
            self.__print_control_obj.exe_print_msg(v_msg)
            v_input_str = "Is this correct? "
            v_chk_ball_res = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
            if  v_chk_ball_res == "Y":
                v_chk_ball_count_flg = v_chk_ball_res
            elif v_chk_ball_res == "N":
                self.post_balls_on_table(p_game_dict,v_balls_on_table)
                v_chk_ball_count_flg = v_chk_ball_res
            else:
                v_msg = "Please input a 'Y' or 'N'"
                self.__print_control_obj.exe_print_msg(v_msg)

    def post_balls_on_table(self,p_game_dict,p_balls_on_table):
        v_balls_on_table = 0
        while v_balls_on_table == 0:
            v_input_str = "How many balls are on table? "
            v_balls_on_table_res = self.__print_control_obj.exe_print_msg_for_response(v_input_str)

            try:
                v_balls_on_table_res = int(v_balls_on_table_res)
            except ValueError:
                v_msg = "Please enter a number between 1 and %s " %(p_balls_on_table)
                self.__print_control_obj.exe_print_msg(v_msg)

            if v_balls_on_table_res >= 1 and v_balls_on_table_res <= p_balls_on_table:
                v_score_delta = p_balls_on_table - v_balls_on_table_res
                if v_score_delta > 0:
                    self.post_score_delta(p_game_dict,v_score_delta)
                v_balls_on_table = v_balls_on_table_res
            else:
                v_msg = "Please enter a number between 1 and %s " %(p_balls_on_table)
                self.__print_control_obj.exe_print_msg(v_msg)

        p_game_dict['balls_on_table'] = v_balls_on_table
        self.__json_obj.write_json('game',p_game_dict)


    def post_score_delta(self,p_game_dict,p_score_delta):
        v_msg = "There is a score difference of %s" %(p_score_delta)
        self.__print_control_obj.exe_print_msg(v_msg)
        v_player_up         = p_game_dict['player_up']
        if  v_player_up == 1:
           v_player_not_up = 2
        else:
            v_player_not_up = 1
        v_player_up_nm              = self.get_player_up_nm(p_game_dict)
        v_player_not_up_nm_key      = "player_%s_nm" %(v_player_not_up)
        v_player_not_up_nm          = p_game_dict[v_player_not_up_nm_key]
        v_input_qa1 = 0
        while v_input_qa1 == 0:
            v_input_str                 = "How many of %s points does %s get " %(p_score_delta,v_player_up_nm)
            v_pre_player_up_add_score   = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
            try:
                v_player_up_add_score = int(v_pre_player_up_add_score)
                if v_player_up_add_score >=0 and v_player_up_add_score <= p_score_delta:
                    v_msg = "Adding %s points to %s's score" %(v_player_up_add_score,v_player_up_nm)
                    self.__print_control_obj.exe_print_msg(v_msg)
                    v_new_score_delta = p_score_delta - v_player_up_add_score
                    if v_new_score_delta > 0:
                        v_input_str = "Add %s points %s's score correct? " %(v_new_score_delta,v_player_not_up_nm)
                        v_add_flg   = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
                        if v_add_flg == "Y":
                            v_input_qa1 = 1
                    else:
                        v_input_qa1 = 1
                else:
                    v_msg = "Please enter a number between 0 and %s " %(p_score_delta)
                    self.__print_control_obj.exe_print_msg(v_msg)
            except ValueError:
                v_msg = "Please enter a number between 0 and %s " %(p_score_delta)
                self.__print_control_obj.exe_print_msg(v_msg)

        if v_player_up == 1:
            v_player1_balls_made = p_game_dict['player1_balls_made'] + v_player_up_add_score
            v_player2_balls_made = p_game_dict['player2_balls_made'] + v_new_score_delta
        else:
            v_player1_balls_made = p_game_dict['player1_balls_made'] + v_new_score_delta
            v_player2_balls_made = p_game_dict['player2_balls_made'] + v_player_up_add_score

        p_game_dict['player1_balls_made']=v_player1_balls_made
        p_game_dict['player2_balls_made']=v_player2_balls_made
        self.__json_obj.write_json('game',p_game_dict)

    def post_end_turn(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm      = self.get_player_up_nm(p_game_dict)
        v_balls_on_table    = p_game_dict['balls_on_table']
        v_end_turn_flg      = "N"
        while v_end_turn_flg == "N":
            v_input_str     = "Is %s's turn over? " %(v_player_up_nm)
            v_end_turn_res  = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
            if v_end_turn_res == "Y":
                p_game_dict['turn_stat'] = 'Done'
                v_run_rack_flg = "?"
                while v_run_rack_flg == "?":
                    v_input_str = "Did %s run a rack? " %(v_player_up_nm)
                    v_rack_res  = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
                    if v_rack_res == "Y":
                        v_run_rack_count_flg = "?"
                        while v_run_rack_count_flg == "?":
                            v_input_str = "How many racks did %s run? " %(v_player_up_nm)
                            v_rack_count_res  = self.__print_control_obj.exe_print_msg_for_response(v_input_str)
                            try:
                                v_rack_count_res = int(v_rack_count_res)
                                if v_rack_count_res > 0:
                                    v_run_rack_count_flg = v_rack_count_res
                                else:
                                    v_msg = "Please enter a number greater than 0"
                                    self.__print_control_obj.exe_print_msg(v_msg)
                            except ValueError:
                                v_msg = "Please enter the number of racks %s ran" %(v_player_up_nm)
                                self.__print_control_obj.exe_print_msg(v_msg)
                        if v_rack_count_res == 1:
                            if v_player_up == 1:
                                p_game_dict['player1_balls_made'] = p_game_dict['player1_balls_made'] + (v_balls_on_table -1)
                            else:
                                p_game_dict['player2_balls_made'] = p_game_dict['player2_balls_made'] + (v_balls_on_table -1)
                        elif v_rack_count_res > 1:
                            if v_player_up == 1:
                                p_game_dict['player1_balls_made'] = p_game_dict['player1_balls_made'] + (v_balls_on_table -1)+(14*(v_rack_count_res-1))
                            else:
                                p_game_dict['player2_balls_made'] = p_game_dict['player2_balls_made'] + (v_balls_on_table -1)+(14*(v_rack_count_res-1))
                        v_run_rack_flg = v_rack_res
                        v_balls_on_table = 15
                    elif v_rack_res == "N":
                        v_run_rack_flg = v_rack_res
                    else:
                        v_msg = "Please enter a 'Y' or a 'N'"
                        self.__print_control_obj.exe_print_msg(v_msg)
                self.post_foul(p_game_dict)

                self.__json_obj.write_json('game',p_game_dict)
                self.post_balls_on_table(p_game_dict,v_balls_on_table)
                v_end_turn_flg = v_end_turn_res
            else:
                v_msg = "Please enter a 'Y' when %s's turn is over" %(v_player_up_nm)
                self.__print_control_obj.exe_print_msg(v_msg)
        if v_player_up == 1:
            p_game_dict['player_up'] = 2
        else:
            v_inning_no = p_game_dict['inning_no']
            p_game_dict['inning_no'] = v_inning_no +1
            p_game_dict['player_up'] = 1
        p_game_dict['turn_stat'] = "Up"
        self.__json_obj.write_json('game',p_game_dict)

    def post_foul(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm      = self.get_player_up_nm(p_game_dict)
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

    def get_player_up_nm(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm_key  = "player_%s_nm" %(v_player_up)
        v_player_up_nm      = p_game_dict[v_player_up_nm_key]

        return v_player_up_nm
