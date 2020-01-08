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

function! leaderf#Bookmark#add(path, ...) abort
    let l:path = a:path
    if has('win32')
        let l:path = substitute(expand(l:path), '\\', '/', 'g')
    endif

    let l:name = a:0 == 0 ? fnamemodify(l:path, ':t') : a:1

    " Add when not exists.
    let l:bookmarks = s:load_bookmaks()
    if has_key(l:bookmarks, l:path)
        echohl ErrorMsg
        execute printf('echo "Already exists in bookmark. (%s)"', l:path)
        echohl None
        return
    endif

    let l:bookmarks[l:path] = l:name
    let l:encoded = json_encode(l:bookmarks)
    call writefile([l:encoded], g:Lf_BookmarkFilePath)
    execute printf('echo "Success added bookmark. (%s => %s)"', l:name, l:path)
endfunction

function! leaderf#Bookmark#delete(path) abort
    let l:path = a:path
    if has('win32')
        let l:path = substitute(expand(l:path), '\\', '/', 'g')
    endif

    let l:bookmarks = s:load_bookmaks()
    if !has_key(l:bookmarks, l:path)
        echohl ErrorMsg
        execute printf('echo "Bookmark with path \"%s\" does not exist."', l:path)
        echohl None
        return
    endif

    let yn = input(printf('Delete ''%s'' (y/N)? ', l:bookmarks[l:path]))
    echo "\n"
    if empty(yn) || yn ==? 'n'
        echo 'Cancelled.'
        return
    endif

    let l:deleted = remove(l:bookmarks, l:path)
    let l:encoded = json_encode(l:bookmarks)
    call writefile([l:encoded], g:Lf_BookmarkFilePath)
    execute printf('echo "Success deleted bookmark. (%s)"', l:path)
endfunction

" {path: name, path: name}
function! s:load_bookmaks() abort
    if !filereadable(g:Lf_BookmarkFilePath)
        return {}
    endif
    let l:lines = readfile(g:Lf_BookmarkFilePath)
    if l:lines == [] | return {} | endif

    return json_decode(l:lines[0])
endfunction
