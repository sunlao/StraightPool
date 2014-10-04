#!/usr/bin/pythponse(self,p_msg):

class Print_Control(object):

    def __init__(self):
        from Utility.Config     import Config
        from Utility.MNG_JSON   import MNG_JSON

        config_obj              = Config()
        self.__json_obj         = MNG_JSON()
        self.__print_screen_typ = config_obj.get_value('print_screen_typ')

    def exe_print_msg(self,p_msg):
        if      self.__print_screen_typ == "C":
            print p_msg
        elif    self.__print_screen_typ == "W":
            self.print_to_web(p_msg)

    def exe_print_msg_for_response(self,p_msg):
        if      self.__print_screen_typ == "C":
            v_res = self.print_to_console_for_response(p_msg)
        elif    self.__print_screen_typ == "W":
            v_res = self.print_to_web_for_response(p_msg)

        return v_res

    def print_to_console_for_response(self,p_msg):
        v_res = raw_input(p_msg)

        return v_res

    def print_to_web(self,p_msg):
        v_res = "Define"

        return v_res
