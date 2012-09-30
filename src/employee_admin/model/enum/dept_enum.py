'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

from collections import namedtuple

DeptEnumItem = namedtuple("DeptEnumItem", "value, ordinal")
  
DEPT_NONE_SELECTED = DeptEnumItem("--None Selected--" , -1)
DEPT_ACCT = DeptEnumItem("Accounting" , 0)
DEPT_SALES = DeptEnumItem("Sales" , 1)
DEPT_PLANT = DeptEnumItem("Plant" , 2)

dept_list = [DEPT_ACCT, DEPT_SALES, DEPT_PLANT]

dept_combo_list = dept_list[:]
dept_combo_list.insert(0, DEPT_NONE_SELECTED)






    
