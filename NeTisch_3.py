#! /usr/bin/python 3.6.7
# -*- coding: utf-8 -*-

PROGRAM_TITLE = "NETISCH INTERFACE DESIGN"

drop1 = ['drop1_sel1','drop1_sel2','drop1_sel3','drop1_sel4','drop1_sel5']
drop2 = ['drop2_sel1','drop2_sel2','drop3_sel3','drop4_sel4','drop5_sel5']
drop3 = ['drop3_sel1','drop3_sel2','drop3_sel3','drop3_sel4','drop3_sel5']

import wx
import os
from wx.lib.floatcanvas import FloatCanvas,NavCanvas,Resources
import numpy

class MasterFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        ## Creating Menubar
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        file1 = filemenu.Append(wx.ID_NEW,'New','New File')
        file2 = filemenu.Append(wx.ID_OPEN,'Open','Open File')
        edit_submenu = wx.Menu()
        edit_submenu.Append(wx.ID_ANY,'Select')
        edit_submenu.Append(wx.ID_ANY,'Copy')
        edit_submenu.Append(wx.ID_ANY,'Paste')
        filemenu.Append(wx.ID_EDIT, '&Edit', edit_submenu)
        file4 = filemenu.Append(wx.ID_SAVE,'Save','Save File')
        file5 = filemenu.Append(wx.ID_SAVEAS,'Save As','Save As File')
        file6 = filemenu.Append(wx.ID_CLOSE,'Close','Close File')
        menubar.Append(filemenu, '&File')
        network_menu = wx.Menu()
        net1 = network_menu.Append(wx.ID_NETWORK,'net1','Network1')
        net2 = network_menu.Append(wx.ID_PREVIEW,'net2','Network2')
        net3 = network_menu.Append(wx.ID_SELECT_COLOR,'net3','Network3')
        menubar.Append(network_menu, '&Network')
        netisch_menu = wx.Menu()
        netisch1 = netisch_menu.Append(wx.ID_VIEW_DETAILS,'view','View NeTisch')
        netisch2 = netisch_menu.Append(wx.ID_VIEW_LIST,'netisch2','List NeTisch')
        menubar.Append(netisch_menu, '&NeTisch')
        help_menu = wx.Menu()
        aboutmenu = help_menu.Append(wx.ID_ABOUT,'About NeTisch','About NeTisch')
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)
        self.SetSize(900,900)
        self.Centre()

        ## Creating Iconbar
        toolbar1 = self.CreateToolBar()
        toolbar1.AddTool(wx.ID_OPEN,'Open/Load', wx.Bitmap('open.png'))
        toolbar1.AddTool(wx.ID_PREVIEW,'Run', wx.Bitmap('play.png'))
        toolbar1.AddTool(wx.ID_VIEW_DETAILS,'ViewCQ', wx.Bitmap('viewcq.png'))
        toolbar1.AddTool(wx.ID_VIEW_LARGEICONS,'ViewOpt-top', wx.Bitmap('viewopttop.png'))
        toolbar1.AddTool(wx.ID_VIEW_SMALLICONS,'VisSchedule', wx.Bitmap('visschedule.png'))
        toolbar1.EnableTool(wx.ID_REDO, False)
        toolbar1.AddSeparator()
        toolbar1.Realize()

        self.splitter_window = wx.SplitterWindow(self,id=wx.ID_ANY,style=wx.SP_3D)
        self.nav_canvas = FloatCanvas.FloatCanvas(self.splitter_window, size=(600, 600), BackgroundColor = "IVORY")
        self.nav_canvas.InitAll()
        self.properties_panel = wx.Panel(self.splitter_window, id = wx.ID_ANY)
        self.splitter_window.SplitVertically(self.nav_canvas, self.properties_panel)
        
        self.CreateStatusBar()
        self.nav_canvas.Draw()

        # Creating Panel-Network Design attributes
        sizer = wx.GridBagSizer()
        
        text1 = wx.StaticText(self.properties_panel,-1,label="Network Design ::")
        sizer.Add(text1,pos=(0,0),flag=wx.LEFT|wx.TOP, border=10)

        line = wx.StaticLine(self.properties_panel)
        sizer.Add(line, pos=(1, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)
 
        text2 = wx.StaticText(self.properties_panel,-1,"Load:")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)
        
        path = wx.TextCtrl(self.properties_panel,-1,style=wx.ALIGN_LEFT)
        sizer.Add(path,pos=(2,1),span=(1,7),flag=wx.EXPAND|wx.LEFT, border=5)
        
        button1 = wx.Button(self.properties_panel, label="Browse...")
        sizer.Add(button1, pos=(2, 9), flag=wx.TOP|wx.RIGHT, border=5)
        self.Bind(wx.EVT_BUTTON, self.OnClickBrowse, button1)

        line1 = wx.StaticLine(self.properties_panel)
        sizer.Add(line1, pos=(4, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)

        staticbox = wx.StaticBox(self.properties_panel, label="Gen C.Q:")
        staticboxsizer = wx.StaticBoxSizer(staticbox,wx.VERTICAL)
        combo1 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(7,0),size=(150,30),choices=drop1,style=wx.CB_DROPDOWN)
        staticboxsizer.Add(combo1, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(staticboxsizer, pos=(6, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        sbox = wx.StaticBox(self.properties_panel, label="Optimize:")
        sboxsizer = wx.StaticBoxSizer(sbox,wx.VERTICAL)
        combo2 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(11,0),size=(150,30),choices=drop2,style=wx.CB_DROPDOWN)
        sboxsizer.Add(combo2, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sboxsizer, pos=(10, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        sb = wx.StaticBox(self.properties_panel, label="Schedule:")
        sbsizer = wx.StaticBoxSizer(sb,wx.VERTICAL)
        combo4 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(15,0),size=(150,30),choices=drop3,style=wx.CB_DROPDOWN)
        sbsizer.Add(combo4, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sbsizer, pos=(14, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        self.properties_panel.SetSizerAndFit(sizer)
        self.Show(True)
        
##        self.panel_list.Bind(wx.EVT_LISTBOX, self.OnListBox)
        self.nav_canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)

    def OnClickBrowse(self, event):
        self.SetStatusText("Find the file...")
        openFileDialog = wx.FileDialog(self.properties_panel,"Open","","","Python files (*.py)|*.py",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        print(openFileDialog.GetPath())
        self.SetStatusText(openFileDialog.GetPath())
        self.properties_panel.path.WriteText(openFileDialog.GetPath())
        openFileDialog.Destroy()

    def Openfile(self):
        wildcard = "Text Files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            f=open(dlg.GetPath(), 'r')
            with f:
                data = f.read()
                self.text.SetValue(data)
                dlg.Destroy()
            f.close()

        # add a rectangle
    def OnLeftDown(self,event):
        x = event.Coords[0]
        y = event.Coords[1]
        print("coordinates: ",x,y)
        rect = FloatCanvas.Rectangle((x,y), (300, 40), FillColor='SKY BLUE')
        self.nav_canvas.AddObject(rect)
        self.nav_canvas.Draw()
    
if __name__ == "__main__":
    app = wx.App()
    frame = MasterFrame(None,title = "Netisch-GUI-SampleCode-3")
    frame.Show()
    app.MainLoop()


    
