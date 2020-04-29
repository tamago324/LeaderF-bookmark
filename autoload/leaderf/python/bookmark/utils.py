#!/usr/bin/env python
# -*- coding: utf-8 -*-

from leaderf.utils import lfCmd, escQuote


def echo_cancel():
    lfCmd("echon ' Canceled.'")


def echo_error(msg):
    lfCmd(
        "echohl ErrorMsg | redraw | echon ' [LeaderF] {}' | echohl NONE".format(
            escQuote(msg)
        )
    )
