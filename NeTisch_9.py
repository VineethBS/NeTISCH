#! /usr/bin/python 3.6.7
# -*- coding: utf-8 -*-

# Drawing on a Panel; NOT Canvas


PROGRAM_TITLE = "NETISCH INTERFACE DESIGN"

drop1 = ['drop1_sel1','drop1_sel2','drop1_sel3','drop1_sel4','drop1_sel5']
drop2 = ['drop2_sel1','drop2_sel2','drop2_sel3','drop2_sel4','drop2_sel5']
drop3 = ['drop3_sel1','drop3_sel2','drop3_sel3','drop3_sel4','drop3_sel5']

import wx
import os
from wx.lib.floatcanvas import FloatCanvas,NavCanvas,Resources
import numpy
import json

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
        self.panel1 = wx.Panel(self.splitter_window, id = wx.ID_ANY)
        self.panel1.SetBackgroundColour(wx.WHITE)
        self.SetTitle("Test GUI")
        self.SetSize(900,600)
        self.properties_panel= wx.Panel(self.splitter_window, id = wx.ID_ANY)
        self.splitter_window.SplitVertically(self.panel1, self.properties_panel)
        self.panel1.Bind(wx.EVT_PAINT, self.OnPaint)

        # Creating StatusBar
        self.CreateStatusBar()
        self.SetStatusText("NeTisch - Graphical User Interface")

        # Creating Panel-Network Design attributes
        sizer = wx.GridBagSizer()
        
        text1 = wx.StaticText(self.properties_panel,-1,label="Network Design ::")
        sizer.Add(text1,pos=(0,0),flag=wx.LEFT|wx.TOP, border=10)

        line = wx.StaticLine(self.properties_panel)
        sizer.Add(line, pos=(1, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)
 
        text2 = wx.StaticText(self.properties_panel,-1,"Load:")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)
        
        button1 = wx.Button(self.properties_panel, label="Browse...")
        sizer.Add(button1, pos=(2, 1), flag=wx.TOP|wx.LEFT, border=5)
        self.Bind(wx.EVT_BUTTON, self.OnClickBrowse, button1)

        line1 = wx.StaticLine(self.properties_panel)
        sizer.Add(line1, pos=(4, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)

        staticbox = wx.StaticBox(self.properties_panel, label="Gen C.Q:")
        staticboxsizer = wx.StaticBoxSizer(staticbox,wx.VERTICAL)
        combo1 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(7,0),size=(150,30),choices=drop1,style=wx.CB_DROPDOWN)
        staticboxsizer.Add(combo1, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(staticboxsizer, pos=(6, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnGenCQ,combo1)
        
        sbox = wx.StaticBox(self.properties_panel, label="Optimize:")
        sboxsizer = wx.StaticBoxSizer(sbox,wx.VERTICAL)
        combo2 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(11,0),size=(150,30),choices=drop2,style=wx.CB_DROPDOWN)
        sboxsizer.Add(combo2, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sboxsizer, pos=(10, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnOptimize,combo2)

        sb = wx.StaticBox(self.properties_panel, label="Schedule:")
        sbsizer = wx.StaticBoxSizer(sb,wx.VERTICAL)
        combo4 = wx.ComboBox(self.properties_panel,-1,"Select: ",pos=(15,0),size=(150,30),choices=drop3,style=wx.CB_DROPDOWN)
        sbsizer.Add(combo4, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sbsizer, pos=(14, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnSchedule,combo4)
        
        self.properties_panel.SetSizerAndFit(sizer)
        self.panel1.SetSizerAndFit(sizer)

    def OnLeftDown(self,event):
        x = event.Coords[0]
        y = event.Coords[1]
        print("coordinates: ",x,y)
        rect = FloatCanvas.Rectangle((x,y), (300, 40), FillColor='SKY BLUE')
        self.nav_canvas.AddObject(rect)
        self.nav_canvas.Draw()
    
    def OnGenCQ(self,event):
        self.SetStatusText("Current Option : Gen C.Q - "+ event.GetEventObject().GetStringSelection())

    def OnOptimize(self,event):
        self.SetStatusText("Current Option : Optimize - "+ event.GetEventObject().GetStringSelection())

    def OnSchedule(self,event):
        self.SetStatusText("Current Option : Schedule - "+ event.GetEventObject().GetStringSelection())

    def OnClickBrowse(self, event):
        self.SetStatusText("Find the json file...")
        openFileDialog = wx.FileDialog(self.properties_panel,"Open","","","*.*",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        print(openFileDialog.GetPath())
        self.SetStatusText(openFileDialog.GetPath())
        self.filename = openFileDialog.GetFilename()
        self.dirname = openFileDialog.GetDirectory()
        openFileDialog.Destroy()

    def OnPaint(self,event):
        print('Entering OnPaint')
        with open(os.path.join(self.dirname, self.filename), "r") as f:
            T = json.load(f)
        dc = wx.PaintDC(self.panel1)
        # dc.Clear()
        dc.SetPen(wx.Pen(wx.BLUE, 0.5))
        vertical_lines = [(i*5,0,i*5,600) for i in range(181)]
        horizontal_lines = [(0,i*5,900,i*5) for i in range(121)]
        dc.DrawLineList(horizontal_lines+vertical_lines)
        dc.SetPen(wx.Pen(wx.BLACK,3))
        
        for room,dim in T.items():
            for par,dim1 in dim.items():
                if par == "topright_pos_y":
                    xx=int(T[room]["topright_pos_x"])
                    yy=int(T[room]["topright_pos_y"])
                    ll=int(T[room]["length"])
                    bb=int(T[room]["breadth"])
                    dc.DrawLine(xx,yy,xx+ll,yy)
                    dc.DrawLine(xx,yy,xx,yy+bb)
                    dc.DrawLine(xx+ll,yy,xx+ll,yy+bb)
                    dc.DrawLine(xx,yy+bb,xx+ll,yy+bb)
                dc.SetPen(wx.Pen(wx.BLACK,3))
                if par=="Nodes":
                    for i in range(len(T[room]["Nodes"])):
                        for node_par,node_val in T[room][par][i].items():
                            if T[room][par][i]["type"] == "s":
                                    dc.SetBrush(wx.Brush('#ed0111'))
                                    dc.SetPen(wx.Pen('#ed0111',3))
                                    dc.DrawCircle(int(T[room][par][i]["node_pos_x"]),int(T[room][par][i]["node_pos_y"]),4)
                            if T[room][par][i]["type"] == "p":
                                    dc.SetBrush(wx.Brush('#000000'))
                                    dc.SetPen(wx.Pen('#000000',3)) 
                                    dc.DrawRectangle(int(T[room][par][i]["node_pos_x"]),int(T[room][par][i]["node_pos_y"]),8,8)
                            if T[room][par][i]["type"] == "k":
                                    dc.SetBrush(wx.Brush('#fdd816'))
                                    dc.SetPen(wx.Pen('#fdd816',3)) 
                                    dc.DrawPolygon([(int(T[room][par][i]["node_pos_x"])-4,int(T[room][par][i]["node_pos_y"])-4),
                                                   (int(T[room][par][i]["node_pos_x"])+4,int(T[room][par][i]["node_pos_y"])-4),
                                                   (int(T[room][par][i]["node_pos_x"])+4,int(T[room][par][i]["node_pos_y"])+4),
                                                   (int(T[room][par][i]["node_pos_x"])-4,int(T[room][par][i]["node_pos_y"])+4)])
                            if T[room][par][i]["type"] == "r":
                                    dc.SetBrush(wx.Brush('#29fdf7'))
                                    dc.SetPen(wx.Pen('#29fdf7',3)) 
                                    dc.DrawPolygon([(int(T[room][par][i]["node_pos_x"]),int(T[room][par][i]["node_pos_y"])-7),
                                                   (int(T[room][par][i]["node_pos_x"])-7,int(T[room][par][i]["node_pos_y"])+7),
                                                   (int(T[room][par][i]["node_pos_x"])+7,int(T[room][par][i]["node_pos_y"])+7)])
            if room == "Blank_Area":
                    dc.SetBrush(wx.Brush('#95bce7'))
                    dc.DrawPolygon([(int(T[room]['x1']),int(T[room]['y1'])),
                                    (int(T[room]['x2']),int(T[room]['y2'])),
                                    (int(T[room]['x3']),int(T[room]['y3'])),
                                    (int(T[room]['x4']),int(T[room]['y4'])),
                                    (int(T[room]['x5']),int(T[room]['y5'])),
                                    (int(T[room]['x6']),int(T[room]['y6'])),
                                    (int(T[room]['x7']),int(T[room]['y7'])),
                                    (int(T[room]['x8']),int(T[room]['y8'])),
                                    (int(T[room]['x9']),int(T[room]['y9'])),
                                    (int(T[room]['x10']),int(T[room]['y10'])),
                                    (int(T[room]['x11']),int(T[room]['y11']))])
        print('Leaving OnPaint')    
#=================================================================================================================                                

    
if __name__ == "__main__":
    app = wx.App()
    frame = MasterFrame(None)
    frame.Show()
    app.MainLoop()


    
