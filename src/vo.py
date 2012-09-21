"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import enum

class RoleVO(object):
    def __init__(self, user_name=None, roles=None):
        self.user_name = user_name
        self.roles = roles or []

class UserVO(object):
    def __init__(self, user_name=None, first_name=None, last_name=None,
                 email=None, password=None, department=None):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.department = department or enum.DEPT_NONE_SELECTED

    def is_valid(self):
        return all([self.user_name, self.password,
                    self.department != enum.DEPT_NONE_SELECTED]
                   )
    
    def given_name(self):
        return self.last_name + ', ' + self.first_name
