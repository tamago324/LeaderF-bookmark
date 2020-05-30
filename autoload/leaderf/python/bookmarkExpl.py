#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import os.path

from bookmark.cmd import Cmd
from bookmark.utils import NO_CONTENT_MSG, echo_error
from leaderf.devicons import *
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.utils import *


# *****************************************************
# BookmarkExplorer
# *****************************************************
class BookmarkExplorer(Explorer):
    def __init__(self):
        self._prefix_length = 0

    def getContent(self, *args, **kwargs):
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        bookmark_filepath = lfEval("expand(get(g:, 'Lf_BookmarkFilePath', '~/.LfBookmarks'))")
        if not os.path.exists(bookmark_filepath):
            return [NO_CONTENT_MSG]

        try:
            with lfOpen(bookmark_filepath) as f:
                bookmarks = json.load(f)
        except json.decoder.JSONDecodeError:
            return [NO_CONTENT_MSG]

        if len(bookmarks) == 0:
            return [NO_CONTENT_MSG]

        if lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == '1':
            self._prefix_length = webDevIconsStrLen()

        # from mruExpl.py
        _max_name_len = max(
            int(lfEval("strdisplaywidth('{}')".format(escQuote(getBasename(line)))))
            for line in bookmarks.values()
        )
        if lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == "1":
            _max_name_len += webDevIconsStrLen()

        lines = []
        for name, path in bookmarks.items():
            space_num = _max_name_len - int(
                lfEval("strdisplaywidth('{}')".format(escQuote(name)))
            )
            lines.append(
                "{}{}{} | {}".format(
                    webDevIconsGetFileTypeSymbol(path, os.path.isdir(path)),
                    name,
                    " " * space_num,
                    path,
                )
            )

        self._content = lines
        return lines

    def getStlCategory(self):
        return "Bookmark"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def supportsNameOnly(self):
        return True

    def getPrefixLength(self):
        return self._prefix_length


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
        path = self._getDigest(line, 2)

        if os.path.isdir(path):
            if lfEval("has_key(g:, 'Lf_BookmarkAcceptSelectionCmd')") == "1":
                # This will be removed in the future.
                cmd = lfEval("get(g:, 'Lf_BookmarkAcceptSelectionCmd', 'edit')")
            else:
                cmd = lfEval("get(g:, 'Lf_BookmarkDirAcceptSelectionCmd', 'edit')")
            lfCmd("%s %s" % (cmd, escSpecial(path)))
            return

        # file
        try:
            if kwargs.get("mode", "") != "t" or (
                lfEval("get(g:, 'Lf_DiscardEmptyBuffer', 0)") == "1"
                and len(vim.tabpages) == 1
                and len(vim.current.tabpage.windows) == 1
                and vim.current.buffer.name == ""
                and len(vim.current.buffer) == 1
                and vim.current.buffer[0] == ""
                and not vim.current.buffer.options["modified"]
            ):

                if vim.current.buffer.options["modified"]:
                    lfCmd("hide edit %s" % escSpecial(path))
                else:
                    lfCmd("edit %s" % escSpecial(path))
            else:
                lfCmd("tab drop %s" % escSpecial(path))
        except vim.error as e:  # E37
            lfPrintError(e)

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
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, return the full path
                  1, return the name only
                  2, return the directory name
        """
        if not line:
            return ""

        prefix_len = self._getExplorer().getPrefixLength()
        if mode == 0:
            return line[prefix_len:]
        elif mode == 1:
            start_pos = line.find(" | ")
            return line[prefix_len:start_pos].rstrip()
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
            return self._getExplorer().getPrefixLength() - webDevIconsStrLen() + webDevIconsBytesLen()

    def _afterEnter(self):
        super(BookmarkExplManager, self)._afterEnter()
        winid = None

        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_bookmarkPath'', ''| [^|]\+$'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)

            if lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == "1":
                lfCmd(
                    """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_bookmarkDirIcon'', ''^%s'')')"""
                    % (
                        self._getInstance().getPopupWinId(),
                        webDevIconsGetFileTypeSymbol("", isdir=True),
                    )
                )
                id = int(lfEval("matchid"))
                self._match_ids.append(id)

            winid = self._getInstance().getPopupWinId()
        else:
            id = int(lfEval(r"matchadd('Lf_hl_bookmarkPath', '| [^|]\+$')"))
            self._match_ids.append(id)

            if lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == "1":
                id = int(
                    lfEval(
                        "matchadd('Lf_hl_bookmarkDirIcon', '^%s')"
                        % webDevIconsGetFileTypeSymbol("", isdir=True)
                    )
                )
                self._match_ids.append(id)

        # devicons
        if lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == "1":
            self._match_ids.extend(
                matchaddDevIconsExtension(
                    r"__icon__\ze\s\+.\{-}\.__name__\($\|\s\)", winid
                )
            )
            self._match_ids.extend(
                matchaddDevIconsExact(r"__icon__\ze\s\+__name__\($\|\s\)", winid)
            )
            self._match_ids.extend(
                matchaddDevIconsDefault(r"__icon__\ze\s\+\S\+\($\|\s\)", winid)
            )

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" N : add file bookmark')
        help.append('" K : add dir bookmark')
        help.append('" D : delete bookmark under cursor')
        help.append('" E : edit bookmark under cursor')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help


# *****************************************************
# bookmarkExplManager is a singleton
# *****************************************************
bookmarkExplManager = BookmarkExplManager()

__all__ = ["bookmarkExplManager"]
