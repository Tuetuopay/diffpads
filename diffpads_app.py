#!/usr/bin/env python

import wx
import .diffpads_dialog

class DiffPadsApp(wx.App):
    def __init__(self, board):
        self.board = board
        super(DiffPadsApp, self).__init__()

    def OnInit(self):
        diffpads_dialog.init_diffpads_dialog(self.board)
        return True
