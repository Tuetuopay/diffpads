#!/usr/bin/env python

# Diff Pads for pcbnew using bezier curves as an exit

from pcbnew import ActionPlugin, GetBoard
from .diffpads_dialog import init_diffpads_dialog

class DiffPadsPlugin(ActionPlugin):
    def defaults(self):
        self.name = "DiffPads"
        self.category = "Modify PCB"
        self.description = "Creates good-looking differential pads exits"

    def Run(self):
        init_diffpads_dialog(GetBoard())
