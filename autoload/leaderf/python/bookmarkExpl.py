#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import os.path

from bookmark.cmd import Cmd
from bookmark.utils import NO_CONTENT_MSG, echo_error
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.utils import *


# *****************************************************
# BookmarkExplorer
# *****************************************************
class BookmarkExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        bookmark_filepath = lfEval("g:Lf_BookmarkFilePath")
        if not os.path.exists(bookmark_filepath):
            return []

        try:
            with lfOpen(bookmark_filepath) as f:
                bookmarks = json.load(f)
        except json.decoder.JSONDecodeError:
            return []

        if len(bookmarks) == 0:
            return [NO_CONTENT_MSG]

        # from mruExpl.py
        _max_name_len = max(
            int(lfEval("strdisplaywidth('{}')".format(escQuote(getBasename(line)))))
            for line in bookmarks.values()
        )
        lines = []
        for name, path in bookmarks.items():
            space_num = _max_name_len - int(
                lfEval("strdisplaywidth('{}')".format(escQuote(name)))
            )
            lines.append("{}{} | {}".format(name, " " * space_num, path))

        self._content = lines
        return lines

    def getStlCategory(self):
        return "Bookmark"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def supportsNameOnly(self):
        return True


# *****************************************************
# BookmarkExplManager
# *****************************************************
class BookmarkExplManager(Manager):
    def __init__(self):
        super(BookmarkExplManager, self).__init__()
        self._command = Cmd(self)

    def _getExplClass(self):
        return BookmarkExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Bookmark#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        cmd = lfEval("g:Lf_BookmarkAcceptSelectionCmd")
        path = self._getDigest(line, 2)
        lfCmd("{} {}".format(cmd, path))

    def do_command(self, cmd_name, silent=False):
        if self._command.contains(cmd_name):
            return self._command.exec(cmd_name)
        elif not silent:
            echo_error("Not found command: {}".format(cmd_name))

    def _cmdExtension(self, cmd_name):
        """
        this function can be overridden to add new cmd
        if return true, exit the input loop

        Use for LfCli#input()
        """
        if self._command.contains(cmd_name):
            return self.do_command(cmd_name)

    def _getDigest(self, line, mode):
        if not line:
            return ""
        if mode == 0:
            return line
        elif mode == 1:
            start_pos = line.find(" | ")
            return line[:start_pos].rstrip()
        else:
            start_pos = line.find(" | ")
            return line[start_pos + 3 :]

    def _getDigestStartPos(self, line, mode):
        if not line:
            return 0

        if mode == 2:
            start_pos = line.find(" | ")
            return lfBytesLen(line[: start_pos + 3])
        else:
            return 0

    def _afterEnter(self):
        super(BookmarkExplManager, self)._afterEnter()
        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_bookmarkPath'', ''\s+\zs\| .\+'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
        else:
            id = int(lfEval("matchadd('Lf_hl_bookmarkPath', '\s+\zs\| .\+')"))
            self._match_ids.append(id)

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" d : delete bookmark under cursor')
        help.append('" e : edit bookmark under cursor')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help


# *****************************************************
# bookmarkExplManager is a singleton
# *****************************************************
bookmarkExplManager = BookmarkExplManager()

__all__ = ["bookmarkExplManager"]
