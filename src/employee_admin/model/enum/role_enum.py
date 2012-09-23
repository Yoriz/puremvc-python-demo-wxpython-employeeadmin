'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

from collections import namedtuple

RoleEnumItem = namedtuple("RoleEnumItem", "value, ordinal")

ROLE_NONE_SELECTED = RoleEnumItem("--None Selected--", -1)
ROLE_ADMIN = RoleEnumItem("Administrator", 0)
ROLE_ACCT_PAY = RoleEnumItem("Accounts Payable", 1)
ROLE_ACCT_RCV = RoleEnumItem("Accounts Receivable", 2)
ROLE_EMP_BENEFITS = RoleEnumItem("Employee Benefits", 3)
ROLE_GEN_LEDGER = RoleEnumItem("General Ledger", 4)
ROLE_PAYROLL = RoleEnumItem("Payroll", 5)
ROLE_INVENTORY = RoleEnumItem("Inventory", 6)
ROLE_PRODUCTION = RoleEnumItem("Production", 7)
ROLE_QUALITY_CTL = RoleEnumItem("Quality Control", 8)
ROLE_SALES = RoleEnumItem("Sales", 0)
ROLE_ORDERS = RoleEnumItem("Orders", 10)
ROLE_CUSTOMERS = RoleEnumItem("Customers", 11)
ROLE_SHIPPING = RoleEnumItem("Shipping", 12)
ROLE_RETURNS = RoleEnumItem("Returns", 13)

role_list = [ROLE_ADMIN, ROLE_ACCT_PAY, ROLE_ACCT_RCV, ROLE_EMP_BENEFITS,
             ROLE_GEN_LEDGER, ROLE_PAYROLL, ROLE_INVENTORY, ROLE_PRODUCTION,
             ROLE_QUALITY_CTL, ROLE_SALES, ROLE_ORDERS, ROLE_CUSTOMERS,
             ROLE_SHIPPING,ROLE_RETURNS]

role_combo_list = role_list[:]
role_combo_list.insert(0, ROLE_NONE_SELECTED)