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
        bookmark_filepath = lfEval('g:Lf_BookmarkFilePath')
        if not os.path.exists(bookmark_filepath):
            return []

        with lfOpen(bookmark_filepath) as f:
            bookmarks = json.load(f)

        return ['{} {}'.format(v, k) for k, v in bookmarks.items()]

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
        cmd = line.split(None, 1)[0]
        lfCmd("norm! `" + cmd)
        lfCmd("norm! zz")
        lfCmd("setlocal cursorline! | redraw | sleep 100m | setlocal cursorline!")

    def _getDigest(self, line, mode):
        if not line:
            return ''
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help


#*****************************************************
# bookmarkExplManager is a singleton
#*****************************************************
bookmarkExplManager = BookmarkExplManager()

__all__ = ['bookmarkExplManager']

