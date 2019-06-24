#!/usr/bin/env python

import wx, re, pcbnew
from .diffpads_core import add_exits
from .diffpads_gui import DiffPadsGui
from collections import OrderedDict

class DiffPadsDialog(DiffPadsGui):
    def __init__(self, board):
        self.board = board
        self.load_footprints()

        super(DiffPadsDialog, self).__init__(None)

        self.cl_pads.Bind(wx.EVT_CHECKLISTBOX, self.on_cl_pads_checked)
        self.cl_pads.Bind(wx.EVT_LISTBOX, self.on_cl_pads_selected)
        self.btn_check_all.Bind(wx.EVT_BUTTON, self.on_check_all)
        self.btn_uncheck_all.Bind(wx.EVT_BUTTON, self.on_uncheck_all)
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_btn_up)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_btn_down)
        self.btn_left.Bind(wx.EVT_BUTTON, self.on_btn_left)
        self.btn_right.Bind(wx.EVT_BUTTON, self.on_btn_right)

        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.btns_dialogCancel.Bind(wx.EVT_BUTTON, self.on_close_window)
        self.btns_dialogOK.Bind(wx.EVT_BUTTON, self.on_btn_ok)

        # By default, make all pads checked
        self.on_check_all(None)
        self.refresh_ok_button_state()

    def on_cl_pads_checked(self, e):
        idx = e.GetInt()
        self.flat_fp[self.cl_pads.GetString(idx)]["enabled"] = self.cl_pads.IsChecked(idx)
        self.refresh_ok_button_state()
    def on_cl_pads_selected(self, e):
        statuses = set()
        pads = self.get_selected_pads()
        for name in pads:
            statuses.add(self.flat_fp[name]["orientation"])
        if len(statuses) == 1:
            self.set_current(str(statuses.pop()))
        elif len(statuses) == 0:
            self.set_current("None")
        else:
            self.set_current("<...>")
        self.refresh_ok_button_state()

        for name in self.flat_fp:
            ref = self.flat_fp[name]["fp"].GetReference()
            for pad in self.flat_fp[name]["pads"]:
                self.set_pad_selected(ref, pad.GetName(), name in pads)

    def set_pad_selected(self, ref, name, selected=True):
        for mod in self.board.GetModules():
            if mod.GetReference() == ref:
                for pad in mod.Pads():
                    if pad.GetName() == name:
                        if selected:
                            pad.SetSelected()
                        else:
                            pad.ClearSelected()
                        return

    def on_check_all(self, e):
        for i in range(self.cl_pads.GetCount()):
            self.cl_pads.Check(i)
        for name in self.flat_fp:
            self.flat_fp[name]["enabled"] = True
        self.refresh_ok_button_state()
    def on_uncheck_all(self, e):
        for i in range(self.cl_pads.GetCount()):
            self.cl_pads.Check(i, False)
        for name in self.flat_fp:
            self.flat_fp[name]["enabled"] = False
        self.refresh_ok_button_state()

    def on_btn_up(self, e):
        self.set_orientations("up")
    def on_btn_down(self, e):
        self.set_orientations("down")
    def on_btn_left(self, e):
        self.set_orientations("left")
    def on_btn_right(self, e):
        self.set_orientations("right")

    def on_btn_ok(self, e):
        add_exits(self.board, {signal: self.flat_fp[signal]
                               for signal in self.flat_fp
                               if self.flat_fp[signal]["enabled"]})
        pcbnew.Refresh()
        print("Done")

    def on_close_window(self, e):
        self.Destroy()

    def set_current(self, cur):
        self.st_current.SetLabelText("Current: {}".format(cur))

    def get_selected_pads(self):
        return [self.cl_pads.GetString(i) for i in self.cl_pads.GetSelections()]

    def set_orientations(self, orientation):
        for name in self.get_selected_pads():
            self.flat_fp[name]["orientation"] = orientation
        self.on_cl_pads_selected(None)
        self.refresh_ok_button_state()

    def refresh_ok_button_state(self):
        statuses = [self.flat_fp[name]["orientation"]
                    for name in self.flat_fp
                    if self.flat_fp[name]["enabled"]]
        self.btns_dialogOK.Enable(None not in statuses)

    def load_footprints(self):
        # List footprints with their pads
        r = re.compile("^.*_[pPnN]$")
        footprints = {}
        for module in self.board.GetModules():
            # Interesting pads. The footprint is interesting only if its pads
            # are differential and not at an angle multiple of 45 degrees
            pads = {}
            for pad in module.Pads():
                name = pad.GetNetname()
                if r.match(name):
                    name = name[:-2] # remove _P or _N
                    if pads.get(name, None):
                        pads[name].append(pad)
                    else:
                        pads[name] = [pad]
            if len(pads) == 0:
                continue
            # Filter pads without a soulmate
            pads = {name: pads[name] for name in pads if len(pads[name]) == 2}
            if len(pads) == 0:
                continue
            # Check the angle at which the pads are
            odd_pads = {}
            for name in pads:
                [p0, p1] = pads[name]
                vec = p1.GetPosition() - p0.GetPosition()
                if vec.x == 0 or vec.y == 0 or vec.x == vec.y:
                    continue
                odd_pads[name] = {
                    "pads": pads[name],
                    "orientation": None,
                    "enabled": False
                }
            if len(odd_pads) == 0:
                continue
            footprints[module.GetReference()] = OrderedDict({
                "module": module,
                "signals": odd_pads
            })
        fp = OrderedDict(footprints)
        self.footprints = fp

        self.flat_fp = {
            "{} - {}/{} - {}".format(
                ref,
                fp[ref]["signals"][signal]["pads"][0].GetName(),
                fp[ref]["signals"][signal]["pads"][1].GetName(),
                signal
            ) : {
                "fp": fp[ref]["module"],
                "pads": fp[ref]["signals"][signal]["pads"],
                "orientation": None,
                "enabled": False
            }
            for ref in fp for signal in fp[ref]["signals"]
        }

def init_diffpads_dialog(board):
    diffpad_dialog = DiffPadsDialog(board)
    diffpad_dialog.Show(True)
    return diffpad_dialog
