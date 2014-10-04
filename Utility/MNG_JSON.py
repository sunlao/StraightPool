#!/usr/bin/python

import json

class MNG_JSON(object):

    def  __init__(self):
        import os

        v_cur_path  = os.path.dirname(os.path.abspath(__file__))
        self.__path = '%s/JSON' %(v_cur_path)

    def write_json(self,p_file_nm,p_dict):

        v_json_str  = json.dumps(p_dict)
        v_path  = "%s/%s.json"  %(self.__path,p_file_nm)
        with open(v_path,'w') as file_obj:
            file_obj.write(json.dumps(p_dict))

    def get_dict(self,p_file_nm):

        v_path  = "%s/%s.json"  %(self.__path,p_file_nm)
        with open(v_path,'r') as file_obj:
            v_json_str = file_obj.read()
        v_json_dict = json.loads(v_json_str)

        return v_json_dict
