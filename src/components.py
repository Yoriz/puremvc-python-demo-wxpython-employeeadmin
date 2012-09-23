"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

from ObjectListView import ObjectListView, ColumnDefn
import enum
import wx

class WxApp(wx.App):
    def __init__(self, redirect=False, filename=None,
            useBestVisual=False, clearSigInt=False):
        wx.App.__init__(self, redirect, filename, useBestVisual,
            clearSigInt)
        self.appFrame = AppFrame(None, title="PureMVC Demo",
                                 style=wx.CLOSE_BOX | wx.CAPTION)
        self.appFrame.Show()
    
    def OnInit(self):
        return True


class AppFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(AppFrame, self).__init__(*args, **kwargs)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        self.user_list = UserList(panel, style=wx.BORDER_THEME | 
                                  wx.TAB_TRAVERSAL)
        self.user_form = UserForm(panel, style=wx.BORDER_THEME | 
                                  wx.TAB_TRAVERSAL)
        self.role_panel = RolePanel(panel, style=wx.BORDER_THEME | 
                                    wx.TAB_TRAVERSAL)
        sizer.AddSpacer(8, -1)
        sizer.Add(self.user_list, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(8, -1)
        sizer.Add(h_sizer, 1, wx.EXPAND)
        h_sizer.Add(self.user_form, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        h_sizer.Add(self.role_panel, 0, wx.EXPAND | wx.RIGHT, 8)
        sizer.AddSpacer(8, -1)
        
        self.Layout()
        sizer.Fit(self)

class UserList(wx.Panel):
    
    evt_USER_SELECTED = wx.NewEventType()
    EVT_USER_SELECTED = wx.PyEventBinder(evt_USER_SELECTED, 1)
    
    evt_NEW = wx.NewEventType()
    EVT_NEW = wx.PyEventBinder(evt_NEW, 1)
    
    evt_DELETE = wx.NewEventType()
    EVT_DELETE = wx.PyEventBinder(evt_DELETE, 1)
    
    userGrid = None
    newBtn = None
    deleteBtn = None
    
    users = None
    selectedUser = None
    
    def __init__(self, *args, **kwargs):
        super(UserList, self).__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        users_label = wx.StaticText(self, label="Users")
        font = users_label.GetFont()
        font.MakeBold()
        users_label.SetFont(font)
        self.users_qty_label = wx.StaticText(self, label="0")

        self.user_list = ObjectListView(self, size=(-1, 150),
                                        style=wx.LC_REPORT | 
                                        wx.LC_SINGLE_SEL | wx.LC_HRULES | 
                                        wx.LC_VRULES)
        columns = [ColumnDefn(title="Username", valueGetter="user_name",
                          minimumWidth=100),
                   ColumnDefn(title="First Name", valueGetter="first_name",
                          minimumWidth=100),
                   ColumnDefn(title="Last Name", valueGetter="last_name",
                          minimumWidth=100),
                   ColumnDefn(title="Email", valueGetter="email",
                          minimumWidth=100),
                   ColumnDefn(title="Department", valueGetter="departmwnr",
                          minimumWidth=100, isSpaceFilling=True)]
        self.user_list.SetColumns(columns)
        self.user_list.AutoSizeColumns()
        
        self.delete_btn = wx.Button(self, wx.ID_DELETE)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.onDelete)
        self.new_btn = wx.Button(self, wx.ID_NEW)
        self.new_btn.Bind(wx.EVT_BUTTON, self.onNew)
        
        sizer.AddSpacer(8, -1)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_sizer, 0 , wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        label_sizer.Add(users_label)
        label_sizer.AddStretchSpacer(1)
        label_sizer.Add(self.users_qty_label)
        
        sizer.AddSpacer(8, -1)
        sizer.Add(self.user_list, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        sizer.AddSpacer(8, -1)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hsizer, 0, wx.ALIGN_RIGHT, 8)
        hsizer.Add(self.delete_btn, 0, wx.RIGHT, 8)
        hsizer.Add(self.new_btn, 0, wx.RIGHT, 8)
        sizer.AddSpacer(8, -1)
        self.Layout()
    
    def updateUserGrid(self, users):
        self.userGrid.ClearGrid()
        self.users = users
        for i in range(len(users)):
            self.userGrid.SetCellValue(i, 0, users[i].user_name)
            self.userGrid.SetCellValue(i, 1, users[i].first_name)
            self.userGrid.SetCellValue(i, 2, users[i].last_name)
            self.userGrid.SetCellValue(i, 3, users[i].email)
            self.userGrid.SetCellValue(i, 4, users[i].department)
            self.userGrid.SetCellValue(i, 5, users[i].password)
        self.userGrid.AutoSize()
    
    def onSelect(self, evt):
        try:
            self.selectedUser = self.users[evt.GetRow()]
            self.userGrid.SelectRow(evt.GetRow())
            self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_USER_SELECTED, self.GetId()))
        except IndexError:
            pass
    
    def deSelect(self):
        self.userGrid.SelectRow(-1)
    
    def onNew(self, evt):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_NEW, self.GetId()))
        self.deSelect()
        
    def onDelete(self, evt):
        if self.selectedUser:
            self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_DELETE, self.GetId()))
            self.deSelect()

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
        self.add_btn.Disable()
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

class RolePanel(wx.Panel):
    
    evt_ADD_ROLE = wx.NewEventType()
    EVT_ADD_ROLE = wx.PyEventBinder(evt_ADD_ROLE, 1)
    
    evt_REMOVE_ROLE = wx.NewEventType()
    EVT_REMOVE_ROLE = wx.PyEventBinder(evt_REMOVE_ROLE, 2)

    user = None
    selectedRole = None
    
    role_list = None
    role_combo = None
    add_btn = None
    remove_btn = None
    
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
        
        self.role_list = wx.ListBox(self, size=(300, -1))
        self.role_list.Bind(wx.EVT_LISTBOX, self.onListClick)
        self.role_combo = wx.ComboBox(self)
        self.role_combo.Bind(wx.EVT_COMBOBOX, self.onComboClick)
        self.add_btn = wx.Button(self, -1, "Add")
        self.add_btn.Disable()
        self.add_btn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.remove_btn = wx.Button(self, -1, "Remove")
        self.remove_btn.Disable()
        self.remove_btn.Bind(wx.EVT_BUTTON, self.onRemove)
        
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
    
    def updateRoleList(self, items):
        self.role_list.Clear()
        self.role_list.AppendItems(items)
    
    def updateRoleCombo(self, choices, default):
        self.role_combo.Clear()
        self.role_combo.AppendItems(choices)
        self.role_combo.SetValue(default)
    
    def onComboClick(self, evt):
        if not self.role_combo.GetValue() == enum.ROLE_NONE_SELECTED:
            self.add_btn.Enable()
        else:
            self.add_btn.Disable()
        self.role_list.SetSelection(-1)
        self.selectedRole = self.role_combo.GetValue()
    
    def onListClick(self, evt):
        if not self.role_list.GetSelection() == enum.ROLE_NONE_SELECTED:
            self.remove_btn.Enable()
        else:
            self.remove_btn.Disable()
        self.role_combo.SetValue(enum.ROLE_NONE_SELECTED)
        self.selectedRole = self.role_list.GetStringSelection()
    
    def onAdd(self, evt):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_ADD_ROLE, self.GetId()))
    
    def onRemove(self, evt):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_REMOVE_ROLE, self.GetId()))
    
if __name__ == '__main__':
    wxapp = WxApp(False)
    wxapp.MainLoop()
    
