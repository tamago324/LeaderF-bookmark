" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

let g:Lf_BookmarkFilePath = expand(get(g:, 'Lf_BookmarkFilePath', '~/.LfBookmarks'))
if has('win32')
    let g:Lf_BookmarkFilePath = substitute(g:Lf_BookmarkFilePath, '\\', '/', 'g')
endif

let g:Lf_BookmarkAcceptSelectionCmd = get(g:, 'Lf_BookmarkAcceptSelectionCmd', 'edit')

command! -nargs=+ -complete=file BookmarkAdd call leaderf#Bookmark#add(<f-args>)
