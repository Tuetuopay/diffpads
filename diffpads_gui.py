# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 11 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import sys

###########################################################################
## Class DiffPadsGui
###########################################################################

class DiffPadsGui ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"DiffPads", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        if sys.version_info[0] == 2:
            self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        else:
            self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bvs_main = wx.BoxSizer( wx.VERTICAL )

        bhs_items = wx.BoxSizer( wx.HORIZONTAL )

        # sb_footprints = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Footprints" ), wx.VERTICAL )
        # cl_footprintsChoices = [u"J9", u"P2"]
        # self.cl_footprints = wx.CheckListBox( sb_footprints.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cl_footprintsChoices, 0 )
        # sb_footprints.Add( self.cl_footprints, 1, wx.ALL|wx.EXPAND, 5 )
        # bhs_items.Add( sb_footprints, 0, wx.EXPAND, 5 )

        sb_pads = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Pads" ), wx.VERTICAL )

        self.cl_pads = wx.CheckListBox( sb_pads.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list(self.flat_fp.keys()), wx.LB_MULTIPLE )
        sb_pads.Add( self.cl_pads, 1, wx.ALL|wx.EXPAND, 5 )

        bhs_check = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_check_all = wx.Button( sb_pads.GetStaticBox(), wx.ID_ANY, u"Check all", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_check.Add( self.btn_check_all, 0, wx.ALL, 5 )

        self.btn_uncheck_all = wx.Button( sb_pads.GetStaticBox(), wx.ID_ANY, u"Uncheck all", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_check.Add( self.btn_uncheck_all, 0, wx.ALL, 5 )


        bhs_check.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        sb_pads.Add( bhs_check, 0, wx.EXPAND, 5 )

        bhs_items.Add( sb_pads, 1, wx.EXPAND, 5 )

        bvs_orientation = wx.BoxSizer( wx.VERTICAL )

        self.st_orientation = wx.StaticText( self, wx.ID_ANY, u"Orientation", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.st_orientation.Wrap( -1 )

        bvs_orientation.Add( self.st_orientation, 0, wx.ALL, 5 )

        gs_orientation = wx.GridSizer( 3, 3, 0, 0 )


        gs_orientation.Add( ( 0, 0), 0, 0, 5 )

        self.btn_up = wx.Button( self, wx.ID_ANY, u"🠹", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        gs_orientation.Add( self.btn_up, 0, wx.ALL, 5 )


        gs_orientation.Add( ( 0, 0), 0, 0, 5 )

        self.btn_left = wx.Button( self, wx.ID_ANY, u"🠸", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        gs_orientation.Add( self.btn_left, 0, wx.ALL, 5 )


        gs_orientation.Add( ( 0, 0), 0, 0, 5 )

        self.btn_right = wx.Button( self, wx.ID_ANY, u"🠺", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        gs_orientation.Add( self.btn_right, 0, wx.ALL, 5 )


        gs_orientation.Add( ( 0, 0), 0, 0, 5 )

        self.btn_down = wx.Button( self, wx.ID_ANY, u"🠻", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        gs_orientation.Add( self.btn_down, 0, wx.ALL, 5 )


        gs_orientation.Add( ( 0, 0), 0, 0, 5 )


        bvs_orientation.Add( gs_orientation, 0, 0, 5 )

        self.st_current = wx.StaticText( self, wx.ID_ANY, u"Current: None", wx.DefaultPosition, wx.DefaultSize, 0  )
        self.st_current.Wrap( -1  )

        bvs_orientation.Add( self.st_current, 0, wx.ALL|wx.EXPAND, 5  )

        bhs_items.Add( bvs_orientation, 0, 0, 5 )


        bvs_main.Add( bhs_items, 1, wx.EXPAND, 5 )

        btns_dialog = wx.StdDialogButtonSizer()
        self.btns_dialogOK = wx.Button( self, wx.ID_OK )
        btns_dialog.AddButton( self.btns_dialogOK )
        self.btns_dialogCancel = wx.Button( self, wx.ID_CANCEL )
        btns_dialog.AddButton( self.btns_dialogCancel )
        btns_dialog.Realize();

        bvs_main.Add( btns_dialog, 0, wx.EXPAND, 5 )


        self.SetSizer( bvs_main )
        self.Layout()
        bvs_main.Fit( self )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


