#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import json
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *


#*****************************************************
# BookmarkExplorer
#*****************************************************
class BookmarkExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        bookmark_filepath = lfEval("g:Lf_BookmarkFilePath")
        if not os.path.exists(bookmark_filepath):
            return []

        with lfOpen(bookmark_filepath) as f:
            bookmarks = json.load(f)

        if len(bookmarks) == 0:
            return []

        # from mruExpl.py
        _max_name_len = max(
            int(lfEval("strdisplaywidth('{}')".format(escQuote(getBasename(line)))))
            for line in bookmarks.values()
        )
        lines = []
        for path, name in bookmarks.items():
            space_num = _max_name_len - int(
                lfEval("strdisplaywidth('{}')".format(escQuote(name)))
            )
            lines.append('{}{} "{}"'.format(name, " " * space_num, path))
        return lines

    def getStlCategory(self):
        return "Bookmark"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))


#*****************************************************
# BookmarkExplManager
#*****************************************************
class BookmarkExplManager(Manager):
    def __init__(self):
        super(BookmarkExplManager, self).__init__()

    def _getExplClass(self):
        return BookmarkExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Bookmark#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        cmd = lfEval("g:Lf_BookmarkAcceptSelectionCmd")
        path = self._getDirPath(line)
        lfCmd("{} {}".format(cmd, path))

    def delete(self, *args, **kwargs):
        instance = self._getInstance()
        line = instance.currentLine
        path = self._getDirPath(line)
        instance.exitBuffer()
        try:
            lfCmd('call leaderf#Bookmark#delete("{}")'.format(path))
        except KeyboardInterrupt:
            pass
        except vim.error as e:
            lfPrintError(e)

    def _getDigest(self, line, mode):
        if not line:
            return ""
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" d : delete bookmark under cursor')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _getDirPath(self, line):
        pos = line.find(' "')
        return line[pos + 2:-1]

#*****************************************************
# bookmarkExplManager is a singleton
#*****************************************************
bookmarkExplManager = BookmarkExplManager()

__all__ = ["bookmarkExplManager"]
