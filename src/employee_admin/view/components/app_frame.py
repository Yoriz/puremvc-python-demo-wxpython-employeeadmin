'''
Created on 30 Sep 2012

@author: Dave Wilson
'''
from employee_admin.view.components.role_panel import RolePanel
from employee_admin.view.components.user_form import UserForm
from employee_admin.view.components.user_list import UserList
import wx

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
        
if __name__ == '__main__':
    wxapp = wx.App(False)
    frame = AppFrame(None, title="Employee Admin")
    frame.Show()
    wxapp.MainLoop()
