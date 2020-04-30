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
from bookmark.utils import NO_CONTENT_MSG, echo_cancel, echo_error
from leaderf.utils import lfCmd, lfEval


def command__edit(manager):
    if manager._inHelpLines():
        return

    line = manager._instance.currentLine

    if line == NO_CONTENT_MSG:
        return

    name = manager._getDigest(line, 1)
    path = manager._getDigest(line, 2)

    save_context(manager, **{"old_name": name, "path": path})
    input_prompt(
        manager,
        "edit",
        "(Edit) Name: ",
        name,
        [{"prompt": "(Edit) Path: ", "text": path}],
    )


def command___do_edit(manager):
    ctx = get_context()
    new_name = ctx.get("result_set", [])[0]
    if len(new_name.strip()) == 0 or len(ctx["path"].strip()) == 0:
        echo_cancel()

    if new_name in lfEval("leaderf#Bookmark#load_bookmaks()"):
        echo_error("Already exists in bookmark '{}'".format(new_name))

    try:
        lfCmd(
            'call leaderf#Bookmark#_edit("{}", "{}", "{}")'.format(
                ctx["old_name"], new_name, ctx["path"]
            )
        )
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)
    manager._instance._cli.setPattern("")
    manager.refresh()
