#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bookmark.commands.input import do_command, input_prompt, save_context
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

    save_context(manager, **{"old_name": name})
    input_prompt(
        manager,
        "edit",
        [
            {"prompt": "(Edit) Path: ", "text": path},
            {"prompt": "(Edit) Name: ", "text": name},
        ],
    )


@do_command()
def command___do_edit(manager, context, results):
    new_path = results[0]
    new_name = results[1]

    if len(new_name.strip()) == 0 or len(new_path.strip()) == 0:
        echo_cancel()
        return

    if context.get("old_name") != new_name and new_name in lfEval(
        "leaderf#Bookmark#load_bookmaks()"
    ):
        echo_error("Already exists in bookmark '{}'".format(new_name))
        return

    lfCmd(
        'call leaderf#Bookmark#_edit("{}", "{}", "{}")'.format(
            context["old_name"], new_name, new_path
        )
    )
