#! /usr/bin/python 3.6.7
# -*- coding: utf-8 -*-

# Use JSON file: /home/sherine/WPyDirectory/Work/t_json.json

PROGRAM_TITLE = "NETISCH INTERFACE DESIGN"

drop1 = ['drop1_sel1','drop1_sel2','drop1_sel3','drop1_sel4','drop1_sel5']
drop2 = ['drop2_sel1','drop2_sel2','drop2_sel3','drop2_sel4','drop2_sel5']
drop3 = ['drop3_sel1','drop3_sel2','drop3_sel3','drop3_sel4','drop3_sel5']


import wx
import os
from wx.lib.floatcanvas import FloatCanvas,NavCanvas,Resources
import numpy
import json
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance
from itertools import combinations
import pickle
import pdb
import logging
import math
import pydot
import graphviz

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)


def store_pickle(graph, filename='pickle'):
    # Its important to use binary mode 
    wrfile = open(filename, 'wb')
    logging.debug('Writing graph to pickle')
    # source, destination 
    pickle.dump(graph, wrfile) 
    logging.debug('Finished Writing')                     
    wrfile.close()

def load_pickle(filename='pickle'): 
    # for reading also binary mode is important 
    rdfile = open(filename, 'rb')  
    logging.debug('Reading graph from pickle')  
    graph = pickle.load(rdfile) 
    logging.debug('Finished Reading')  
    #pj.draw_graph(graph, "out_graph")
    return graph

def make_graphml(graph, filename="gml"):
    nx.write_graphml(graph, filename)
    logging.debug('Finished making graphml')

def make_dotfile(Graph, filename='dot'):
    graph = Graph.copy()
    for n in graph:                                                                                           
        graph.node[n]['pos'] = '"%f,%f!"'%(graph.node[n]['posx'], graph.node[n]['posy'])
    logging.debug('Writing graph to dotfile')
    nx.drawing.nx_pydot.write_dot(graph, filename)
    ##print ('\n\nNow run the command "neato -Tps '+filename+' >'+filename+'.ps" from the directory containing '+filename+'.dot\n\n')

def get_pos(graph):
    px = nx.get_node_attributes(graph, 'posx')
    py = nx.get_node_attributes(graph, 'posy')

    pos = {}
    for n in px: 
        pos[n]=(px[n],py[n])
    #pos = tuple(map(int, p.split(',')))
    return(pos)

def edge_calc(graph, limit, param = 'distance'):
    valid_edges = []
    if param == 'distance':
        pos = get_pos(graph)
        n_type = nx.get_node_attributes(graph, 'type')
        for i in list(combinations(pos, 2)):
            d = distance.euclidean(pos[i[0]], pos[i[1]])
            
            logging.debug(str(i)+' '+str(d))
            if d<=limit:
                weight = 0
# =============================OLD PROPOSAL for weights======================== 
#                if n_type[i[0]]=='R': weight+=1
#                if n_type[i[1]]=='R': weight+=1
# =============================================================================
                
        #my proposal ---------------------------------------
                if n_type[i[0]]=='S': weight+=1
                elif n_type[i[0]]=='R': weight+=2
                if n_type[i[1]]=='S': weight+=1
                elif n_type[i[1]]=='R': weight+=2
        #---------------------------------------------------
                valid_edges.append(i+(weight,))
    return (valid_edges)

def draw_graph(graph, filename="graph.png"):
    my_dpi = 100
    #plt.figure(frameon=False, figsize=(8,8), dpi=my_dpi)
    plt.clf()
    type_map=nx.get_node_attributes(graph, 'type')

    colour_map=[]
    for n in type_map: 
        if type_map[n]=='R':
            colour_map.append('yellow')
        elif type_map[n]=='S':
            colour_map.append('green')
        elif type_map[n]=='BS':
            colour_map.append('blue')
        else:
            colour_map.append('black')

    nx.draw(graph, node_size = min(300, 300*150/len(type_map)), font_size= min(12, int(12*150/len(type_map))), pos= get_pos(graph), with_labels = True, node_color = colour_map)  
    
    bbox = {'ec':[1,1,1,0], 'fc':[0,1,1,0]}  # hack to label edges over line (rather than breaking up line)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, font_size= min(12, int(12*150/len(type_map))), pos=get_pos(graph), edge_labels=edge_labels, bbox=bbox)

    #plt.axis('on')
    #plt.grid('on')
    plt.savefig(filename, dpi=my_dpi)
    plt.show()

