#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from bookmark.utils import echo_cancel
import re

from bookmark.commands.input import (
    command___input_cancel,
    do_command,
    input_prompt,
    save_context,
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
    input_prompt(
        manager, "delete", [{"prompt": "Delete {}? Y[es]/n[o]: ".format(name)}]
    )


@do_command()
def command___do_delete(manager, context, results):
    if not yes(results[0]):
        command___input_cancel(manager)
        return

    lfCmd("call leaderf#Bookmark#_delete('{}')".format(context["name"]))


def yes(result, default_yes=True):
    if default_yes and result == "":
        result = "y"
    return re.search(r"^[yY](e?s?)?$", result)
