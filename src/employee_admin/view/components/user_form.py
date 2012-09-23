'''
Created on 23 Sep 2012

@author: Dave Wilson
'''

import wx

class UserForm(wx.Panel):
    
    evt_ADD = wx.NewEventType()
    EVT_ADD = wx.PyEventBinder(evt_ADD, 1)
    evt_UPDATE = wx.NewEventType()
    EVT_UPDATE = wx.PyEventBinder(evt_UPDATE, 1)
    evt_CANCEL = wx.NewEventType()
    EVT_CANCEL = wx.PyEventBinder(evt_CANCEL, 1)

    MODE_ADD = "modeAdd";
    MODE_EDIT = "modeEdit";
    
    user = None
    mode = None
    
    usernameInput = None
    firstInput = None
    lastInput = None
    emailInput = None
    passwordInput = None
    confirmInput = None
    departmentCombo = None
    add_btn = None
    cancelBtn = None
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        profile_label = wx.StaticText(self, label="User Profile")
        font = profile_label.GetFont()
        font.MakeBold()
        profile_label.SetFont(font)
        self.username_label = wx.StaticText(self, label="")
        
        sizer.AddSpacer(8, -1)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_sizer, 0 , wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        label_sizer.Add(profile_label)
        label_sizer.AddStretchSpacer(1)
        label_sizer.Add(self.username_label)
        
        self.flex_gridsizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=8)
        sizer.AddSpacer(8, -1)
        sizer.Add(self.flex_gridsizer, 0,
                  wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 8)
        sizer.AddSpacer(8, -1)
        
        ctrl_size = (200, -1)
        self.first_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("First name", self.first_input)
        self.last_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("Last name", self.last_input)
        self.email_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("Email", self.email_input)
        self.username_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("Username*", self.username_input)
        self.password_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("Password*", self.password_input)
        self.confirm_input = wx.TextCtrl(self, size=ctrl_size)
        self.create_field("Confirm Password*", self.confirm_input)
        self.department_combo = wx.ComboBox(self, size=ctrl_size)
        self.create_field("Department*", self.department_combo)
         
        self.add_btn = wx.Button(self, -1, "Add User", size=(100, -1))
        self.add_btn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        hsizer.AddStretchSpacer(1)
        hsizer.Add(self.add_btn, 0, wx.RIGHT, 8)
        hsizer.Add(self.cancelBtn, 0, wx.RIGHT)
        sizer.AddSpacer(8, -1)

        self.Layout()
        
    def create_field(self, field_name, ctrl):
        label = wx.StaticText(self, label=field_name)
        self.flex_gridsizer.Add(label, flag=wx.ALIGN_CENTER_VERTICAL | 
                                                                wx.ALIGN_RIGHT)
        self.flex_gridsizer.Add(ctrl, flag=wx.ALIGN_CENTER)
    
    def updateUser(self, user):
        self.user = user
        self.usernameInput.SetValue(self.user.user_name)
        self.firstInput.SetValue(self.user.first_name)
        self.lastInput.SetValue(self.user.last_name)
        self.emailInput.SetValue(self.user.email)
        self.passwordInput.SetValue(self.user.password)
        self.confirmInput.SetValue(self.user.password)
        self.departmentCombo.SetValue(self.user.department)
        self.checkValid()

    def updateDepartmentCombo(self, choices, default):
        self.departmentCombo.Clear()
        self.departmentCombo.AppendItems(choices)
        self.departmentCombo.SetValue(default)
    
    def updateMode(self, mode):
        self.mode = mode
        if self.mode == self.MODE_ADD:
            self.add_btn.SetLabel("Add User")
        else:
            self.add_btn.SetLabel("Update User")
        
    def onAdd(self, evt):        
        if self.mode == self.MODE_ADD:
            self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_ADD, self.GetId()))
        else:
            self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_UPDATE, self.GetId()))
        self.checkValid()
    
    def onCancel(self, evt):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_CANCEL, self.GetId()))
        
    def checkValid(self, evt=None):
        if self.enableSubmit(self.usernameInput.GetValue(), self.passwordInput.GetValue(), self.confirmInput.GetValue(), self.departmentCombo.GetValue()):
            self.add_btn.Enable()
        else:
            self.add_btn.Disable()
    
    def enableSubmit(self, u, p, c, d):
        return (len(u) > 0 and len(p) > 0 and p == c and not d == enum.DEPT_NONE_SELECTED)
