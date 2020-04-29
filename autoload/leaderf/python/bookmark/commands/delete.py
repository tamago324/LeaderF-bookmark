#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bookmark.commands.input import (
    command___input_cancel,
    get_context,
    input_prompt,
    restore_context,
    save_context,
    switch_normal_mode,
)
from leaderf.utils import lfCmd
# from bookmark.utils import echo_cancel
import re


def command__delete(manager):
    if manager._inHelpLines():
        return

    line = manager._instance.currentLine
    name = manager._getDigest(line, 1)

    save_context(manager, **{'current_line': line, 'name': name})
    # confirm
    input_prompt(manager, "delete", "Delete {}? Y[es]/n[o]: ".format(name))


def command___do_delete(manager):
    result = manager._instance._cli.pattern

    if not yes(result):
        command___input_cancel(manager)
        return

    ctx = get_context()
    try:
        lfCmd("call leaderf#Bookmark#_delete('{}')".format(ctx["name"]))
        manager.refresh()
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)


def yes(result, default_yes=True):
    if default_yes and result == "":
        result = "y"
    return re.search(r"^[yY](e?s?)?$", result)
