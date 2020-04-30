#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from bookmark.utils import echo_cancel
import re

from bookmark.commands.input import (
    command___input_cancel,
    get_context,
    input_prompt,
    restore_context,
    save_context,
    switch_normal_mode,
    do_command,
)
from bookmark.utils import NO_CONTENT_MSG
from leaderf.utils import lfCmd


def command__delete(manager):
    line = manager._instance.currentLine

    if manager._inHelpLines():
        return

    if line == NO_CONTENT_MSG:
        return

    name = manager._getDigest(line, 1)

    save_context(manager, **{"current_line": line, "name": name})
    # confirm
    input_prompt(manager, "delete", "Delete {}? Y[es]/n[o]: ".format(name))


@do_command
def command___do_delete(manager, results):
    if not yes(results[0]):
        command___input_cancel(manager)
        return

    ctx = get_context()
    try:
        lfCmd("call leaderf#Bookmark#_delete('{}')".format(ctx["name"]))
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)
    manager._instance._cli.setPattern("")
    manager.refresh()


def yes(result, default_yes=True):
    if default_yes and result == "":
        result = "y"
    return re.search(r"^[yY](e?s?)?$", result)
