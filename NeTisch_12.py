#! /usr/bin/env/python3.6.7
#  -*-coding: utf-8 -*-

PROGRAM_TITLE = "NETISCH INTERFACE DESIGN"

import wx
import json
from wx.lib.floatcanvas import FloatCanvas,NavCanvas,Resources

drop1 = ['drop1_sel1','drop1_sel2','drop1_sel3','drop1_sel4','drop1_sel5']
drop2 = ['drop2_sel1','drop2_sel2','drop2_sel3','drop2_sel4','drop2_sel5']
drop3 = ['drop3_sel1','drop3_sel2','drop3_sel3','drop3_sel4','drop3_sel5']

class NavCan(NavCanvas.NavCanvas):
    def __init__(self,parent):
        NavCanvas.NavCanvas.__init__(self,
                                     parent=parent,
                                     ProjectionFun = None,
                                     BackgroundColor = "WHITE",
                                     )
        self.parent_frame = parent
        self.SetSize(1270,750)
        self.Canvas.Bind(FloatCanvas.EVT_LEFT_DOWN,self.OnClickLeft)

    def OnClickLeft(self,event):
        with open('testjson.json','r') as file1:
            T = json.load(file1)
        for room,dim in T.items():
            for par,dim1 in dim.items():
                if par == "topright_pos_y":
                    xx=int(T[room]["topright_pos_x"])
                    y1=int(T[room]["topright_pos_y"])
                    yy=0-y1
                    ll=int(T[room]["length"])
                    bb=int(T[room]["breadth"])

                    drline1 = FloatCanvas.Line([(xx,yy),(xx+ll,yy)],LineWidth=4,LineColor='black')
                    self.Canvas.AddObject(drline1)
                    self.Canvas.Draw()
                    drline2 = FloatCanvas.Line([(xx,yy),(xx,yy-bb)],LineWidth=4,LineColor='black')
                    self.Canvas.AddObject(drline2)
                    self.Canvas.Draw()
                    drline3 = FloatCanvas.Line([(xx+ll,yy),(xx+ll,yy-bb)],LineWidth=4,LineColor='black')
                    self.Canvas.AddObject(drline3)
                    self.Canvas.Draw()
                    drline4 = FloatCanvas.Line([(xx,yy-bb),(xx+ll,yy-bb)],LineWidth=4,LineColor='black')
                    self.Canvas.AddObject(drline4)
                    self.Canvas.Draw()
                self.Canvas.Draw()
                if par == "nodes":
                    for i in range(len(T[room]["nodes"])):
                        for node_par,node_val in T[room][par][i].items():
                            if T[room][par][i]["type"] == "s":
                                cir = FloatCanvas.Circle([int(T[room][par][i]["node_pos_x"]),0-int(T[room][par][i]["node_pos_y"])],7,FillColor = 'red')
                                self.Canvas.AddObject(cir)
                            if T[room][par][i]["type"] == "p":
                                rect = FloatCanvas.Rectangle([int(T[room][par][i]["node_pos_x"]),0-int(T[room][par][i]["node_pos_y"])],(8,8),FillColor='blue')
                                self.Canvas.AddObject(rect)
                            if T[room][par][i]["type"] == "k":
                                poly = FloatCanvas.Polygon([(int(T[room][par][i]["node_pos_x"])-4,0-int(T[room][par][i]["node_pos_y"])-4),
                                                            (int(T[room][par][i]["node_pos_x"])+4,0-int(T[room][par][i]["node_pos_y"])-4),
                                                            (int(T[room][par][i]["node_pos_x"])+4,0-int(T[room][par][i]["node_pos_y"])+4),
                                                            (int(T[room][par][i]["node_pos_x"])-4,0-int(T[room][par][i]["node_pos_y"])+4)],
                                                           FillColor='yellow')
                                self.Canvas.AddObject(poly)
                            if T[room][par][i]["type"] == "r":
                                poly1 = FloatCanvas.Polygon([(int(T[room][par][i]["node_pos_x"]),0-int(T[room][par][i]["node_pos_y"])-7),
                                                             (int(T[room][par][i]["node_pos_x"])-7,0-int(T[room][par][i]["node_pos_y"])+7),
                                                             (int(T[room][par][i]["node_pos_x"])+7,0-int(T[room][par][i]["node_pos_y"])+7)],
                                                            FillColor='cyan')
                                self.Canvas.AddObject(poly1)
                    self.Canvas.Draw()
            if room == "Blank_Area":
                points = [(int(T[room]['x1']),0-int(T[room]['y1'])),
                          (int(T[room]['x2']),0-int(T[room]['y2'])),
                          (int(T[room]['x3']),0-int(T[room]['y3'])),
                          (int(T[room]['x4']),0-int(T[room]['y4'])),
                          (int(T[room]['x5']),0-int(T[room]['y5'])),
                          (int(T[room]['x6']),0-int(T[room]['y6'])),
                          (int(T[room]['x7']),0-int(T[room]['y7'])),
                          (int(T[room]['x8']),0-int(T[room]['y8'])),
                          (int(T[room]['x9']),0-int(T[room]['y9'])),
                          (int(T[room]['x10']),0-int(T[room]['y10'])),
                          (int(T[room]['x11']),0-int(T[room]['y11']))]

                blankarea = FloatCanvas.Polygon(points,LineWidth=4,LineColor='black',FillColor = "SKY BLUE" , FillStyle='Solid')
                self.Canvas.AddObject(blankarea)

            self.Canvas.Draw()
    

