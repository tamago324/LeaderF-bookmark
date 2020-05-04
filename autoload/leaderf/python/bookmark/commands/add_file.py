#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bookmark.commands.input import do_command, input_prompt, save_context
from bookmark.utils import echo_cancel, echo_error
from leaderf.utils import lfCmd, lfEval


def command__add_file(manager):
    name = lfEval("expand('%:p:t')")
    path = lfEval("expand('%:p')").replace("\\", "/")
    save_context(manager)
    input_prompt(
        manager,
        "add_file",
        [
            {"prompt": "(Add file) Path: ", "text": path},
            {"prompt": "(Add file) Name: ", "text": name},
        ],
    )


@do_command()
def command___do_add_file(manager, context, results):
    path = results[0]
    name = results[1]
    if len(name.strip()) == 0 or len(path.strip()) == 0:
        echo_cancel()
        return

    if name in lfEval("leaderf#Bookmark#load_bookmaks()"):
        echo_error("Already exists in bookmark '{}'".format(name))
        return

    lfCmd('call leaderf#Bookmark#_add("{}", "{}")'.format(name, path))
