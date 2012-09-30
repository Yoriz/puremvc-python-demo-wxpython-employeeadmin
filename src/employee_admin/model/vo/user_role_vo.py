'''
Created on 23 Sep 2012

@author: Dave Wilson
'''


class UserRoleVo(object):
    
    def __init__(self, user_name=None, roles=None):
        self.user_name = user_name
        self.roles = roles or []
        
    def get_copy(self):
        return UserRoleVo(self.user_name, self.roles)
