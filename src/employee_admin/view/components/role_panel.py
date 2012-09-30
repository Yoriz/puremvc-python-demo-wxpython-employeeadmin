'''
Created on 30 Sep 2012

@author: Dave Wilson
'''

from employee_admin.model.enum.role_enum import role_combo_list, \
    ROLE_NONE_SELECTED
from employee_admin.model.vo.user_role_vo import UserRoleVo
from employee_admin.model.vo.user_vo import UserVo
from wx.lib.newevent import NewCommandEvent
import wx

class RolePanel(wx.Panel):
    
    AddRoleEvent, EVT_ADD_ROLE = NewCommandEvent()
    RemoveRoleEvent, EVT_REMOVE_ROLE = NewCommandEvent()
    
    def __init__(self, *args, **kwargs):
        super(RolePanel, self).__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        roles_label = wx.StaticText(self, label="User Roles")
        font = roles_label.GetFont()
        font.MakeBold()
        roles_label.SetFont(font)
        self.given_name_label = wx.StaticText(self, label="")
        sizer.AddSpacer(8, -1)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_sizer, 0 , wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        label_sizer.Add(roles_label)
        label_sizer.AddStretchSpacer(1)
        label_sizer.Add(self.given_name_label)
        
        self.role_list = wx.ListBox(self, size=(300, -1), style=wx.LB_SINGLE)
        self.role_list.Bind(wx.EVT_LISTBOX, self.on_listbox_role_list)
        
        self.role_combo = wx.ComboBox(self)
        self.role_combo.Bind(wx.EVT_COMBOBOX, self.on_role_combo)
        self.set_roles_list(role_combo_list)
        
        self.add_btn = wx.Button(self, -1, "Add")
        self.add_btn.Bind(wx.EVT_UPDATE_UI, self.on_update_add_btn)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        
        self.remove_btn = wx.Button(self, -1, "Remove")
        self.remove_btn.Bind(wx.EVT_UPDATE_UI, self.on_update_remove_btn)
        self.remove_btn.Bind(wx.EVT_BUTTON, self.on_remove)
        
        sizer.AddSpacer(8, -1)
        sizer.Add(self.role_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT , 8)
        sizer.AddSpacer(8, -1)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        combo_sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer.Add(combo_sizer, 1, wx.EXPAND)
        combo_sizer.Add(self.role_combo, 0, wx.EXPAND)
        hsizer.Add(self.add_btn, 0, wx.LEFT, 8)
        hsizer.Add(self.remove_btn, 0, wx.LEFT, 8)
        sizer.AddSpacer(8, -1)
        self.Layout()
        
        self.user = None
        self.user_roles = None
        self.role_selected = ROLE_NONE_SELECTED
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_panel, self)
        
    def on_update_panel(self, event):
        event.Enable(isinstance(self.user_roles, UserRoleVo))
        
    def on_update_add_btn(self, event):
        event.Enable(self.role_combo.GetSelection())
        
    def on_update_remove_btn(self, event):
        event.Enable(self.role_list.GetSelection() > -1)
        
    def on_role_combo(self, event):
        self.role_selected = event.ClientData
        self.role_list.SetSelection(-1)
        
    def on_listbox_role_list(self, event):
        self.role_selected = event.ClientData
        self.role_combo.SetSelection(0)
        
    def on_add(self, event):
        evt = self.AddRoleEvent(self.Id)
        wx.PostEvent(self, evt)
        self.role_combo.SetSelection(0)
        event.Skip()

    def on_remove(self, event):
        evt = self.RemoveRoleEvent(self.Id)
        wx.PostEvent(self, evt)
        self.role_list.SetSelection(-1)
        event.Skip()

    def set_user(self, user_vo=None):
        if user_vo:
            self.user = user_vo
            self.populate_from_user()
        else:
            self.user = UserVo()
            self.populate_from_user()
            self.user = None
        
    def populate_from_user(self):
        self.given_name_label.SetLabel(self.user.given_name)
        self.Layout()
        
    def set_user_roles(self, user_roles_vo=None):
        if user_roles_vo:
            self.user_roles = user_roles_vo.get_copy()
            self.populate_from_user_roles()
        else:
            self.user_roles = UserRoleVo()
            self.populate_from_user_roles()
            self.user_roles = None
         
    def populate_from_user_roles(self):
        self.role_list.Clear()
        for role in self.user_roles.roles: 
            self.role_list.Append(role.value, role)
        
    def set_roles_list(self, role_list_enum):
        self.role_combo.Clear()
        for role in role_list_enum: 
            self.role_combo.Append(role.value, role)
        self.role_combo.SetSelection(0)
    
  
if __name__ == '__main__':
    from employee_admin.model.common.test_user_list import test_user_list_data
    from employee_admin.model.common.test_role_list import test_role_list_data
    wxapp = wx.App(False)
    frame = wx.Frame(None)
    fsizer = wx.BoxSizer(wx.VERTICAL)
    frame.SetSizer(fsizer)
    panel = RolePanel(frame)
    fsizer.Add(panel, 1, wx.EXPAND)
    frame.Layout()
    frame.Fit()
    frame.Show()
    panel.set_user(test_user_list_data[0])
#    panel.set_user(None)
    panel.set_user_roles(test_role_list_data[0])
#    panel.set_user_roles(None)
    wxapp.MainLoop()
