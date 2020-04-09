" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "bookmark",
            \   "help": "navigate the bookmarks",
            \   "manager_id": "leaderf#Bookmark#managerId",
            \   "arguments": [
            \   ]
            \ }

" In order that `Leaderf bookmark` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfBookmark Leaderf bookmark

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfBookmark", "navigate the bookmarks")