class PanelFrame(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)

        # Creating Panel-Network Design attributes
        sizer = wx.GridBagSizer()
        
        text1 = wx.StaticText(self,-1,label="Network Design ::")
        sizer.Add(text1,pos=(0,0),flag=wx.LEFT|wx.TOP, border=10)

        line = wx.StaticLine(self)
        sizer.Add(line, pos=(1, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)
 
        text2 = wx.StaticText(self,-1,"Load:")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)
        
        button1 = wx.Button(self, label="Browse...")
        sizer.Add(button1, pos=(2, 1), flag=wx.TOP|wx.LEFT, border=5)
        self.Bind(wx.EVT_BUTTON, self.OnClickBrowse, button1)

        line1 = wx.StaticLine(self)
        sizer.Add(line1, pos=(4, 0), span=(1, 12),flag=wx.EXPAND|wx.BOTTOM, border=10)

        staticbox = wx.StaticBox(self, label="Gen C.Q:")
        staticboxsizer = wx.StaticBoxSizer(staticbox,wx.VERTICAL)
        combo1 = wx.ComboBox(self,-1,"Select: ",pos=(7,0),size=(150,30),choices=drop1,style=wx.CB_DROPDOWN)
        staticboxsizer.Add(combo1, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(staticboxsizer, pos=(6, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnGenCQ,combo1)
        
        sbox = wx.StaticBox(self, label="Optimize:")
        sboxsizer = wx.StaticBoxSizer(sbox,wx.VERTICAL)
        combo2 = wx.ComboBox(self,-1,"Select: ",pos=(11,0),size=(150,30),choices=drop2,style=wx.CB_DROPDOWN)
        sboxsizer.Add(combo2, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sboxsizer, pos=(10, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnOptimize,combo2)

        sb = wx.StaticBox(self, label="Schedule:")
        sbsizer = wx.StaticBoxSizer(sb,wx.VERTICAL)
        combo4 = wx.ComboBox(self,-1,"Select: ",pos=(15,0),size=(150,30),choices=drop3,style=wx.CB_DROPDOWN)
        sbsizer.Add(combo4, 0, wx.ALL|wx.LEFT, 10)
        sizer.Add(sbsizer, pos=(14, 0), span=(1, 12), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        self.Bind(wx.EVT_COMBOBOX,self.OnSchedule,combo4)

        self.SetSize(100,750)
        self.SetSizer(sizer)
        self.Show()
    
        
    def OnGenCQ(self,event):
        self.SetStatusText("Current Option : Gen C.Q - "+ event.GetEventObject().GetStringSelection())

    def OnOptimize(self,event):
        self.SetStatusText("Current Option : Optimize - "+ event.GetEventObject().GetStringSelection())

    def OnSchedule(self,event):
        self.SetStatusText("Current Option : Schedule - "+ event.GetEventObject().GetStringSelection())

    def OnClickBrowse(self, event):
        ''' Should retrieve the file from directory '''

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title="Splitter for NeTISCH GUI")

        self.CreateStatusBar()
        self.SetStatusText("NeTisch - Graphical User Interface")

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
        self.SetSize(1370,750)
        self.Centre()

        ## Creating Iconbar
        toolbar1 = self.CreateToolBar(wx.TB_DOCKABLE)
        toolbar1.AddTool(wx.ID_OPEN,'Open/Load', wx.Bitmap('open.png'))
        toolbar1.AddTool(wx.ID_PREVIEW,'Run', wx.Bitmap('play.png'))
        toolbar1.AddTool(wx.ID_VIEW_DETAILS,'ViewCQ', wx.Bitmap('viewcq.png'))
        toolbar1.AddTool(wx.ID_VIEW_SMALLICONS,'ViewOpt-top', wx.Bitmap('viewopttop.png'))
        toolbar1.AddTool(wx.ID_VIEW_SMALLICONS,'VisSchedule', wx.Bitmap('visschedule.png'))
        toolbar1.EnableTool(wx.ID_REDO, False)
        toolbar1.AddSeparator()
        toolbar1.Realize()

        splitter = wx.SplitterWindow(self)
        leftP = NavCan(splitter)
        rightP = PanelFrame(splitter)
        
        splitter.SplitVertically(leftP,rightP)
        splitter.SetMinimumPaneSize(30)
        leftP.SetSize(1270,750)
        rightP.SetSize(100,750)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter,1,wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()




