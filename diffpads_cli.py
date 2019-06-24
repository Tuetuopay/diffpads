#!/usr/bin/env python

import .diffpads_app, pcbnew, sys

if len(sys.argv) < 3:
    print("Usage: {} <kicad pcb file> <output file>".format(sys.argv[0]))
    exit(-1)
board = pcbnew.LoadBoard(sys.argv[1])
app = diffpads_app.DiffPadsApp(board)
app.MainLoop()
board.Save(sys.argv[2])
