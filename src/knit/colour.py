#!/usr/bin/env python3


class ANSIColor:
    def __init__(self, *color_codes):
        self.color_codes = color_codes
        self.ansi_seq = "".join(map(lambda c: f"\033[{c}m", color_codes))

    def __and__(self, other):
        if not isinstance(other, ANSIColor):
            raise ValueError(
                f"ANSIColor can only be combined with another ANSIColor, not {other.__repr__()}"
            )
        if len(self.color_codes) == 1 and len(other.color_codes) == 1:
            cc_s = list(map(int, [*self.color_codes[0].split(";"), "0"]))
            cc_o = list(map(int, [*other.color_codes[0].split(";"), "0"]))
            return ANSIColor(str(cc_s[0] or cc_o[0]) + ";" + str(cc_s[1] or cc_o[1]))
        return ANSIColor(*self.color_codes, *other.color_codes)

    def __or__(self, other):
        if not isinstance(other, str):
            raise ValueError(
                f"ANSIColor can only be applied to strings, not {other.__repr__()}"
            )
        return self.ansi_seq + other + "\033[0m"


bold = ANSIColor("1")

red = ANSIColor("0;31")
green = ANSIColor("0;32")
yellow = ANSIColor("0;33")
blue = ANSIColor("0;34")
magenta = ANSIColor("0;35")
cyan = ANSIColor("0;36")
grey = ANSIColor("0;90")

bred = bold & red
bgreen = bold & green
byellow = bold & yellow
bblue = bold & blue
bmagenta = bold & magenta
bcyan = bold & cyan
bgrey = bold & grey
