'''
Created on 23 Sep 2012

@author: Dave Wilson
'''
from employee_admin.model.common.obs_class_attr import ObsClassAttr

class RoleVO(object):
    
    user_name = ObsClassAttr("user_name")
    roles = ObsClassAttr("roles")
    
    def __init__(self, user_name=None, roles=None):
        self.user_name = user_name
        self.roles = roles or []