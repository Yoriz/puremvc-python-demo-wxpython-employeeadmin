'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

from employee_admin.model.common.obs_class_attr import obs_attr
from employee_admin.model.enum.dept_enum import dept_combo_list
from employee_admin.model.vo.user_vo import UserVo
from wx.lib.newevent import NewCommandEvent
import wx

class UserForm(wx.Panel):
    
    AddEvent, EVT_ADD = NewCommandEvent()
    UpdateEvent, EVT_UPDATE = NewCommandEvent()
    CancelEvent, EVT_CANCEL = NewCommandEvent()

    MODE_ADD = "modeAdd"
    MODE_EDIT = "modeEdit"
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        sizer.AddSpacer(8, -1)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_sizer, 0 , wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        
        profile_label = wx.StaticText(self, label="User Profile")
        font = profile_label.GetFont()
        font.MakeBold()
        profile_label.SetFont(font)
        label_sizer.Add(profile_label)
        
        self.username_label = wx.StaticText(self, label="")
        label_sizer.AddStretchSpacer(1)
        label_sizer.Add(self.username_label)
        
        self.flex_gridsizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=8)
        sizer.AddSpacer(8, -1)
        sizer.Add(self.flex_gridsizer, 0,
                  wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 8)
        sizer.AddSpacer(8, -1)
        
        ctrl_size = (200, -1)
        self.first_name_input = wx.TextCtrl(self, size=ctrl_size)
        self.first_name_input.Bind(wx.EVT_TEXT, self.on_first_name_input)
        self.create_field("First name", self.first_name_input)
        
        self.last_name_input = wx.TextCtrl(self, size=ctrl_size)
        self.last_name_input.Bind(wx.EVT_TEXT, self.on_last_name_input)
        self.create_field("Last name", self.last_name_input)
        
        self.email_input = wx.TextCtrl(self, size=ctrl_size)
        self.email_input.Bind(wx.EVT_TEXT, self.on_email_input)
        self.create_field("Email", self.email_input)
        
        self.username_input = wx.TextCtrl(self, size=ctrl_size)
        self.username_input.Bind(wx.EVT_TEXT, self.on_username_input)
        self.username_input.Bind(wx.EVT_UPDATE_UI,
                                 self.on_update_username_input)
        self.create_field("Username*", self.username_input)
        
        self.password_input = wx.TextCtrl(self, size=ctrl_size,
                                          style=wx.TE_PASSWORD)
        self.password_input.Bind(wx.EVT_TEXT, self.on_password_input)
        self.create_field("Password*", self.password_input)
        
        self.confirm_input = wx.TextCtrl(self, size=ctrl_size,
                                         style=wx.TE_PASSWORD)
        self.create_field("Confirm Password*", self.confirm_input)
        
        self.department_combo = wx.ComboBox(self, size=ctrl_size)
        self.department_combo.Bind(wx.EVT_COMBOBOX, self.on_department_combo)
        self.create_field("Department*", self.department_combo)
        self.set_department_list(dept_combo_list)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        self.submit_btn = wx.Button(self, -1, "Add User", size=(100, -1))
        self.submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        self.submit_btn.Bind(wx.EVT_UPDATE_UI, self.on_update_submit)
        hsizer.AddStretchSpacer(1)
        hsizer.Add(self.submit_btn, 0, wx.RIGHT, 8)
        
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.on_cancel)
        hsizer.Add(self.cancelBtn, 0, wx.RIGHT)
        sizer.AddSpacer(8, -1)

        self.Layout()
        
        self.user = None
        self.mode = UserForm.MODE_ADD
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_panel, self)
        
        
    def create_field(self, field_name, ctrl):
        label = wx.StaticText(self, label=field_name)
        self.flex_gridsizer.Add(label, flag=wx.ALIGN_CENTER_VERTICAL | 
                                                                wx.ALIGN_RIGHT)
        self.flex_gridsizer.Add(ctrl, flag=wx.ALIGN_CENTER)
        
    def on_update_panel(self, event):
        event_ob = event.EventObject
        if event_ob.Enabled != bool(self.user):
            event.Enable(not event_ob.Enabled)
        
    def on_update_submit(self, event):
        if not self.IsEnabled():
            event.Skip()
            return
        
        event_ob = event.EventObject
        if self.mode == self.MODE_ADD:
            event_ob.SetLabel("Add User")
        else:
            event_ob.SetLabel("Update Profile")
            
        is_valid = all([self.user.is_valid,
                        self.confirm_input.GetValue() == self.user.password])
            
        if event_ob.Enabled != is_valid:
            event.Enable(not event_ob.Enabled)
            
    def on_update_username_input(self, event):
        if not self.IsEnabled():
            event.Skip()
            return
        
        event_ob = event.EventObject
        if event_ob.Enabled != bool(self.mode == UserForm.MODE_ADD):
            event.Enable(not event_ob.Enabled)
            
    def on_first_name_input(self, event):
        self.user.first_name = event.String
        
    def on_last_name_input(self, event):
        self.user.last_name = event.String
        
    def on_email_input(self, event):
        self.user.email = event.String
        
    def on_username_input(self, event):
        self.user.user_name = event.String
        
    def on_password_input(self, event):
        self.user.password = event.String
        
    def on_department_combo(self, event):
        ordinal = event.ClientData
        dept = [item for item in dept_combo_list if item.ordinal == ordinal][0]
        self.user.department = dept
            
    def set_department_list(self, dept_list_enum):
        self.department_combo.Clear()
        for dept_enum_item in dept_list_enum: 
            self.department_combo.Append(dept_enum_item.value,
                                         dept_enum_item.ordinal)
        self.department_combo.SetSelection(0)
        
    def set_user(self, user_vo=None, mode=None):
        self.mode = mode or self.MODE_ADD
        self.user = user_vo or UserVo()
        self.set_input(self.user.password, self.confirm_input)
        self.set_user_vo_binds()
        if not user_vo:
            self.user = None
        
        self.first_name_input.SetFocus()
        self.first_name_input.SetInsertionPointEnd()
        
    def set_user_vo_binds(self):
        obs_attr(self.user, "first_name", self.set_first_name_input)
        obs_attr(self.user, "last_name", self.set_last_name_input)
        obs_attr(self.user, "email", self.set_email_input)
        obs_attr(self.user, "user_name", self.set_username_input)
        obs_attr(self.user, "user_name", self.set_username_label)
        obs_attr(self.user, "password", self.set_password_input)
        obs_attr(self.user, "department", self.set_dept_combo)

    def set_input(self, value, ctrl):
        insertion_point = ctrl.GetInsertionPoint()
        ctrl.ChangeValue("%s" % value)
        ctrl.SetInsertionPoint(insertion_point)
        
    def set_first_name_input(self, value):
        self.set_input(value, self.first_name_input)
        
    def set_last_name_input(self, value):
        self.set_input(value, self.last_name_input)
        
    def set_email_input(self, value):
        self.set_input(value, self.email_input)
        
    def set_username_input(self, value):
        self.set_input(value, self.username_input)

    def set_password_input(self, value):
        self.set_input(value, self.password_input)
        
    def set_dept_combo(self, value):
        self.department_combo.SetSelection(dept_combo_list.index(value))

    def set_username_label(self, value):
        self.username_label.SetLabel(value)
        self.Layout()
    
    def on_submit(self, event):        
        if self.mode == self.MODE_ADD:
            evt = self.AddEvent(self.Id)
        else:
            evt = self.UpdateEvent(self.Id)
        wx.PostEvent(self, evt)
        event.Skip()
    
    def on_cancel(self, event):
        evt = self.CancelEvent(self.Id)
        wx.PostEvent(self, evt)
        event.Skip()
        
if __name__ == '__main__':
    from employee_admin.model.common.test_user_list import test_user_list_data
    wxapp = wx.App(False)
    frame = wx.Frame(None)
    fsizer = wx.BoxSizer(wx.VERTICAL)
    frame.SetSizer(fsizer)
    panel = UserForm(frame)
    fsizer.Add(panel, 1, wx.EXPAND)
    frame.Layout()
    frame.Fit()
    frame.Show()
    panel.set_user(test_user_list_data[1], UserForm.MODE_EDIT)
    wxapp.MainLoop()