def draw_schedule(graph, filename="graph.png"):
    my_dpi = 100
    #plt.figure(frameon=False, figsize=(8,8), dpi=my_dpi)
    plt.clf()
    type_map=nx.get_node_attributes(graph, 'type')
    bmsg = nx.get_node_attributes(graph, 'Bmsg')
    ecol = nx.get_edge_attributes(graph, 'color')
    ewid =nx.get_edge_attributes(graph, 'width')
    colour_map=[]
    for n in type_map: 
        if bmsg[n]:
            colour_map.append('red')
        elif type_map[n]=='R':
            colour_map.append('yellow')
        elif type_map[n]=='S':
            colour_map.append('green')
        elif type_map[n]=='BS':
            colour_map.append('blue')
        else:
            colour_map.append('black')
        
    ecolor = []
    ewidth = []
    for u,v in ecol:
        ecolor.append(ecol[u,v])
        ewidth.append(ewid[u,v])

    nx.draw(graph, node_size = min(300, 300*150/len(type_map)), font_size= min(12, int(12*150/len(type_map))),pos= get_pos(graph), with_labels = True, node_color = colour_map, edge_color=ecolor, width = ewidth)  
    
    bbox = {'ec':[1,1,1,0], 'fc':[0,1,1,0]}  # hack to label edges over line (rather than breaking up line)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, font_size= min(12, int(12*150/len(type_map))), pos=get_pos(graph), edge_labels=edge_labels, bbox=bbox)

    #plt.axis('on')
    #plt.grid('on')
    plt.savefig(filename)
    plt.show()
    
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
        self.nav_canvas = FloatCanvas.FloatCanvas(self.splitter_window, size=(600, 900), BackgroundColor = "IVORY")
        self.nav_canvas.InitAll()
        self.properties_panel = wx.Panel(self.splitter_window, id = wx.ID_ANY)
        self.splitter_window.SplitVertically(self.nav_canvas, self.properties_panel)
        self.nav_canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)

        # Creating StatusBar
        self.CreateStatusBar()
        self.SetStatusText("NeTisch - Graphical User Interface")
        self.nav_canvas.Draw()

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
        self.SetStatusText(openFileDialog.GetPath())
        self.filename = openFileDialog.GetFilename()
        self.dirname = openFileDialog.GetDirectory()
        with open(os.path.join(self.dirname, self.filename), "r") as file1:
            node_data = json.load(file1)
                
        file_dir = os.path.dirname(openFileDialog.GetPath())
        file = os.path.basename(openFileDialog.GetPath())
        file_name, file_ext = os.path.splitext(file)
        out_file_path = os.path.join(file_dir, file_name)
        
        G = nx.Graph()
        for key1,val1 in node_data.items():
            for key2,val2 in val1.items():
                if (key2 == "Nodes"):
                    for i in range(len(node_data[key1]["Nodes"])):
                        G.add_node(node_data[key1][key2][i]["id"])
                        for key3 in node_data[key1][key2][i]:
                            G.nodes[node_data[key1][key2][i]["id"]][key3] = node_data[key1][key2][i][key3]

        logging.debug(str(list(G.nodes(data=True))))
# =============================== Input a value for "limit" ======================================
        dlg_limit = wx.TextEntryDialog(self.nav_canvas, 'Input the limit value:','Limit Value ?')
        if dlg_limit.ShowModal() == wx.ID_OK:
            limit = int(dlg_limit.GetValue())
        dlg_limit.Destroy() 
# =================================================================================================
        G.add_weighted_edges_from(edge_calc(G, limit, param = 'distance'))
        option = True    #-----sbt
        
        #making different kinds of o/p files
        if(option == True):
            store_pickle(G, out_file_path+'_pickle')
            make_graphml(G, out_file_path+'_gml')
            make_dotfile(G, out_file_path+'_dot')
            draw_graph(G, out_file_path+'_graph')

        return (G, out_file_path)

        openFileDialog.Destroy()
    
if __name__ == "__main__":
    app = wx.App()
    frame = MasterFrame(None,title = "NETISCH")
    frame.Show()
    app.MainLoop()


    
