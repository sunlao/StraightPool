#!/usr/bin/python

class Config(object):

    def __init__(self):
        from MNG_JSON       import MNG_JSON
        self.__json_obj     = MNG_JSON()

    def get_dict(self):
        v_dict = self.__json_obj.get_dict('config')

        return v_dict

    def post_config(self,p_key,p_value):
        if  self.get_value(p_key)!=p_value:
            v_dict = self.get_dict()
            v_dict[p_key]=p_value
            self.__json_obj.write_json('config',v_dict)

    def get_value(self,p_key):
        v_dict = self.get_dict()
        v_value = v_dict[p_key]

        return v_value
