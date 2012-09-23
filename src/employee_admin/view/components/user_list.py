'''
Created on 23 Sep 2012

@author: Dave Wilson
'''
import wx
from ObjectListView import ObjectListView, ColumnDefn
from wx.lib.newevent import NewCommandEvent

columns = [ColumnDefn(title="Username", valueGetter="user_name",
                      minimumWidth=75),
           ColumnDefn(title="First Name", valueGetter="first_name",
                      minimumWidth=75),
           ColumnDefn(title="Last Name", valueGetter="last_name",
                      minimumWidth=75),
           ColumnDefn(title="Email", valueGetter="email",
                      minimumWidth=90),
           ColumnDefn(title="Department", valueGetter="department",
                      minimumWidth=100),
           ColumnDefn(title="", valueGetter="*filler*",
                      minimumWidth=0, isSpaceFilling=True)]

class OLVList(ObjectListView):
    def __init__(self, *args, **kwargs):
        super(OLVList, self).__init__(*args, **kwargs)
        self.SetEmptyListMsg("No Records")
        self.useAlternateBackColors = False
        self.SetColumns(columns)
        self.AutoSizeColumns()

class UserList(wx.Panel):
    
    SelectEvent, EVT_SELECT = NewCommandEvent()
    NewEvent, EVT_NEW = NewCommandEvent()
    DeleteEvent, EVT_DELETE = NewCommandEvent()

    def __init__(self, *args, **kwargs):
        super(UserList, self).__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        sizer.AddSpacer(8, -1)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_sizer, 0 , wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        
        users_label = wx.StaticText(self, label="Users")
        font = users_label.GetFont()
        font.MakeBold()
        users_label.SetFont(font)
        label_sizer.Add(users_label)
        
        label_sizer.AddStretchSpacer(1)
        self.users_qty_label = wx.StaticText(self, label="0")
        label_sizer.Add(self.users_qty_label)
        
        sizer.AddSpacer(8, -1)
        self.user_list = OLVList(self, size=(-1, 150),style=wx.LC_REPORT | 
                                wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES)
        self.user_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_selection)
        self.user_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_selection)
        sizer.Add(self.user_list, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        
        sizer.AddSpacer(8, -1)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hsizer, 0, wx.ALIGN_RIGHT, 8)
        
        self.delete_btn = wx.Button(self, wx.ID_DELETE)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.delete_btn.Bind(wx.EVT_UPDATE_UI, self.on_update_delete)
        hsizer.Add(self.delete_btn, 0, wx.RIGHT, 8)
        
        self.new_btn = wx.Button(self, wx.ID_NEW)
        self.new_btn.Bind(wx.EVT_BUTTON, self.on_new)
        hsizer.Add(self.new_btn, 0, wx.RIGHT, 8)

        sizer.AddSpacer(8, -1)
        self.Layout()
        
        self.users = []
        
    def on_update_delete(self, event):
        event_ob = event.EventObject
        has_selection = self.user_list.GetSelectedObject() != None

        if event_ob.Enabled != has_selection:
            event.Enable(not event_ob.Enabled)
            
    def on_selection(self, event):
        selected_obj = self.user_list.GetSelectedObject()
        evt = self.SelectEvent(self.Id, selected_obj=selected_obj)
        wx.PostEvent(self, evt)
        event.Skip()
        
    def on_new(self, event):
        self.user_list.DeselectAll()
        evt = self.NewEvent(self.Id)
        wx.PostEvent(self, evt)
        event.Skip()
        
    def on_delete(self, event):
        selected_obj = self.user_list.GetSelectedObject()
        self.user_list.DeselectAll()
        evt = self.DeleteEvent(self.Id, selected_obj=selected_obj)
        wx.PostEvent(self, evt)
        event.Skip()

    def update_user_list(self, value):
        self.user_list.SetObjects(value)
        users_amount = len(value)
        self.users_qty_label.SetLabel(str(users_amount))
          
if __name__ == '__main__':
    from employee_admin.model.common.test_user_list import test_user_list_data
    wxapp= wx.App(False)
    frame = wx.Frame(None)
    panel = UserList(frame)
    panel.update_user_list(test_user_list_data)
    frame.Layout()
    frame.Show()
    wxapp.MainLoop()