'''
Created on 23 Sep 2012

@author: Dave Wilson
'''
from employee_admin.model.common.obs_class_attr import ObsClassAttr, obs_any, \
    AUTO_TOPIC
from employee_admin.model.enum.dept_enum import DEPT_NONE_SELECTED

class UserVO(object):
    
    user_name = ObsClassAttr("user_name")
    first_name = ObsClassAttr("first_name")
    last_name = ObsClassAttr("last_name")
    email = ObsClassAttr("email")
    password = ObsClassAttr("password")
    is_valid = ObsClassAttr("is_valid")
    given_name = ObsClassAttr("given_name")

    def __init__(self, user_name="", first_name="", last_name="",
                 email="", password="", department=""):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.department = department or DEPT_NONE_SELECTED
        self.is_valid = False
        self.given_name = ""
        obs_any(self, self.any_changed)
        self.calc_given_name()
        self.calc_is_valid()
        
    def any_changed(self, value, topic=AUTO_TOPIC):#IGNORE:W0613
        topic = topic.getNameTuple()
        if topic[1] in ("first_name", "last_name"):
            self.calc_given_name()
        if topic[1] not in ("is_valid", "given_name"):
            self.calc_is_valid()
        
    def calc_is_valid(self):
        self.is_valid = all([self.user_name, self.password,
                              self.department != DEPT_NONE_SELECTED])
    
    def calc_given_name(self):
        self.given_name = "%s, %s" % (self.last_name, self.first_name)
