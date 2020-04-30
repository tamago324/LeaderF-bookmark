#!/usr/bin/env python
# -*- coding: utf-8 -*-

from leaderf.utils import escQuote, lfCmd

NO_CONTENT_MSG = " No content!"


def echo_cancel():
    lfCmd("echon ' Canceled.'")


def echo_error(msg):
    lfCmd(
        "echohl ErrorMsg | redraw | echon ' [LeaderF] {}' | echohl NONE".format(
            escQuote(msg)
        )
    )
