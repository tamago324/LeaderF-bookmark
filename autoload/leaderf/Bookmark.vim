" ============================================================================
" File:        Bookmark.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from bookmarkExpl import *"

function! leaderf#Bookmark#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "bookmarkExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "bookmarkExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "bookmarkExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "bookmarkExplManager.quit()"<CR>
    nnoremap <buffer> <silent> <Tab>         :exec g:Lf_py "bookmarkExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "bookmarkExplManager.toggleHelp()"<CR>
    nnoremap <buffer> <silent> d             :exec g:Lf_py "bookmarkExplManager.delete()"<CR>
    nnoremap <buffer> <silent> e             :exec g:Lf_py "bookmarkExplManager.edit()"<CR>
    if has_key(g:Lf_NormalMap, "Bookmark")
        for i in g:Lf_NormalMap["Bookmark"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Bookmark#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(bookmarkExplManager)")
    else
        return py3eval("id(bookmarkExplManager)")
    endif
endfunction

function! leaderf#Bookmark#NormalModeFilter(winid, key) abort
    let key = get(g:Lf_KeyDict, get(g:Lf_KeyMap, a:key, a:key), a:key)

    if key !=# "g"
        call win_execute(a:winid, "let g:Lf_Bookmark_is_g_pressed = 0")
    endif

    if key ==# "j" || key ==? "<Down>"
        call win_execute(a:winid, "norm! j")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "k" || key ==? "<Up>"
        call win_execute(a:winid, "norm! k")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<PageUp>" || key ==? "<C-B>"
        call win_execute(a:winid, "norm! \<PageUp>")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<PageDown>" || key ==? "<C-F>"
        call win_execute(a:winid, "norm! \<PageDown>")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "g"
        if get(g:, "Lf_Bookmark_is_g_pressed", 0) == 0
            let g:Lf_Bookmark_is_g_pressed = 1
        else
            let g:Lf_Bookmark_is_g_pressed = 0
            call win_execute(a:winid, "norm! gg")
            exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
            redraw
        endif
    elseif key ==# "G"
        call win_execute(a:winid, "norm! G")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<C-U>"
        call win_execute(a:winid, "norm! \<C-U>")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<C-D>"
        call win_execute(a:winid, "norm! \<C-D>")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<LeftMouse>"
        if has('patch-8.1.2266')
            call win_execute(a:winid, "exec v:mouse_lnum")
            call win_execute(a:winid, "exec 'norm!'.v:mouse_col.'|'")
            exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
            redraw
        endif
    elseif key ==? "<ScrollWheelUp>"
        call win_execute(a:winid, "norm! 3k")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        redraw
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<ScrollWheelDown>"
        call win_execute(a:winid, "norm! 3j")
        exec g:Lf_py "bookmarkExplManager._cli._buildPopupPrompt()"
        redraw
        exec g:Lf_py "bookmarkExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "q" || key ==? "<ESC>"
        exec g:Lf_py "bookmarkExplManager.quit()"
    elseif key ==# "i" || key ==? "<Tab>"
        call leaderf#ResetPopupOptions(a:winid, 'filter', 'leaderf#PopupFilter')
        exec g:Lf_py "bookmarkExplManager.input()"
    elseif key ==# "o" || key ==? "<CR>" || key ==? "<2-LeftMouse>"
        exec g:Lf_py "bookmarkExplManager.accept()"
    elseif key ==? "<F1>"
        exec g:Lf_py "bookmarkExplManager.toggleHelp()"
    elseif key ==? "d"
        exec g:Lf_py "bookmarkExplManager.delete()"
    elseif key ==? "e"
        exec g:Lf_py "bookmarkExplManager.edit()"
    endif

    return 1
endfunction



" =====================
" add
" =====================
function! leaderf#Bookmark#add(name, path) abort
    let l:path = has('win32') ? substitute(expand(a:path), '\\', '/', 'g') : a:path

    " Add when not exists.
    let l:bookmarks = s:load_bookmaks()
    if has_key(l:bookmarks, a:name)
        call s:echoerr(printf('echo "Already exists in bookmark. (%s)"', a:name))
        return
    endif

    call s:add(a:name, l:path)
    execute printf('echo "Success added bookmark. (%s => %s)"', a:name, l:path)
endfunction


" ---------------------
" add here
" ---------------------
function! leaderf#Bookmark#add_here(...) abort
    let l:path = has('win32') ? substitute(expand(getcwd()), '\\', '/', 'g') : getcwd()
    let l:name = get(a:, 1, fnamemodify(l:path, ':t'))

    let yn = input(printf('Add ''%s'' (y/N)? ', l:name))
    echo "\n"
    if empty(yn) || yn ==? 'n'
        echo 'Cancelled.'
        return
    endif

    call leaderf#Bookmark#add(l:name, l:path)
endfunction



function! s:add(name, path) abort
    let l:path = has('win32') ? substitute(expand(a:path), '\\', '/', 'g') : a:path
    let l:bookmarks = s:load_bookmaks()
    let l:bookmarks[a:name] = l:path
    call s:write(l:bookmarks)
endfunction




" =====================
" delete
" =====================
function! leaderf#Bookmark#delete(name) abort
    if !has_key(s:load_bookmaks(), a:name)
        call s:echoerr(printf('echo "Not exists in bookmark. (%s)"', a:name))
        return
    endif

    let yn = input(printf('Delete ''%s'' (y/N)? ', a:name))
    echo "\n"
    if empty(yn) || yn ==? 'n'
        echo 'Cancelled.'
        return
    endif

    call s:delete(a:name)
    redraw!
    echo  printf('Success deleted bookmark. (%s)', a:name)
endfunction


function! s:delete(name) abort
    let l:bookmarks = s:load_bookmaks()
    let l:deleted = remove(l:bookmarks, a:name)
    call s:write(l:bookmarks)
endfunction



" =====================
" edit
" =====================
function! leaderf#Bookmark#edit(name) abort
    let l:bookmarks = s:load_bookmaks()

    if !has_key(s:load_bookmaks(), a:name)
        call s:echoerr(printf('echo "Not exists in bookmark. (%s)"', a:name))
        return
    endif

    " name
    let l:new_name = input('Name: ', a:name)
    if empty(l:new_name)
        return
    endif

    " path
    let l:path = input('Path: ', l:bookmarks[a:name])
    if empty(l:path)
        return
    endif

    call s:edit(a:name, l:new_name, l:path)
    redraw!
    echo printf('Success edited bookmark. (%s)', l:new_name)
endfunction


function! s:edit(old_name, new_name, path) abort
    let l:bookmarks = s:load_bookmaks()
    let l:path = has('win32') ? substitute(expand(a:path), '\\', '/', 'g') : a:path

    if !has_key(l:bookmarks, a:new_name)
        call s:delete(a:old_name)
    endif
    call s:add(a:new_name, a:path)
endfunction




" =====================
" load bookmarks
" =====================

" {path: name, ...}
function! s:load_bookmaks() abort
    if exists('g:Lf_Bookmarks')
        return g:Lf_Bookmarks
    endif

    if !filereadable(g:Lf_BookmarkFilePath)
        let g:Lf_Bookmarks = {}
        return g:Lf_Bookmarks
    endif

    let l:lines = readfile(g:Lf_BookmarkFilePath)
    if l:lines == [] | return {} | endif
    let g:Lf_Bookmarks = json_decode(l:lines[0])
    return g:Lf_Bookmarks
endfunction


" =====================
" echo error
" =====================
function! s:echoerr(msg) abort
    echohl ErrorMsg
    execute a:msg
    echohl None
endfunction


" =====================
" write
" =====================
function! s:write(bookmarks) abort
    let l:encoded = json_encode(a:bookmarks)
    call writefile([l:encoded], g:Lf_BookmarkFilePath)
endfunction


" =====================
" complete
" =====================
function! leaderf#Bookmark#name_complete(arglead, cmdline, cursorpos) abort
    return join(keys(s:load_bookmaks()), "\n")
endfunction
