" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

let g:Lf_BookmarkFilePath = expand(get(g:, 'Lf_BookmarkFilePath', '~/.LfBookmarks'))
let g:Lf_BookmarkFilePath = 
\   has('win32') 
\       ? substitute(g:Lf_BookmarkFilePath, '\\', '/', 'g')
\       : g:Lf_BookmarkFilePath

let g:Lf_BookmarkAcceptSelectionCmd = get(g:, 'Lf_BookmarkAcceptSelectionCmd', 'edit')
