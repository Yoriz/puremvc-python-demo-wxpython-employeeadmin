'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

from employee_admin.model.enum.dept_enum import DEPT_NONE_SELECTED

class UserVo(object):
    
    def __init__(self, user_name="", first_name="", last_name="",
                 email="", password="", department=""):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.department = department or DEPT_NONE_SELECTED

    @property    
    def is_valid(self):
        return all([self.user_name, self.password,
                                        self.department != DEPT_NONE_SELECTED])
    
    @property
    def given_name(self):
        return "%s, %s" % (self.last_name, self.first_name)
    
    def get_copy(self):
        return UserVo(self.user_name, self.first_name, self.last_name,
                      self.email, self.password, self.department)
