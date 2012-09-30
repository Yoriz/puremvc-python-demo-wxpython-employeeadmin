'''
Created on 30 Sep 2012

@author: Dave Wilson
'''

from employee_admin.model.enum import role_enum
from employee_admin.model.vo.user_role_vo import UserRoleVo

test_role_list_data = \
    [UserRoleVo("lstooge", [role_enum.ROLE_PAYROLL,
                            role_enum.ROLE_EMP_BENEFITS]),
     UserRoleVo("cstooge", [role_enum.ROLE_ACCT_PAY,
                            role_enum.ROLE_ACCT_RCV,
                            role_enum.ROLE_GEN_LEDGER]),
     UserRoleVo("mstooge", [role_enum.ROLE_INVENTORY,
                            role_enum.ROLE_PRODUCTION,
                            role_enum.ROLE_SALES,
                            role_enum.ROLE_SHIPPING])
    ]
