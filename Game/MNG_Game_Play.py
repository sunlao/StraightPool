#!/usr/bin/python

class MNG_Game_Play(object):

    def __init__(self):
        from Utility.MNG_JSON       import MNG_JSON
        from Init_Game              import Init_Game
        from Utility.Print_Control  import Print_Control
        from MNG_Player             import MNG_Player
        from MNG_Score              import MNG_Score

        self.__json_obj             = MNG_JSON()
        self.__init_game_obj        = Init_Game()
        self.__print_control_obj    = Print_Control()
        self.__mng_playr_obj        = MNG_Player()
        self.__mng_score_obj        = MNG_Score()

    def exe_game(self):
        try:
            v_game_dict = self.__json_obj.get_dict('game')
        except IOError:
            self.start_new_game()
        else:
            if  v_game_dict['game_status']=='over':
                self.start_new_game()
            else:
                v_chk_cont_game = "?"
                while v_chk_cont_game == "?":
                    v_input_str = "A game exists.  Would you like to continue? "
                    v_cont_game = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
                    if  v_cont_game == 'N':
                        v_msg = "Lets start a new game!"
                        self.__print_control_obj.exe_print_msg(v_msg)
                        self.start_new_game()
                        v_chk_cont_game = v_cont_game
                    elif v_cont_game == 'Y':
                        v_msg = "Last Game Loaded"
                        self.__print_control_obj.exe_print_msg(v_msg)
                        v_game_dict = self.__json_obj.get_dict('game')
                        self.chk_game_over(v_game_dict)
                        self.play_game(v_game_dict)
                        v_chk_cont_game = v_cont_game
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
        v_player_up_nm      = self.__mng_playr_obj.get_player_up_nm(p_game_dict)
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

        v_winner = "?"
        if v_player1_score >= v_score_end and v_player1_score > v_player2_score:
            v_winner = v_player_1_nm
        elif v_player2_score >= v_score_end and v_player2_score > v_player1_score:
            v_winner = v_player_2_nm
        if v_winner != "?":
            p_game_dict['game_status'] = "over"
            p_game_dict['winner'] = v_winner
            self.__json_obj.write_json('game',p_game_dict)
            v_msg = "Game is over"
            self.__print_control_obj.exe_print_msg(v_msg)
            v_msg = "%s is the Winner!" %(v_winner)
            self.__print_control_obj.exe_print_msg(v_msg)

        self.__print_control_obj.exe_print_msg(v_msg1)
        self.__print_control_obj.exe_print_msg(v_msg2)

    def chk_ball_count(self,p_game_dict):
        v_balls_on_table = p_game_dict['balls_on_table']

        v_chk_ball_count = "?"
        while v_chk_ball_count == "?":
            v_msg = "--There should be %s balls on the table" %(v_balls_on_table)
            self.__print_control_obj.exe_print_msg(v_msg)
            v_input_str = "Is this correct? "
            v_ball_count_qa = self.__print_control_obj.exe_print_msg_for_response(v_input_str).upper()
            if  v_ball_count_qa == "Y":
                v_chk_ball_count = v_ball_count_qa
            elif v_ball_count_qa == "N":
                self.updt_balls_on_table(p_game_dict,v_balls_on_table)
                v_chk_ball_count = v_ball_count_qa
            else:
                v_msg = "Please input a 'Y' or 'N'"
                self.__print_control_obj.exe_print_msg(v_msg)

    def updt_balls_on_table(self,p_game_dict,p_balls_on_table_at_turn_start):
        v_chk_balls_on_table = 0
        while v_chk_balls_on_table == 0:
            v_input_str = "How many balls are on table? "
            v_balls_on_table = self.__print_control_obj.exe_print_msg_for_response(v_input_str)

            try:
                v_balls_on_table = int(v_balls_on_table)
            except ValueError:
                v_msg = "Please enter a number between 1 and %s " %(p_balls_on_table)
                self.__print_control_obj.exe_print_msg(v_msg)

            if v_balls_on_table >= 1 and v_balls_on_table <= p_balls_on_table_at_turn_start:
                v_score_delta = p_balls_on_table_at_turn_start - v_balls_on_table
                if v_score_delta > 0:
                    self.__mng_score_obj.updt_score_delta(p_game_dict,v_score_delta)
                v_chk_balls_on_table = v_balls_on_table
            else:
                v_msg = "Please enter a number between 1 and %s " %(p_balls_on_table_at_turn_start)
                self.__print_control_obj.exe_print_msg(v_msg)

        p_game_dict['balls_on_table'] = v_balls_on_table
        self.__json_obj.write_json('game',p_game_dict)

    def post_end_turn(self,p_game_dict):
        v_player_up         = p_game_dict['player_up']
        v_player_up_nm      = self.__mng_playr_obj.get_player_up_nm(p_game_dict)
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
                self.__mng_score_obj.add_foul(p_game_dict)

                self.__json_obj.write_json('game',p_game_dict)
                self.updt_balls_on_table(p_game_dict,v_balls_on_table)
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
