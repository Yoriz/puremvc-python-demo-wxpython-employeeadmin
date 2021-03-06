"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import enum
import vo
import main
import puremvc.patterns.proxy

class UserProxy(puremvc.patterns.proxy.Proxy):
    
    NAME = "UserProxy"
    def __init__(self):
        super(UserProxy, self).__init__(UserProxy.NAME, [])
        self.data = []
        self.addItem(vo.UserVO('lstooge', 'Larry', 'Stooge', "larry@stooges.com", 'ijk456', enum.DEPT_ACCT))
        self.addItem(vo.UserVO('cstooge', 'Curly', 'Stooge', "curly@stooges.com", 'xyz987', enum.DEPT_SALES))
        self.addItem(vo.UserVO('mstooge', 'Moe', 'Stooge', "moe@stooges.com", 'abc123', enum.DEPT_PLANT))

    def getUsers(self):
        return self.data
   
    def addItem(self, item):
        self.data.append(item)

    def updateItem(self, user):
        for i in range(0, len(self.data)):
            if self.data[i].user_name == user.user_name:
                self.data[i] = user

    def deleteItem(self, user):
        for i in range(0, len(self.data)):
            if self.data[i].user_name == user.user_name:
                del self.data[i]

class RoleProxy(puremvc.patterns.proxy.Proxy):

    NAME = "RoleProxy"
    def __init__(self):
        super(RoleProxy, self).__init__(RoleProxy.NAME, [])
        self.data = []
        self.addItem(vo.RoleVO('lstooge', [enum.ROLE_PAYROLL, enum.ROLE_EMP_BENEFITS]))
        self.addItem(vo.RoleVO('cstooge', [enum.ROLE_ACCT_PAY, enum.ROLE_ACCT_RCV, enum.ROLE_GEN_LEDGER]))
        self.addItem(vo.RoleVO('mstooge', [enum.ROLE_INVENTORY, enum.ROLE_PRODUCTION, enum.ROLE_SALES, enum.ROLE_SHIPPING]))

    def getRoles(self):
        print self.data
        return self.data

    def addItem(self, item):
        self.data.append(item)

    def deleteItem(self, item):
        for i in range(len(self.data)):
            if self.data[i].user_name == item.user_name:
                del self.data[i]
                break

    def doesUserHaveRole(self, user, role):
        hasRole = False
        for i in range(len(self.data)):
            if self.data[i].user_name == user.user_name:
                userRoles = self.data[i].roles
                for j in range(len(userRoles)):
                    if userRoles[j] == role:
                        hasRole = True
                        break
        return hasRole

    def addRoleToUser(self, user, role):
        result = False
        if not self.doesUserHaveRole(user, role):
            for i in range(0, len(self.data)):
                if self.data[i].user_name == user.user_name:
                    userRoles = self.data[i].roles
                    userRoles.append(role)
                    result = True
                    break
        self.sendNotification(main.AppFacade.ADD_ROLE_RESULT, result)

    def removeRoleFromUser(self, user, role):
        if self.doesUserHaveRole(user, role):
            for i in range(0, len(self.data)):
                if self.data[i].user_name == user.user_name:
                    userRoles = self.data[i].roles
                    for j in range(0, len(userRoles)):
                        if userRoles[j] == role:
                            del userRoles[i]
                            break

    def getUserRoles(self, user_name):
        userRoles = []
        for i in range(0, len(self.data)):
            if self.data[i].user_name == user_name:
                userRoles = self.data[i].roles
                break
        return userRoles
