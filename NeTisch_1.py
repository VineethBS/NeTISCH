#! /usr/bin/python 3.6.7
# -*- coding: utf-8 -*-

PROGRAM_TITLE = "NETISCH INTERFACE DESIGN"

import wx

class MasterFrame(wx.Frame):
        def __init__(self,*args,**kwargs):
                wx.Frame.__init__(self,*args,**kwargs)

                menubar = wx.MenuBar()

                filemenu = wx.Menu()
                file1 = filemenu.Append(wx.ID_NEW,'New','New File')
                file2 = filemenu.Append(wx.ID_OPEN,'Open','Open File')
                file3 = filemenu.Append(wx.ID_EDIT,'Edit','Edit File')
                file4 = filemenu.Append(wx.ID_SAVE,'Save','Save File')
                file5 = filemenu.Append(wx.ID_SAVEAS,'Save As','Save As File')
                file6 = filemenu.Append(wx.ID_CLOSE,'Close','Close File')
                menubar.Append(filemenu, '&File')

                network_menu = wx.Menu()
                net1 = network_menu.Append(wx.ID_NETWORK,'net1','Network1')
                net2 = network_menu.Append(wx.ID_PREVIEW,'net2','Network2')
                net3 = network_menu.Append(wx.ID_SELECT_COLOR,'ne3','Network3')
                menubar.Append(network_menu, '&Network')

                netisch_menu = wx.Menu()
                netisch1 = netisch_menu.Append(wx.ID_VIEW_DETAILS,'view','View NeTisch')
                netisch2 = network_menu.Append(wx.ID_VIEW_LIST,'netisch2','List NeTisch')
                menubar.Append(netisch_menu, '&NeTisch')

                help_menu = wx.Menu()
                aboutmenu = help_menu.Append(wx.ID_ABOUT,'About NeTisch','About NeTisch')
                menubar.Append(help_menu, '&Help')

                self.SetMenuBar(menubar)

if __name__ == "__main__":
        app = wx.App()
        frame = MasterFrame(None,title="Netisch - GUI - SampleCode1")
        frame.Show()
        app.MainLoop()

        
