'''
Created on 23 Sep 2012

@author: Dave Wilson
'''
from employee_admin.model.enum.dept_enum import DEPT_ACCT, DEPT_SALES, \
    DEPT_PLANT
from employee_admin.model.vo.user_vo import UserVo

test_user_list_data = \
    [
    UserVo("lstooge", "Larry", "Stooge", "larry@stooges.com",
            "ijk456", DEPT_ACCT),
    UserVo("cstooge", "Curly", "Stooge", "curly@stooges.com",
           "xyz987", DEPT_SALES),
    UserVo("mstooge", "Moe", "Stooge", "moe@stooges.com",
           "abc123", DEPT_PLANT)
    ]
