#!/usr/bin/env python

import pcbnew
import math

class Vec:
    def __init__(self, x=0, y=0):
        if type(x) in [pcbnew.wxPoint, Vec]:
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    def __add__(self, o):
        return Vec(self.x + o.x, self.y + o.y)
    def __sub__(self, o):
        return self + (-o)
    def __mul__(self, o):
        return Vec(self.x * o, self.y * o)
    def __truediv__(self, o):
        return Vec(self.x / o, self.y / o)
    def __floordiv__(self, o):
        return Vec(self.x // o, self.y // o)
    def __neg__(self):
        return Vec(-self.x, -self.y)
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    def __ne__(self, o):
        return self.x != o.x and self.y != o.y
    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
    def __imul__(self, o):
        self.x *= o
        self.y *= o
    def __idiv__(self, o):
        self.x /= o
        self.y /= o
    def __ifloordiv__(self, o):
        self.x //= o
        self.y //= o

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    def normalize(self):
        self /= self.len()
        return self
    def normalized(self):
        return self / self.len()

    def rotated(self, angle):
        return Vec(math.cos(angle) * self.x - math.sin(angle) * self.y,
                   math.sin(angle) * self.x + math.cos(angle) * self.y)
    def rotate(self, angle):
        v = self.rotated(angle)
        self.x, self.y = v.x, v.y
        return self

    def normal(self):
        return Vec(-self.y, self.x)

    def cross(self, o):
        return self.x * o.y - self.y * o.x
    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def asWxPoint(self):
        return pcbnew.wxPoint(self.x, self.y)

def line_intersection(a1, b1, a2, b2):
    # p1_t = a1 t_1 + b1
    # p2_t = a2 t_2 + b2
    #
    # ax1 t1 + bx1 = ax2 t2 + bx2
    # ay1 t1 + by1 = ay2 t2 + by2
    #
    # ay2 (ax1 t1 + bx1) = ax2 ay2 t2 + ay2 bx2
    # ax2 (ay1 t1 + by1) = ax2 ay2 t2 + ax2 by2
    #
    # ay2 (ax1 t1 + bx1) - ax2 (ay1 t1 + by1) = ay2 bx2 - ax2 by2
    # t1 (ax1 ay2 - ax2 ay1) + ay2 bx1 - ax2 by1 = ay2 bx2 - ax2 by2
    # t1 = (ax2 by1 + ay2 bx2 - ax2 by2 - ay2 bx1) / (ax1 ay2 - ax2 ay1)
    # t1 = (ax2 (by1 - by2) + ay2 (bx2 - bx1)) / (ax1 ay2 - ax2 ay1)
    t = (a2.x * (b1.y - b2.y) + a2.y * (b2.x - b1.x)) / a1.cross(a2)
    return a1 * t + b1

def cubic_bezier(p0, p1, p2, p3, n=20):
    pts = []
    for i in range(n + 1):
        t = float(i) / float(n)
        p = p0 *              (1 - t) ** 3 + \
            p1 * t      * 3 * (1 - t) ** 2 + \
            p2 * t ** 2 * 3 * (1 - t) + \
            p3 * t ** 3
        pts.append(p)
    return pts

def trace_points(board, points, pad):
    net = pad.GetNet()
    width = pad.GetNetClass().GetDiffPairWidth()

    start = points[0]
    for end in points[1:]:
        track = pcbnew.TRACK(board)
        track.SetStart(start.asWxPoint())
        track.SetEnd(end.asWxPoint())
        track.SetLayer(0) # CHANGEME
        track.SetNet(net)
        track.SetWidth(width)
        board.Add(track)
        start = end

def add_exit(board, fp):
    [pad0, pad1] = fp["pads"]
    orientation = fp["orientation"]

    p0, p1 = Vec(pad0.GetPosition()), Vec(pad1.GetPosition())

    # Determine pad closest to entrypoint
    no_swap = (orientation == "up" and p0.y < p1.y) or \
              (orientation == "down" and p0.y > p1.y) or \
              (orientation == "left" and p0.x < p1.x) or \
              (orientation == "right" and p0.x > p1.x)
    if not no_swap:
        p0, p1 = p1, p0
        pad0, pad1 = pad1, pad0

    p0p1 = p1 - p0
    p0mid = p0p1 / 2
    p_mid = p0 + p0mid

    if orientation in ["up", "down"]:
        p_entry = Vec(p1.x, p0.y)
    else:
        p_entry = Vec(p0.x, p1.y)
    p0ep = p_entry - p0

    trace_tangent = p0ep.normal().normalized()

    # Start point -> trace center
    netclass = pad0.GetNetClass()
    dp_gap, dp_width = netclass.GetDiffPairGap(), netclass.GetDiffPairWidth()
    ep_sp = p0ep.normalized() * (dp_gap + dp_width) / 2.0
    trace_in_start = p_entry - ep_sp
    trace_out_start = p_entry + ep_sp

    cp_in_1 = line_intersection(trace_tangent, trace_in_start,
                                p0mid.normal(), p_mid)
    cp_out_1 = line_intersection(trace_tangent, trace_out_start,
                                 p0ep, p_mid)

    p0r = p0p1.normalized() * pad0.GetSize().x / 2
    p1r = (-p0p1).normalized() * pad1.GetSize().x / 2

    cp_in_2 = p0 + p0r * 1.5
    cp_out_2 = p1 + p1r * 2

    cp_in_end = p0 + p0r
    cp_out_end = p1 + p1r

    inner = cubic_bezier(trace_in_start, cp_in_1, cp_in_2, cp_in_end)
    outer = cubic_bezier(trace_out_start, cp_out_1, cp_out_2, cp_out_end)

    # Add small bits at the start
    if trace_tangent.dot(-p0p1) < 0:
        trace_tangent = -trace_tangent
    inner = [trace_in_start + trace_tangent * (dp_gap + dp_width)] + inner
    outer = [trace_out_start + trace_tangent * (dp_gap + dp_width)] + outer

    # Add down to the pad
    inner.append(p0)
    outer.append(p1)

    # Trace the traces (pun intended)
    trace_points(board, inner, pad0)
    trace_points(board, outer, pad1)

def add_exits(board, flat_fp):
    for sig in flat_fp:
        fp = flat_fp[sig]
        add_exit(board, fp)
