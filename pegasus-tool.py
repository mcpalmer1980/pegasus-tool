'''
GUI program for maintaining Pegasus-FE assets and metadata

menu_window
help_window
    get_doc
    get_menu_tooltips

add_assets_window
    add_assets

backup_metadata_window
    popup_get_folder

check_files_window    
    delete_clicked
    get_file_report
    get_metadata_exts
    launch clicked
    launch file
    scan_files
    scan_metadata

edit_genre_window
    backup_metadata
    export_genre_window
    get_metadatas
    scan_genres
    update_metadata_genres

hide_disks

make_mix_window
    load_image
    make_mix_images
    scan_for_mix

export_xml_window
    export_xml
    update_xml_images

option_window
    update_history
    Options class
        load
        save

remove_assets

import_xml_window
    import_xml
   
'''
import sys, os, json, pyperclip, tempfile, subprocess, re, inspect
import xml.etree.cElementTree as ET
import PySimpleGUI as sg
from re import match
import multiprocessing as mp

icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAS7SURBVFhH1ZdtqN5zGMcPkYTGC/KG8vBCycZ9zn2ed56fz6IwvBCSNKYk0WaKUyi8mIeEF5SViGPyELGVFRbrmCK2JZRZoTwNsw37+Xz+u6+z/7nP/959W97sX5/OfX7/3++6vr/ruv6/h6bD8mlubpYj4Tg4Fc6Es+F0OAmOhqzf//KEMTgGFsIyeArehW2wHXbA1/AxvAyroAsUeWhiYiAsgKWg4e9hH6QG+BXehIvhWGhcSKWzoZyA9bAbipw0wi5YA2fBwUVEBzC3q8FZFBmtSwkugPMrv2nbBD7FIuIFnAvrYF6ow2jF4Lx3OhP/72lpSZe1taVbOjvTYLkcY2bgHJgrIhqA8VmnOcZFA/0Yuhyjffxt4f9wWIZh2q5pb0/3LF6cXurvT5+MjKQfx8fT35OT6aGenkx4xdaLcDzsd14qlcK5OdoIcxyLzheWSunajo703dhY+hzjrwwMpAdx9gjG3x4cTF+OjqbfJybSPhymKj6j/8CBKOyBK2G/AH/ACfA8zDqsDuelzPyx3t70VxhesiRzljnkd7VTcfZG4YPh4XRha2s+Chb2gnAuy2EvpFaIcN7LDNdWhTOMf0rbXd3d6X76bCcqtu0mAjv4/f7QUHq6ry/d3tWVLkF4FxPQdo6fYSicu5JthUzhnRj96iDhFN9dTzrOIy2LGLOcQnuYVNxI2yQz7cChtqyTESZjX4VUUhDcHQJWRqMhf4IwF4U0wmk01jA7CzIM5lOmY9HxG9TJN0TkTwRPMbFIaYVpnZ8CH0ZjXkCEc2NVOK2H6F8L7dxMVPZUxCtgGVGoErBBAeOwMxpV7sBHCecNDJggnNaEX4DhbMS5OOY1Zh/RM6WjuYhVeEcBU7mGDEWYV/N4EQJcSJ4kKu8RiVcx2llHhLO8jWhZJyHAlBX0fUEBLgqzjSq8iup/jsr/iE/nB3Ke/+xmaKslIOrAgouvQr7l91JS58SqxkwpYEO+MV8DYWCWGgLCcRusYubWTYyxjvyUq0Ivpn28roB/4Bei4MpnTlfiwGXX2djXv90Iuo5Zv877Xbmw7wWLt533BQIs/JMVMJ1rzAy6sGxmps8y2DXhikrlh8PYZFYg5hn6mKrfco7F/D/ORIxWgXNZAdkyPK8InZEFuIjKd7Br+NW5VdEV8KeqVTFw4drCe4vQSNVwvgVc/DIBQ+CymL10gFunK5uf4ro6m0xguLfRz9VwjPEFBRe43Lvs6zsTcCK4MWQdDPNqjMxWfh12ImyaqNzKjN0/dFxj1oEbnhvfnJ3QrdEt8kARVjmymv20thLefOgNd6/pYlwdx+JWnx3LPALkBXg4yNYDBVg8VvMXhPQtUuBhwlXR0N5EahSTF9BXu9DyeMjBfCX08UQDeEya0ZD7vlvxEA4tJEUFY6yM91GMfikPgF+Cnxlja+GxzuOdx7y5zuOJF+CzyTzqrGhWtuUFSXWfHB5oPdh6wC12Hk90AHPkEfoPKDLaCB7hLexJyG5JDT3lcjlEeInwMuGlotFjuaH20uLlxUuMl5nM3n9+YiB4rfJ6dQeshc3g9ctrmNcxr2Vez7ymeV3z2ub17dAcFz1hDI4CL56ngWk6A8ytIo+AyojD6mlq+hevylK0ZElvugAAAABJRU5ErkJggg=='
OPT_LABEL = 20
OPT_WIDTH = 44
meta_filename = 'metadata.pegasus.txt'
disc_pattern = '.*\([dD]is[ck] [0-9]\)$'

def menu_window():
    '''
    Displays a list of tools and opens them when clicked.
    '''
    import inspect
    
    tips = get_menu_tooltips()
    gw = 4 # grid width
    font, size = opts['Font']
    bigfont = font, int(size*1.5), 'bold'
    grid = [[sg.Image(icon), 
            sg.Text('Pegasus Tool', font=bigfont), sg.Push(),
            sg.Button('?', font=(font, size, 'bold'), key='help')]]
    values = list(tools.keys())
    size = len(max(values, key=len))
    for y in range(len(values)+1//gw):
        row = []
        for x in range(gw):
            if y*gw + x < len(values):
                i = y*gw+x
                row.append(sg.Button(values[i], size=size, tooltip=tips[i],
                          disabled=not bool(windows[values[i]])))
        grid.append(row)            

    window = sg.Window('Main Menu', grid, finalize=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,):
            window.close()
            break
        elif event in windows.keys():
            launch_tool(event)
        elif event == 'help':
            launch_tool(event)


def help_window():
    '''
    This Pegasus tool was designed to help manage metadata files and assets
    used by the Pegasus Frontend program. It can help find missing image
    assets, edit genres, and convert to or from EmultionStation gamelist.xml
    files. 

    For ideal functionality you should keep all your rom folders under a
    shared base folder, such as Roms. Inside each rom folder should be a
    media folder, with subfolders such as screenshot, box2dfront, and
    videos inside of it. Each of those should have an image file that
    matches the rom file names. 

    Add Assets | Add asset links to metadata file 
    Backup Metadata | Backup all metadata files to zip archive 
    Check Files | Find missing and extra files in a rom path 
    Edit Genres | Rename genres within one or more metadata files 
    Export XML | Export gamelist.xml based on metadata.pegasus.txt 
    Hide Disks | Hides multi-disc ISOs and creates M3U playlist
    Import XML | Create Pegasus metadata based on a gamelist.xml 
    Make Image Mixes | Create collage from screenshot, box, and logo 
    Options |  Edit global options and access Theme selector  
    Remove Assets | Remove asset links from metadata
    '''
    def print_doc(title, text, clear=False):
        if clear:
            window['text'].update('')
        outp.print(title, font=bigfont, justification='c', c=bigcolor)
        for l in text.split('\n'):
            if ' | ' in l:
                b, a = l.split(' | ', 1)
                sep = ' - ' if a else ''
                outp.print(b, font=opts['Font'] + ['bold'], end='')
                outp.print(sep, a)
            else:
                outp.print(l)
    def print_all():
        window['text'].update('')
        for w in ['Pegasus Tool Help'] + list(windows.keys()):
            doc = get_doc(windows.get(w, help_window))
            if doc:
                print_doc(w, doc)
        outp.set_vscroll_position(0)


    layout = [[sg.Multiline('Loading...', size=(60, 15), disabled=True, 
               enable_events=True, key='text')],
               [sg.Combo(['...']+list(windows.keys()), default_value='Jump to...',
                         key='jump', enable_events=True, readonly=True),
                         sg.Push(), sg.Button('Done')]]
    window = sg.Window('Help', layout, finalize=True)
    outp = window['text']
    bigfont = opts['Font'][0], int(opts['Font'][1] * 1.5), 'bold'
    bigcolor = sg.theme_input_background_color(), sg.theme_input_text_color()
    window.read(20)
    print_all()
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Done'):
            break
        elif event == 'jump':
            clicked = values['jump']
            if clicked == '...':
                print_all()
            else:
                doc = get_doc(windows[clicked])
                print_doc(clicked, doc, True)
                outp.set_vscroll_position(0)
    window.close()

def get_doc(func):
    outp = ''
    if getattr(func, '__doc__'):
        for l in func.__doc__.split('\n'):
            l = l.lstrip(' ').rstrip('\n')
            if l.endswith(' '):
                l += '\n'
            elif l:
                l += ' '
            else:
                l = '\n'
            outp += l
            
    return outp[1:]

def get_menu_tooltips():
    d = []
    for w in windows.values():
        i = inspect.getdoc(w)
        if opts['Tooltips'] and i:
            d.append(i.split('\n')[0])
        else: d.append(None)
    return d


def add_assets_window():
    '''
    Add asset links to metadata file 

    This tool adds asset links to the metadata. Select a source folder where
    roms or links are located. Then select the folders for each asset type,
    such as screenshot, fanart, and video. Images matching the rom's filename
    will be searched for and added to the metadata file. 

    Add Missing Files | Links for images that cannot be found will still be
    added. The extension chosen from the drop down box will be assumed. 
    Keep Old Assets | Existing asset links will be removed by default. Check
    this box to keep them. Duplicates may be created in this case. 
    Save | Save changes to metadata.pegasus.txt. A backup will be created first.
    '''
    def update_path():
        window['Save'].update(disabled=False)
        image_dirs = get_image_paths()
        l = [''] + list(image_dirs.values())
        for a in assets:
            v = image_dirs.get(assets[a][0], '')
            window[a].update(values=l, value=v)
   
    def get_image_paths():
        image_base = os.path.join(source, 'media')
        if not os.path.isdir(image_base): image_base = source
            
        return {f: os.path.join(image_base, f) for f in ['']+os.listdir(image_base)
                        if os.path.isdir(os.path.join(image_base,f))}

    assets = 'banner, boxfront, logo, screenshot, titlescreen, video'.split(', ')
    assets = dict(
            banner=('banner','jpg'), boxfront=('box2dfront', 'jpg'),
            logo=('wheel', 'png'), screenshot=('screenshot', 'jpg'),
            titlescreen=('title', 'jpg'), video=('videos', 'mp4') )
    exts = opts['Image Types'].split(',')

    source = opts['History'][0]

    layout = [[sg.Text('Source', size=12),
                sg.Combo(opts['History'], default_value=source, size=(50,1),
                enable_events=True, bind_return_key=True, key='Source'),
                sg.FolderBrowse(initial_folder=source)],
            [sg.Checkbox('Add Missing Files', default=True, key='missing'),
                sg.Checkbox('Keep Old Assets', key='keep')],
            [[sg.Text(asset, size=12),
                sg.Combo([], size=50, key=asset, readonly=True),
                sg.Combo(exts, default_value=assets[asset][1], size=5, key=asset+'-ext')]
                for asset in assets.keys()], 
            [sg.Text('')],
            [sg.Push(), sg.Button('Save', disabled=True)] ]
    
    window = sg.Window('Add Asset Metadata', layout, finalize=True)
    results = False
    if os.path.isdir(source):
        update_path()

    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        
        elif event == 'Source':
            if os.path.isdir(values['Source']):
                source = values['Source']
                update_history(source, window['Source'])
                update_path()

        elif event == 'Scan':
            results = scan_for_mix(source, window)
            if results:
                info, image_dirs, exists = results
                window['BUILD'].update(disabled=False)
                window['LIST'].update(disabled=False, values=info)
        
        elif event == 'Save':
            params = {a: (window[a].get(), window[a+'-ext'].get()) for a in assets}
            add_assets(source, params, values['missing'], values['keep'])
            break
        
        elif event == 'LIST':
            if values['LIST'][0].startswith(' '):
                pyperclip.copy(values['LIST'][0].strip())
    window.close()

def add_assets(source, values, missing=True, keep=False):
    path = source
    if not os.path.isfile(source):
        source = os.path.join(source, meta_filename)
    if not os.path.isfile(source):
        print('cannot find', source)
        return

    backup_metadatas([os.path.split(source)[0]])
    with open(source, encoding='utf8') as inp:
        lines = inp.readlines()

    game = file = None
    with open(source, 'w', encoding='utf8') as outp:
        for line in lines:
            l = line.strip()
            if l.startswith('game:'):
                game = l.split('game:')[1].strip()
            elif l.startswith('file:'):
                file = os.path.splitext(l.split('file:')[1].strip())[0]
            elif game and l == '':
                for v in values:
                    p, e = values[v]
                    if not p:
                        continue
                    for ext in opts['Image Types'].split(','):
                        f = os.path.join(p, file) + '.' + ext
                        if os.path.isfile(f):
                            f = './'+os.path.relpath(f, path)
                            print('assets.{}: {}'.format(v, f), file=outp)
                            break
                    else:
                        if missing:
                            f = os.path.join(p, file) + '.' + e
                            f = './'+os.path.relpath(f, path)
                            print('assets.{}: {}'.format(v, f), file=outp)
                game = file = None

            if keep or not l.startswith('assets.'):
                print(line.rstrip('\n'), file=outp, end=None)


def backup_metadata_window():
    '''
    Backup all pegasus metadata files found into a zip file. 

    Select a source folder and press ok button. All metadata.pegasus.txt
    files found in the folder and its subfolders are added to a
    metadata.pegasus.?.zip file in the source folder, where ? is a date
    stamp.
    '''
    source = popup_get_folder(
        "Select or enter path to search for metadata.", "Backup Metadata")
    if source:
        metadatas = get_metadatas(source)
        backup_metadatas(metadatas)

def popup_get_folder(message, title=None):
    source = opts['History'][0]
    browse_button = sg.FolderBrowse(initial_folder=source)

    layout = [[]]
    layout += [[sg.Text(message, auto_size_text=True)]]
    layout += [[sg.Combo(opts['History'], default_value=source, key='-INPUT-', size=(45, 1), bind_return_key=True),
                    browse_button]]
    layout += [[sg.Push(), sg.Button('Cancel', size=(6, 1)), sg.Button('Ok', size=(6, 1), bind_return_key=True)]]
    window = sg.Window(title=title or message, layout=layout)

    while True:
        event, values = window.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break
        elif event in ('Ok', '-INPUT-'):
            if values['-INPUT-'] != '':
                update_history(values['-INPUT-'], window['-INPUT-'])
            break

    window.close()
    del window
    if event in ('Cancel', sg.WIN_CLOSED):
        return None

    return values['-INPUT-']


def check_file_window():
    '''
    Find missing and extra files in a rom path. 

    This tool scans a rom folder for games and for matching assets. It reports missing
    images in each media subfolder, images that don't match a game, and games that lack
    entries in the metadata file. 

    Select a source folder and press Scan. A list of categories will appear in the text
    box. Click one to display a list of items in that category. The category name is
    shown as the first item of the list. Click it to return to the initial category list. 

    By using the Cut or Copy options you may copy the name of a file into the
    clipboard. This allows you to easily search for images on the web or renme files to
    complete or correct your game media assets. You may also copy the entire report or
    view it in a text editor. 

    On Click Options | 
    Ignore | Clicking a list item does nothing 
    Hide | Clicking a list item removes it from the list 
    Launch | Clicking on an extra image will open it in your default viewer. Clicking
    on a missing image will open the metadata file. 
    Copy | Clicking a list item copies it into the clipboard 
    Cut | Clicking a list item copies it to the clipboard and removes it from the list 
    Delete | Clicking on an extra image will delete the file. Clicking on a missing
    image will delete the game's metadata from the metadata.pegasus.txt file 

    Other Buttons | 
    Copy Mode | Duplicate assets and broken asset links show both the game's name and a
    file link. This option determines what gets copied to the clipboard when such items
    are clicked, the game, the link, or both. 
    Metadata | Open the metadata.pegaus.txt file 
    Copy | Copy the entire report into your clipboard 
    Open | Open the entire report in a text editor defined in this program's options
    '''
    def copy_text(text):
        if '->' in text:
            if values['copymode'] == 'Game':
                text = sel.split(' -> ')[0]
            elif values['copymode'] == 'Link':
                text = sel.split(' -> ')[1]
        pyperclip.copy(text)

    source = opts['History'][0]
    boxes = ['Ignore', 'Hide', 'Launch', 'Copy', 'Cut', 'Delete']
    Buttons = ['Clip Report']

    layout = [[sg.Text('Source', size=10),
                sg.Combo(opts['History'], default_value=source,
                        size=(50,1), enable_events=True ,key='Source'),
                sg.FolderBrowse(initial_folder=source), sg.Push(), sg.Button('Scan')],
            [sg.Text('On Click:')] + [
                    sg.Radio(box, 'CLICK', key=box, enable_events=True, default=box=='Ignore')
                    for box in boxes] + 
                    [sg.Push(), sg.Text('Copy Mode: '), 
                        sg.Combo(['Game', 'Link', 'Both'], key='copymode', default_value='Both', readonly=True)],
            [sg.Listbox(['Select source folder and scan'],enable_events=True, size=(100, 15),
                    expand_x=True, expand_y=True, key="LIST", disabled=True)],
            [sg.Button('Metadata', disabled=True), sg.Push(), sg.Text('Full Report'),
                    sg.Button('Copy', key='COPY', disabled=True), sg.Button('Open', disabled=True)] ]
    
    window = sg.Window('Check Files', layout, finalize=True)
    #scroller = get_scroller(econsole)
    text_rows = []
    results = False

    while True:
        event, values = window.read()
        values = values or {}
        checked = {k: values.get(k, False) for k in boxes}
        #source = values.get('Source')

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        elif event == 'Scan':
            category = None
            source = values['Source']
            if os.path.isdir(source):
                update_history(source, window['Source'])
                window['LIST'].update(disabled=False, values=['scanning...'])
                window.refresh()
                info = scan_files(source)
                window['LIST'].update(values=info.keys())
                for w in ('COPY', 'Open', 'Metadata'):
                    window[w].update(disabled=False)
            else:
                window['LIST'].update(['error: not a folder'])
        
        elif event == 'Metadata':
            open_text_file(os.path.join(source, meta_filename))

        elif event == 'COPY':
            pyperclip.copy(get_file_report(info))
        elif event == 'Open':
            fp, name = tempfile.mkstemp(suffix='.txt')
            with open(name, 'w', encoding='utf8') as outp:
                print(get_file_report(info), file=outp)
            open_text_file(name)

        elif event == 'LIST':
            if values['LIST']:
                sel = values['LIST'][0]

                if sel == category: # top item/back
                    category = None
                    window['LIST'].update(values=info.keys())
                elif info.get(sel):
                    category = sel
                    window['LIST'].update(values=[sel]+info[sel])
                elif category in info and sel in info[category]:
                    if values['Copy']:
                        copy_text(sel)
                        window.minimize()
                    elif values['Cut']:
                        copy_text(sel)
                        items = window['LIST'].get_list_values()
                        items.remove(sel)
                        window['LIST'].update(values=items)
                        window.minimize()
                    elif values['Hide']:
                        items = window['LIST'].get_list_values()
                        items.remove(sel)
                        window['LIST'].update(values=items)
                    elif values['Launch']:
                        launch_clicked(sel, category, source)
                    elif values['Delete']:
                        print('deleting:', sel)
                        if delete_clicked(sel, category, source):
                            items = window['LIST'].get_list_values()
                            items.remove(sel)
                            window['LIST'].update(values=items)
    window.close()

def delete_clicked(item, category, base, confirm=True):
    if 'metadata' in category:
        if category.startswith('missing in'):
            path = os.path.join(base, item)
            for ext in get_metadata_exts(base):
                fn = path+'.'+ext
                if os.path.exists(fn):
                    print('deleting', fn)
                    if sg.popup_ok_cancel('Delete file',fn, title='Confirm') == 'OK':
                        os.remove(fn)
                        return True

        elif category.startswith('extra in'):
            skip = False
            md = os.path.join(base, meta_filename)
            if sg.popup_ok_cancel('Delete {} from:\n{}'.format(
                    item, md), title='Confirm') != 'OK':
                return

            with open(md, encoding='utf8') as inp:
                lines = inp.readlines()
            os.rename(md, md+'.b')

            with open(md, 'w', encoding='utf8') as outp:
                for l in lines:
                    if l.startswith('game:'):
                        skip = False
                        if l.split(':', 1)[1].strip() == item:
                            skip = True
                    if not skip:
                        print(l.strip('\n'), file=outp)
            return True
        else:
            sg.popup_ok('Cannot manage duplicates. Use Metadata button to resolve this issue.', title='Error')

    elif category.startswith('extra in '):
        typ = category[9:].rsplit(':', 1)[0]
        path = os.path.join(base, typ, item)
        if not os.path.isdir(path):
            path = os.path.join(base, 'media', typ, item)
        for ext in opts['Image Types'].split(','):
            fn = path+'.'+ext
            if os.path.exists(fn):
                print('deleting', fn)
                if sg.popup_ok_cancel('Delete file',fn, title='Confirm') == 'OK':
                    os.remove(fn)
                    return True

    elif category.startswith('missing in '):        
        path = os.path.join(base, item)
        for ext in get_metadata_exts(base):
            fn = path+'.'+ext
            if os.path.exists(fn):
                print('deleting', fn)
                if sg.popup_ok_cancel('Delete file',fn, title='Confirm') == 'OK':
                    os.remove(fn)
                    return True
    
    elif category.startswith('broken in '):
        key = category.split('broken in ')[1].split(':', 1)[0]
        md = os.path.join(base, meta_filename)
        found = False

        with open(md, encoding='utf8') as inp:
            lines = inp.readlines()
        os.rename(md, md+'.b')
        match = item.split(' -> ')[1]

        with open(md, 'w', encoding='utf8') as outp:
            for l in lines:
                skip = False
                if l.startswith(key):
                    v = l.split(':', 1)[1].strip()
                    if match in v:
                        skip = found = True
                if not skip:
                    print(l.strip('\n'), file=outp)
        return found

def get_file_report(info):
    s = ''
    for k, v in info.items():
        s += '{}\n'.format(k)
        if v:
            for i in v:
                s += '\t{}\n'.format(i)
    return s

def get_metadata_exts(base):
    path = os.path.join(base, meta_filename)
    exts = []
    try:
        with open(path, encoding='utf8') as inp:
            for l in inp:
                if l.strip().startswith('extension:') or l.strip().startswith('extensions:'):
                    exts += [i.strip() for i in l.split(':', 1)[1].split(',')]
    except:
        pass
    if exts:
        exts = list(set(exts))
    else:
        print('cannot find extensions in metadata!')
        exts = opts['Rom Types']
    #print('Rom Extensions:', exts)
    return exts

def launch_clicked(item, category, base):
    if 'metadata' in category:
        if category.startswith('missing in'):
            open_text_file(os.path.join(base, meta_filename))
            launch_file(base)

        else:
            open_text_file(os.path.join(base, meta_filename))

    elif category.startswith('extra in '):
        typ = category[9:].rsplit(':', 1)[0]
        path = os.path.join(base, typ, item)
        if not os.path.isdir(path):
            path = os.path.join(base, 'media', typ, item)
        for ext in opts['Image Types'].split(','):
            fn = path+'.'+ext
            if os.path.exists(fn):
                launch_file(fn)

    elif category.startswith('missing in '):
        open_text_file(os.path.join(base, meta_filename))

def open_text_file(fn):
    if opts['Editor']:
        subprocess.Popen((opts['Editor'], fn), close_fds=True)
    else:
        launch_file(fn)

def launch_file(filename):
    platform = sys.platform
    if platform == 'darwin':
        subprocess.call(('open', filename))
    elif platform in ['win64', 'win32']:
        os.startfile(filename.replace('/','\\'))
    else:
        try: # check for wsl
            proc_version = open('/proc/version').read()
            if 'Microsoft' in proc_version:
                subprocess.call('cmd.exe /C start'.split() + [filename])
        except:
            pass # other linux variants
        subprocess.call(('xdg-open', filename))

def scan_files(base, image_dirs=None):

    if not image_dirs:
        image_base = os.path.join(base, 'media')
        if not os.path.isdir(image_base): image_base = base
            
        image_dirs = [os.path.join(image_base, f) for f in os.listdir(image_base)
                        if os.path.isdir(os.path.join(image_base,f))]
        #print('Image Dirs:', image_dirs)

    exts = get_metadata_exts(base) or opts['Rom Types']
    files = sorted([os.path.splitext(f)[0] for f in os.listdir(base)
                if os.path.splitext(f)[-1][1:].lower() in exts], key=lambda x: x.lower())
    #print(f'\nFiles found: {len(files)}')

    info = {}
    info['{} files found in {}'.format(
            len(files), os.path.split(base)[-1])] = None
    for typ in image_dirs:
        if not os.path.isdir(typ):
            print(typ, 'missing')
            continue

        t = os.path.split(typ)[-1]
        names = sorted([os.path.splitext(f)[0] for f in os.listdir(typ)
                    if os.path.splitext(f)[-1][1:].lower() in opts['Image Types']])
        items = []
        for name in files:
            if name not in names and not re.match(disc_pattern, name):
                items.append(name)
        info['missing in {}: {}'.format(t, len(items))] = items

        items = []
        for name in names:
            if name not in files:
                items.append(name)
        info['extra in {}: {}'.format(t, len(items))] = items

    add_metadata(base, files, info)
    return info


def scan_metadata(path, return_ignored=False, strip_ext=True):
    path = os.path.join(path, meta_filename)
    if not os.path.isfile(path):
        print('cannot find', path)
        return

    games = []
    ignored = []
    game = key = None

    with open(path, encoding="utf8") as file:
        for l in file:
            if l.startswith('game:'):
                if game:
                    games.append(game)
                game = {'game': l.split(':', 1)[1].strip()}
                
            elif l.startswith('collection:'):
                if game:
                    games.append(game)
                game = None

            elif ':' in l and not l.startswith(' '):
                key, value = l.split(':', 1)
                value = value.strip(' \n')
                key = key.strip(' \n')
                if value.startswith('./'):
                    value = value[2:]
                if key == 'file' and strip_ext:
                    value = os.path.splitext(value)[0]
                if key.startswith('ignore-file'):
                    ignored.append(value)
                if game:
                    game[key] = value

            elif key == 'description':
                s = l.lstrip() # + ' '
                #if s in (' ', '. '):
                #    s = '\n'
                game[key] += s
            elif isinstance(key, str) and key.startswith('ignore-file'):
                if value:
                    ignored.append(value)
                elif l.strip():
                    ignored.append(l.strip())
        if game:
            games.append(game)
    if return_ignored:
        return games, ignored
    return games

def add_metadata(path, files, info):
    games = scan_metadata(path)
    d = {}; dups = []
    for g in games:
        name = g.get('game')
        file = g.get('file')
        if name in d:
            if d[name]:
                dups.append('{} -> {}'.format(name, d[name]))
                d[name] = None
            dups.append('{} -> {}'.format(name, file))
        else:
            d[name] = file

    meta_files = [d['file'] for d in games]# if 'file' in d]
    file_game = {i['file']: i['game'] for i in games}
    extras = sorted([file_game[m] for m in meta_files if m not in files], key=lambda x: x.lower())
    missing = sorted([f for f in files if f not in meta_files], key=lambda x: x.lower())
    
    broken = {}
    for g in games:
        for i in g:
            if i.startswith('assets.'):
                fn = g[i]
                if not os.path.isfile(fn) and not os.path.isfile(os.path.join(path, fn)):
                    if i not in broken:
                        broken[i] = []
                    broken[i].append('{} -> {}'.format(g['game'], g[i]))

    info['missing in metadata: {}'.format(len(missing))] = missing
    info['extra in metadata: {}'.format(len(extras))] = extras
    info['duplicates in metadata: {}'.format(len(dups))] = dups
    for b in broken:
        info['broken in {}: {}'.format(b, len(broken[b]))] = broken[b]


def edit_genre_window():
    '''
    Rename genres within one or more metadata files 

    This tool helps you consolidate genres into managable lists or just rename them as
    preferred. Select a source folder and press scan. Metadata in all subfolders will
    be scanned. A list of all genres will appear with a count of the games that use it. 

    Click on a genre to get a list of all games that use it, along with all the genres
    that each of those games use. Click Back or the top top line of the game list to
    return to the genre list. When you're done press Export to save changes to all the
    metadata.pegasus.txt files. Backups will be created first. 

    On Click Options | 
    View | Clicking on a genre opens a list of games using it 
    Rename | Clicking on a genre opens a dialog allowing you to rename it 
    Select | Clicking on genres multi-select them so you can rename them all at once 

    Default Text Options | 
    Blank | The rename dialog opens blank, without any default text 
    Clicked | The rename dialog opens with the genre's name for easy editing 
    Previous | The rename dialog opens with the previous entry for easy reapplying 

    Other Buttons | 
    Back | Return from the game list to the genre list 
    Export | Export changes to all metadata files after backing them up 
    Rename | Rename the currently selected genre or genres
    '''
    def rename(sel):
        default = ''
        if values['Clicked']:
            default = sel.split(': ')[0]
        elif values['Previous']:
            default = rename.previous
        
        if isinstance(sel, str):
            suffix = ''
            sel = (sel, )
        else:
            suffix = ' + {} more'.format(len(sel)-1)

        title = sel[0].rsplit(':', 1)[0] + suffix
        text = sg.popup_get_text('Rename Genre', title, default_text=default)
        if text:
            window['Export'].update(disabled=False)
            rename.previous = text
        
            for s in sel:
                s = s.rsplit(':', 1)[0]
                changes[s] = text
                games = genres.get(s)
                for ng in text.split(','):
                    nl = genres.get(ng.strip(), []) + games
                    genres[ng.strip()] = nl
                genres.pop(s)
            update_genres()

    def update_genres():
        head = ['{} genres in {}'.format(len(genres), source) + '']
        window['LIST'].update(disabled=False, values=head+sorted(
            ['{}: {}'.format(g, len(genres[g])) for g in genres]))

    rename.previous = ''
    category = None
    changes = {}
    click_boxes = ['View', 'Rename', 'Select']
    results = False
    source = opts['History'][0]
    text_boxes = ['Blank', 'Clicked', 'Previous']

    layout = [[sg.Text('Source', size=10),
                sg.Combo(opts['History'], default_value=source,
                        size=(50,1), enable_events=True ,key='Source'),
                sg.FolderBrowse(initial_folder=source), sg.Push(), sg.Button('Scan')],
            [sg.Text('On Click:')] + [
                    sg.Radio(box, 'CLICK', key=box, enable_events=True, default=box=='View')
                    for box in click_boxes] + [sg.Push(), sg.Text('Default Text:')] + [
                    sg.Radio(box, 'TEXT', key=box, enable_events=True, default=box=='Blank')
                    for box in text_boxes],
             
            [sg.Listbox(['Select source folder and scan'],enable_events=True, size=(100, 15),
                    expand_x=True, expand_y=True, key="LIST", disabled=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Push(), sg.Button('Back', disabled=True), sg.Button('Export', disabled=True),
                    sg.Button('Rename', disabled=True, key='RENAME')] ]
    
    window = sg.Window('Edit Genres', layout, finalize=True)
    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        elif event == 'Scan':
            category = None
            source = values['Source']
            if os.path.isdir(source):
                update_history(source, window['Source'])
                window.refresh()

                genres = scan_genres(source)
                update_genres()
                
            else:
                window['LIST'].update(['error: not a folder'])
        
        elif event == 'LIST':
            if values['View'] or category:
                if values['LIST']:
                    sel = values['LIST'][0]
                    split = sel.split(':')[0]

                    if sel == category:
                        category = None
                        window['LIST'].update(disabled=False, values=sorted(
                            ['{}: {}'.format(g, len(genres[g])) for g in genres]))

                    elif split in genres:
                        n = [sel, ''] + sorted(genres[split])
                        window['LIST'].update(values=n)
                        category = sel
                    
                    else:
                        window['LIST'].update(set_to_index=[])

            elif values['Rename']: #single click on list with Rename selected
                sel = values['LIST'][-1]
                window['LIST'].update(set_to_index=[])
                rename(sel)
                window['LIST'].update(set_to_index=[])
                
        elif event == 'Back':
            category = None
            window['LIST'].update(disabled=False, values=sorted(
                ['{}: {}'.format(g, len(genres[g])) for g in genres]))
        
        elif event == 'RENAME': # clicked Rename button
            sel = category or values['LIST']
            rename(sel)
        
        elif event == 'Export':
            if export_genre_window(changes):
                metadatas = get_metadatas(source)
                backup_metadatas(metadatas)
                for md in metadatas:
                    update_metadata_genres(md, changes)
        
        elif event in click_boxes:
            window['LIST'].update(set_to_index=[])
            if category:
                category = None
                window['LIST'].update(disabled=False, values=sorted(
                    ['{}: {}'.format(g, len(genres[g])) for g in genres]))


        window['Back'].update(disabled=not bool(category))
        disabled = False if category or (values['Select'] and len(values['LIST'])) else True
        window['RENAME'].update(disabled=disabled)

    window.close()

def backup_metadatas(metadatas):
    import zipfile, datetime
    if metadatas:
        basepath = os.path.commonpath(metadatas)
        timestamp = datetime.datetime.now().strftime("%y-%m-%d@%H:%M")

        outp = os.path.join(basepath, 'meta.backup.{}.zip'.format(timestamp))
        print('backing up metadata to', outp)
        with zipfile.ZipFile(os.path.join(basepath, outp),
                'w', zipfile.ZIP_DEFLATED) as outp:

            for md in metadatas:
                if not md.endswith('.txt'):
                    md = os.path.join(md, meta_filename)
                outp.write(md, os.path.relpath(md, basepath))

def export_genre_window(changes):
    backup = changes.copy()
    items = ['{} >> {}'.format(k, v) for k, v in changes.items()]
    layout = [
        [sg.Listbox(items, size=(100, 15), enable_events=True,
                expand_x=True, expand_y=True, key="LIST")],
        [sg.Push(), sg.Button('Cancel'), sg.Button('Save')] ]

    window = sg.Window('Confirm Changes', layout, finalize=True)
    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            changes.update(backup)
            break
        elif event == 'LIST':
            sel = values['LIST'][0]
            changes.pop(sel.split(' >>')[0])
            items.remove(sel)
            window['LIST'].update(values=items)
            print(changes)
        elif event == 'Save':
            window.close()
            return True

    window.close()

def get_metadatas(path):
    print('get_metadata:', path)
    if os.path.isdir(path):
        metadatas = []
        if os.path.isfile(os.path.join(path, meta_filename)):
            metadatas.append(path)
        for root, folders, files in os.walk(path):
            for f in folders:
                p =os.path.join(root, f)
                if os.path.isfile(os.path.join(p, meta_filename)):
                    metadatas.append(p)
        print(metadatas)
        return metadatas

def scan_genres(path):
    from timeit import timeit

    max_length = 60
    sg.one_line_progress_meter('Scanning Folder', 0, 1, 
            'Scanning for metadata in {}'.format(path),
            orientation='h', size = (max_length, 3), grab_anywhere=False,
            bar_color=('white', 'red'), keep_on_top=False, key=1)


    metadatas = get_metadatas(path)
    print(metadatas)
    metadata = []
    count = len(metadatas)
    for i, m in enumerate(metadatas):
        sg.one_line_progress_meter('Scanning Metadata', i+1, count, 
                'Scanning for metadata in {}'.format(m),
                orientation='h', size = (max_length, 3), grab_anywhere=False,
                bar_color=('white', 'red'), keep_on_top=False, key=1)
        meta = scan_metadata(m)
        for d in meta:
            d['root'] = m
            metadata.append(d)

    genres = {}
    for m in sorted(metadata, key = lambda x: x['game']):
        gs = m.get('genre', '')
        gs = gs.replace(' / ', ', ')
        for i in gs.split(','):
            g = i.strip()
            if g:
                if g not in genres:
                    genres[g] = []
                genres[g].append('{} | {}'.format(m['game'], gs))
   
    return genres

def update_metadata_genres(metadata, changes):
    skip = False
    if not metadata.endswith('.txt'):
        metadata = os.path.join(metadata, meta_filename)

    with open(metadata, encoding='utf8') as inp:
        lines = inp.readlines()

    with open(metadata, 'w', encoding='utf8') as outp:
        for l in lines:
            if l.startswith('genre:'):
                text = l.split(': ', 1)[1].strip()
                for og in text.split(','):
                    og = og.strip()
                    if og in changes:
                        l = l.replace(og, changes[og])
            print(l.strip('\n'), file=outp)


def hide_disks():
    '''
    Hides multi-disc ISOs and creates M3U playlists
    
    Select a folder. All pegasus metadata files in the folder and its subfolders are
    scanned and the files with '(disc X)' tags in their filename will be added
    to the ignored files list. If there is no M3U playlist for the game it will be
    created. 

    Example files | 
    Resident Evil (disk 1).chd 
    Resident Evil (disk 2).chd 
    Resident Evil.m3u 

    The two chd files will be set to ignore in the metadata.pegasus.txt file. The m3u
    file will be created if necessary. 
    '''
    source = popup_get_folder(
        "Select or enter path to search for metadata.", "Backup Metadata")
    if source:
        metadatas = get_metadatas(source)
        md = os.path.join(source, meta_filename)
        if os.path.isfile(md):
            metadatas.append(source)

        exts = get_metadata_exts(source)
        backup_metadatas(metadatas)
        ignore = []
        for md in metadatas:
            files = []
            for fn in os.listdir(md):
                name, ext = os.path.splitext(fn)

                # check if file matches disk pattern
                if ext[1:] in exts and re.match(disc_pattern, name):
                    ignore.append(fn)
                    pat = disc_pattern[2:]
                    match = re.split(pat, name)[0].strip() + '.m3u'

                    # build m3u playlist if necessary
                    if not os.path.isfile(os.path.join(md, match)):
                        discs = [fn for fn in os.listdir(md) if fn.startswith(match[:-4])
                                and os.path.splitext(fn)[1][1:] in exts]
                        with open(os.path.join(md, match), 'w', encoding='utf8') as outp:
                            for d in sorted(discs, key=lambda x: x.lower()):
                                print(d, file=outp)
                        print('making m3u playlist for', match)

            # read old metadata
            with open(os.path.join(md, meta_filename), encoding='utf8') as inp:
                lines = inp.readlines()

            wrote = False
            with open(os.path.join(md, meta_filename), 'w', encoding='utf8') as outp:
                for l in lines:
                    # write ignore file list for games with (disk x) in the filename
                    if (l == '\n' or l.strip().startswith('game:')) and not wrote:
                        print('\n', file=outp)
                        print('ignore-files:', file=outp)
                        for i in sorted(ignore, key=lambda x: x.lower()):
                            print('  '+i, file=outp)
                        print('', file=outp)
                        wrote = True
                    else:
                        # write the other lines
                        print(l, end='', file=outp)


def make_mix_window():
    '''
    Create image mix collages from screenshot, box, and logo images 

    This tool generates image mixes similar to various scraper sites provide by plotting
    a logo and box art over a screenshot or similar image. It only supports 3 image
    mixes. 

    Select a source folder with image subfolders. A list of image folders will populate
    the dropdown boxes for background, box, and logo. Select the folder you want to use
    for each of them. Then press scan. A report of missing images will appear in the
    text box. Press Build to create the image mixes in the mix folder. 
    '''
    def update_path():
        image_base = os.path.join(source, 'media')
        defaults = dict(Background='screenshot', Box='box2d', Logo='wheel')
        if not os.path.isdir(image_base): image_base = source
            
        image_dirs = sorted([os.path.join(image_base, f) for f in os.listdir(image_base)
                        if os.path.isdir(os.path.join(image_base, f)) and f != opts['Mix Folder']])
        

        for f in ('Background', 'Box', 'Logo'):
            window[f].update(values=image_dirs)

            for i in image_dirs:
                if i.endswith(defaults[f]):
                    window[f].update(value=i)
                    break
            else:
                window[f].update(set_to_index=0)

    source = opts['History'][0]
    #boxes = ['Ignore', 'Hide', 'Launch', 'Copy', 'Cut', 'Delete']

    layout = [[sg.Text('Source', size=12),
                sg.Combo(opts['History'], default_value=source, size=(50,1),
                enable_events=True, bind_return_key=True, key='Source'),
                sg.FolderBrowse(initial_folder=source), sg.Push(), sg.Button('Scan')],
            [sg.Text('')],
            [sg.Push(), sg.Text('Background'),
                sg.Combo([], size=50, key='Background', readonly=True)],
            [sg.Push(), sg.Text('Box'),
                sg.Combo([], size=50, key='Box', readonly=True)],
            [sg.Push(), sg.Text('Logo'),
                sg.Combo([], size=50, key='Logo', readonly=True)],
            [sg.Listbox(['Select source folder and scan'],enable_events=True, size=(100, 15),
                    expand_x=True, expand_y=True, key="LIST", disabled=True)],
            [sg.Push(), sg.Button('Build Mix Images', key='BUILD', disabled=True)] ]
    
    window = sg.Window('Make Image Mixes', layout, finalize=True)
    results = False
    if os.path.isdir(source):
        update_path()

    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        
        elif event == 'Source':
            if os.path.isdir(values['Source']):
                source = values['Source']
                update_history(source, window['Source'])
                update_path()

        elif event == 'Scan':
            results = scan_for_mix(source, window)
            if results:
                info, image_dirs, exists = results
                window['BUILD'].update(disabled=False)
                window['LIST'].update(disabled=False, values=info)
        
        elif event == 'BUILD':
            overwrite = True
            if exists:
                overwrite = sg.popup_yes_no(
                    '{} images already exists in output folder.'.format(len(exists)), 
                    'Overwrite them?', title='Confirm') == 'Yes'

            make_mix_images(source, image_dirs, overwrite)
        
        elif event == 'LIST':
            if values['LIST'][0].startswith(' '):
                pyperclip.copy(values['LIST'][0].strip())


    window.close()

def load_image(name, folder, png=False):
    import pygame as pg
    Rect = pg.Rect

    if png:
        path = os.path.join(folder, name+'.png')
        alt_path = os.path.join(folder, name+'.jpg')
    else:
        path = os.path.join(folder, name+'.png')
        alt_path = os.path.join(folder, name+'.jpg')
        
    if os.path.isfile(path):
        image = pg.image.load(path)
    elif os.path.isfile(alt_path):
        image = pg.image.load(alt_path)
    else:
        print('{} not found in {}'.format(name, folder))
        return
    if image.get_bytesize() < 3:
        surface = pg.Surface(image.get_size(), depth=32)
        surface.blit(image, (0,0))
        image = surface
    return image


def make_mix_images(base, image_dirs, overwrite):
    try:
        import pygame as pg
        Rect = pg.Rect
    except:
        sg.popup_ok('Could not import pygame library.',
                'This feature is unavailable', title='Error')
        return

    try:
        mix_size = opts['Mix Size'][:2]
    except: mix_size = 800, 600
    try:
        box_size = opts['Mix Box Size'][:2]
    except: box_size = 200, 400
    try:
        logo_width = int(opts['Mix Logo Width'])
    except: logo_width = 400 
    padding = opts['Mix Padding']

    image_rect = Rect(0,0, *mix_size)
    box_rect = Rect(0,0, *box_size)
    box_rect.bottomleft = image_rect.bottomleft
    logo_rect = Rect(0,0, logo_width, 1000)

    out_folder = os.path.join(base, opts['Mix Folder'])
    if os.path.isdir(os.path.join(base, 'media')):
        out_folder = os.path.join(base, 'media', opts['Mix Folder'])
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)

    exts = get_metadata_exts(base)
    names = sorted([os.path.splitext(f)[0] for f in os.listdir(base)
                    if os.path.splitext(f)[-1][1:].lower() in exts])

    total = len(names)
    for i, game in enumerate(names):
        out_filename = os.path.join(out_folder, game+'.png')
        if os.path.exists(out_filename) and not overwrite:
            print(out_filename, 'exists: skipping')
            continue

        max_length = 60
        if not sg.one_line_progress_meter('Building Images', i+1, total, 
                'Building file for {}'.format(game),
                orientation='h', no_titlebar=False, size = (max_length, 3), grab_anywhere=False,
                bar_color=('white', 'red'), keep_on_top=False, key=1):
            print('Canceled build')
            return

        out_surface = pg.surface.Surface(image_rect.size, pg.SRCALPHA)

        image = load_image(game, image_dirs['Background'])
        if not image: continue
        r = Rect(0,0, *image.get_size()).fit(image_rect)
        r.topleft = 0,0
        scaled = pg.transform.smoothscale(image, r.size)
        out_surface.blit(scaled, (0,0))
        #   pg.draw.rect(out_surface, (255,255,255), r, 2)

        image = load_image(game, image_dirs['Box'])
        if not image: continue
        r = Rect(0,0, *image.get_size()).fit(box_rect)
        r.bottomleft = (image_rect.left+padding,
                image_rect.bottom-padding)
        scaled = pg.transform.smoothscale(image, r.size)
        out_surface.blit(scaled, r.topleft)
        #pg.draw.rect(out_surface, (255,255,255), r, 2)

        image = load_image(game, image_dirs['Logo'])
        if not image: continue
        r = Rect(0,0, *image.get_size()).fit(logo_rect)
        r.bottomright = image_rect.right-5, image_rect.bottom-padding
        scaled = pg.transform.smoothscale(image, r.size)
        out_surface.blit(scaled, r.topleft)
        #pg.draw.rect(out_surface, (255,255,255), r, 2)

        pg.image.save(out_surface, out_filename)
    sg.one_line_progress_meter_cancel(key=1)

def scan_for_mix(path, window):
    mix = opts['Mix Folder']
    image_dirs = {p: window[p].get() for p in ('Background', 'Box', 'Logo')}
    if len(set(image_dirs.values())) < 3:
        sg.popup_ok('Must provide unique path for each image type.', title='Error')
        return

    info = scan_files(path, image_dirs.values())
    types = [os.path.split(v)[-1] for v in image_dirs.values()]
    results = []
    for k, v in info.items():
        if k[len('missing in '):].split(':', 1)[0] in types:
            results.append(k)
            for i in v:
                results.append(' '+i)
            results.append('')
    
    exts = get_metadata_exts(path)
    dest = os.path.join(path, mix)
    if os.path.isdir(os.path.join(path, 'media')):
        dest = os.path.join(path, 'media', mix)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    wheels = [f for f in os.listdir(dest)]
    games = [os.path.splitext(f)[0] for f in os.listdir(path) if os.path.splitext(f)[-1][1:].lower() in exts]

    exists = []
    for g in games:
        if g+'.png' in wheels:
            exists.append(' {}.png'.format(g))
    results.append('missing in mix: {}'.format(len(games)-len(exists)))
    results.append('already in mix: {}'.format(len(exists)))
    results += exists
    return results, image_dirs, exists


def option_window():
    '''
    Edit global options and access Theme selector 

    A list of all programs is given. Change them as desired. Changes are saved when okay
    is pressed. These changes only apply to tool windows opened after changes are saved,
    not to alredy open windows. 

    Minimal error checking is performed. If the program stops working properly after
    changing an option you can delete options.dat to restore defaults. 

    Theme Menu | 
    There is a Theme button allowing you to change the appearance and size of the
    program. Like other options, changes made to the theme only apply to newly opened
    windows. 
    '''
    column = []

    column = [
        [sg.Text(k+':', size=OPT_LABEL),sg.Input(str(v), key=k, expand_x=True)] for k, v in sorted(opts.items()) ] 
     
    layout = [
        [sg.Column(column, size=(800,280), scrollable=True,  vertical_scroll_only=True)],
        [sg.Button('Theme', key='THEME'), sg.Push(), sg.Button('Cancel'), sg.Button('Okay')] ]

    window = sg.Window('Option Menu', layout,  finalize=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Okay':
            #print('window values', values)
            for k, v in opts.items():
                n = values.get(k)
                if type(v) == int:
                    try:
                        opts[k] = int(n)
                    except:
                        print('option {} failed int conversion'.format(k))
                elif type(v) == float:
                    try:
                        opts[k] = float(n)
                    except:
                        print('option {} failed float conversion'.format(k))
                elif type(v) in (list, tuple):
                    try:
                        v = eval(n)
                        if type(v) in (list, tuple):
                            opts[k] = v
                    except:
                        print('option {} failed tuple conversion'.format(k))
                else:
                    opts[k] = n            

            opts.save()
            break

        elif event == 'THEME':
            print('theme')
            launch_tool('theme')
        else:
            print(event)

    window.close()

def update_history(path, widget=None):
    'Updates history list by adding path to options[history] and updating widget'
    history = opts['History']
    if path in history:
        if history[0] != path:
            history.remove(path)
            history.insert(0, path)
            opts.save(True)
    else:
        history.insert(0, path)
        opts.save(True)
    if widget:
        widget.update(value=path, values=history)

class Options():
    'Stores program options in dict and handles saving/loading to json file'
    changed = False

    def __init__(self, filename='options.dat', reset=False):
        self.defaults()
        self.filename = filename
        if filename and os.path.exists(filename) and not reset:
            self.load(filename)
            #print 'Options Loaded:\n', self.options

        if self.options.get('Theme'):
            sg.theme(self.options['Theme'])
        font = self.options.get('Font', ('arial', 16))
        sg.set_options(font=font, tooltip_font=font, icon=icon)

    def __call__(self, option):
        return self.options.get(option, None)
    def __getitem__(self, option):
        return self.options.get(option, None)
    def __setitem__(self, index, value):
        if self.options[index] is not value:
            self.options[index] = value
            self.changed = True
            self.save(True)
            #print('{} option changed to {}'.format(index, value))
        else:
            pass
            #print('set not change')
    def items(self): return self.options.items()
    def keys(self): return self.options.keys()

    def defaults(self):
        self.options = {
            'Editor': '',
            'History': [''],
            'Image Types':  'jpg,png,mp4',
            'Mix Box Size': [200,400],
            'Mix Logo Width': 400,
            'Mix Folder': 'mix',
            'Mix Padding': 5,
            'Mix Size': [800, 600],
            'Option Label Width': 20,
            'Option Edit Width': 60,
            'Theme': 'DarkGrey11',
            'Tooltips': True,
            'Font': ['arial', 16],
            'Rom Types': 'zip,chd,iso,rom',}

    def load(self, filename = None):
        if filename: self.filename = filename

        try:
            with open(filename, encoding='utf8') as inp:
                self.options.update(json.load(inp))
            #print('loaded options from options.dat')
        except:
            print('failed to load options.dat: using defaults')
            self.defaults()
        #print('options:', self.options)

    def reset(self):
        self.defaults()
        self.save(True)

    def save(self, force=False):
        #print(self.options)
        if self.filename and (self.changed or force):
            with open(self.filename, 'w', encoding='utf8') as outp:
                json.dump(self.options, outp, sort_keys=True, indent=4)
            self.changed = False
            print('options saved')
        else:
            print('save skipped: nothing changed')
            return


def remove_assets():
    '''
    Remove asset links from metadata 

    Select a source path press okay. All metadata.pegasus.txt files will be scanned and
    all asset links will be removed from them. This is useful if you prefer to have
    Pegasus load images using their default path and filename and can shrink metadata
    files a bit. 
    '''
    source = popup_get_folder(
        "Select or enter path to search for metadata.", "Remove Assets")
    if source:
        metadatas = get_metadatas(source)
        md = os.path.join(source, meta_filename)
        if os.path.isfile(md):
            metadatas.append(source)
        backup_metadatas(metadatas)

        for md in metadatas:
            path = os.path.join(md, meta_filename)
            if not os.path.isfile(path):
                print('cannot find', path)
                continue

            with open(path, encoding='utf8') as inp:
                lines = inp.readlines()

            with open(path, 'w', encoding='utf8') as outp:
                for l in lines:
                    if l.strip().startswith('assets.'):
                        pass
                        #print(f'stripped: {l}')
                    else:
                        print(l.strip('\n'), file=outp, end=None)


def export_xml_window():
    '''
    Export Pegasus metadata to a gamelist.xml file  

    This tool reads a metadata.pegasus.txt file and saves it as an EmulationStation
    gamelist.xml file. Select a source folder that includes pegasus metadata and
    any desired image assets. Then select which image asset you want for each game's
    image and thumbnail. You may select a folder of images or existing asset metadata to
    add, or leave the drop-down blank to skip it.
    
    If a folder is selected and an image is missing for a particular game, the
    selected extension will be used as a placeholder, but only if the Add Missing Files
    options is enabled. Press save to create gamelist.xml in the source folder. If
    the file already exists it will be renamed to gamelist.xml.b, possibly overwriting
    it. 
    '''
    def update_path():
        image_dirs = get_image_paths()
        l = [''] + list(image_dirs.values()) + get_metadata_assets()
        for a in assets:
            v = image_dirs.get(assets[a][0], '')
            window[a].update(values=l, value=v)
   
    def get_image_paths():
        image_base = os.path.join(source, 'media')
        if not os.path.isdir(image_base): image_base = source
            
        return {f: os.path.join(image_base, f) for f in ['']+os.listdir(image_base)
                        if os.path.isdir(os.path.join(image_base,f))}

    def get_metadata_assets():
        path = os.path.join(source, meta_filename)
        assets = []
        if os.path.isfile(path):
            window['Save'].update(disabled=False)
            with open(path, encoding='utf8') as inp:
                for l in inp:
                    if l.startswith('assets.'):
                        asset = l.split(': ', 1)[0]
                        assets.append(asset)
            return list(set(assets))
        else:
            window['Save'].update(disabled=True)
            return []


    assets = 'image, thumbnail, video'.split(', ')
    assets = dict(
            image=('screenshot','jpg'),
            thumbnail=('wheel', 'png'),
            video=('videos', 'mp4') )
    exts = opts['Image Types'].split(',')
    source = opts['History'][0]

    layout = [[sg.Text('Source', size=12),
                sg.Combo(opts['History'], default_value=source, size=(50,1),
                enable_events=True, bind_return_key=True, key='Source'),
                sg.FolderBrowse(initial_folder=source)],
            [sg.Checkbox('Add Missing Files', default=True, key='missing')],
            [[sg.Text(asset, size=12),
                sg.Combo([], size=50, key=asset, readonly=True),
                sg.Combo(exts, default_value=assets[asset][1], size=5, key=asset+'-ext')]
                for asset in assets.keys()], 
            [sg.Text('')],
            [sg.Push(), sg.Button('Save', disabled=True)] ]
    
    window = sg.Window('Export XML', layout, finalize=True)
    results = False
    if os.path.isdir(source):
        update_path()

    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        
        elif event == 'Source':
            if os.path.isdir(values['Source']):
                source = values['Source']
                update_history(source, window['Source'])
                update_path()
        
        elif event == 'Save':
            export_xml(source, values)
        
    window.close()


def export_xml(path, values):
    convert = dict(
            game='name',
            file='path',
            description='desc',
            release='releasedate')

    games, ignored = scan_metadata(path, True, False)
    update_xml_images(games, path, values)
    print(ignored)
      
    root = ET.Element("gameList")
    root.text = '\n\t'
    for i in games:
        src = i.pop('x-source', None)
        _id = i.pop('x-id', None)
        if _id and src:
            game = ET.SubElement(root, "game", id=_id, source=src)
        else: game = ET.SubElement(root, "game")

        file = i['file']
        if file in ignored:
            i['hidden'] = 'true'
        if not os.path.isfile(file):
            i['file'] = './'+file

        game.tail = '\n\t'
        game.text = '\n\t\t'
        for k, v in i.items():
            if not k.startswith('assets.'):
                e = ET.SubElement(game, convert.get(k, k))
                e.text = v.rstrip('\n')
                e.tail = '\n\t\t'
        e.tail = e.tail[:-1]
    game.tail = game.tail[:-1]

    outfn = os.path.join(path, 'gamelist.xml')
    if os.path.isfile(outfn):
        os.rename(outfn, outfn+ '.b')

    tree = ET.ElementTree(root)
    tree.write(outfn)


def theme_window(theme=None):
    if theme:
        sg.theme(theme)
    else:
        theme = opts['Theme']
    themes = sg.theme_list()
    font, size = opts['Font']

    layout = [[sg.Listbox(values=themes, size=(30,10), key='List',
                    enable_events=True)],
             [sg.Text('Size:'), sg.Slider(default_value=size, range=(6,32),
                    key='size', orientation='h')],
             [sg.Checkbox('Show Tooltips', default=opts['Tooltips'],
                    key='tooltips')],
             [sg.Push(), sg.Button('Cancel'), sg.Button('Change')]]
 
    window = sg.Window("Theme Chooser", layout, finalize=True)
    #sg.theme(options.get('theme', ''))

    if theme in themes:
        i = themes.index(theme)
        window['List'].update(set_to_index=[i], scroll_to_index=max(i-3, 0))
    while True:
        event, values = window.read()
        if event == 'Change':
            theme = values.get('List')
            new_size = int(values.get('size', size))
            opts['Font'] = (font, new_size)
            opts['Tooltips'] = values['tooltips']
            if new_size != size:
                print('Size changed to', new_size)
            if theme and theme[0] in themes:
                theme = theme[0]
                print('Theme changed to', theme)
                opts['Theme'] = theme
            window.close()
            break
              
        elif event in (sg.WIN_CLOSED, 'Cancel'):
            print('Canceled theme change')
            window.close()
            break
        elif event == 'List':
            theme = values['List'][0]
            window.close()
            theme_window(theme)


def update_xml_images(games, path, values):
    missing = values['missing']

    for g in games:
        for im in ('image', 'thumbnail', 'video'):
            if values[im].startswith('assets.'):
                if values[im] in g:
                    g[im] = g[values[im]]
            elif values[im]:
                for ext in opts['Image Types'].split(','):
                    fn = os.path.join(values[im], g['file']) + '.' + ext
                    if os.path.isfile(fn):
                        break
                else:
                    ext = values[im+'-ext']
                    fn = os.path.join(values[im], g['file']) + '.' + ext

                if os.path.isfile(fn) or missing:
                    fn = './' + os.path.relpath(fn, path)
                    g[im] = fn


def import_xml_window():
    '''
    Import Pegasus metadata to a gamelist.xml file  

    This tool reads an EmulationStation gamelist.xml file and saves it as a
    metadata.pegasus.txt file. Select a source folder that includes a gamelist.xml file
    and any desired image assets. Then select which Pegasus image asset you want to assign
    the gamelist's image and thumbnail values to. 

    No Pegasus asset link will be created if the gamelist asset doesn't exist. You can
    add them using the Add Asset tool. 
    '''
    xml_assets = 'image, thumbnail'.split(', ')
    peg_assets = ['assets.'+a for a in
            'banner, box_front, fanart, logo, screenshot, titlescreen'.split(', ')]
    defaults = dict(image='assets.screenshot', thumbnail='assets.box_front')
    exts = opts['Image Types'].split(',')
    source = opts['History'][0]

    layout = [[sg.Text('Source', size=12),
                sg.Combo(opts['History'], default_value=source, size=(50,1),
                enable_events=True, bind_return_key=True, key='Source'),
                sg.FolderBrowse(initial_folder=source)], [sg.Text('')],
            #[sg.Checkbox('Add Missing Files', default=True, key='missing')],
            [[sg.Push(), sg.Text(asset, size=12),
                sg.Combo(peg_assets, default_value=defaults[asset],
                    size=50, key=asset, readonly=True)]
                for asset in xml_assets], 
            [sg.Push(), sg.Button('Import', disabled= not os.path.isfile(
                    os.path.join(source, 'gamelist.xml')))] ]
    
    window = sg.Window('Import XML', layout, finalize=True)
    results = False

    while True:
        event, values = window.read()
        values = values or {}

        if event in ('Cancel', sg.WIN_CLOSED):
            break
        
        elif event == 'Source':
            if os.path.isfile(os.path.join(values['Source'], 'gamelist.xml')):
                source = values['Source']
                update_history(source, window['Source'])
                window['Import'].update(disabled=False)
            else:
                window['Import'].update(disabled=True)
        
        elif event == 'Import':
            import_xml(source, values)
            break
        
    window.close()


def import_xml(path, values):
    convert = dict(
            path='file',
            desc='description',
            releasedate='release',
            develper='developer',
            publisher='publisher',
            players='players' )

    out_fn = os.path.join(path, meta_filename)
    if os.path.isfile(out_fn):
        os.rename(out_fn, out_fn+'.b')
    gamelist = ET.parse(os.path.join(path, 'gamelist.xml')).getroot()

    with open(out_fn, 'w', encoding='utf8') as outp:
        for game in gamelist:
            name = game.findtext('name')
            if name:
                src = game.attrib.get('source', None)
                _id = game.attrib.get('id', None)

                print('game:', name, file=outp)
                for a in game:
                    if a.tag == 'desc':
                        print('description:', file=outp)
                        if a.text:
                            for l in a.text.split('\n'):
                                print('  ', l, file=outp)
                    elif a.tag == 'releasedate' and a.text:
                        date = a.text
                        print('release: {}-{}-{}'.format(
                            date[:4], date[4:6], date[6:8]), file=outp)
                    elif a.tag in convert:
                        print('{}: {}'.format(
                            convert.get(a.tag, a.tag),
                            a.text), file=outp)
                    im = game.findtext('image')
                    thumb = game.findtext('thumb') or game.findtext('thumbnail')
                    vid = game.findtext('video')

                if _id and src:
                    print('x-source: {}\nx-id: {}'.format(src, _id), file=outp)
                if im:
                    print('{}: {}'.format(values['image'], im), file=outp)
                if thumb:
                    print('{}: {}'.format(values['thumbnail'], thumb), file=outp)
                if vid:
                    print('assets.video: {}'.format(vid), file=outp)

                print('\n', file=outp)


def launch_tool(name):
    if name in windows:
        p = mp.Process(target=windows[name])
        p.start()
        opts.save()

tools = {
    'Add Assets': add_assets_window,
    'Backup Metadata': backup_metadata_window,
    'Check Files': check_file_window,
    'Edit Genres': edit_genre_window,
    'Export XML': export_xml_window,
    'Hide Disks': hide_disks,
    'Import XML': import_xml_window,
    'Make Image Mixes': make_mix_window,
    'Options': option_window,
    'Remove Assets': remove_assets }
windows = {
    'help': help_window,
    'theme': theme_window }
windows.update(tools)

opts = Options()
if __name__ == '__main__':
    if 'linux' in sys.platform:
        mp.set_start_method('forkserver')
    if len(sys.argv) > 1 and sys.argv[1]:
        if sys.argv[1] in windows.keys():
            windows[sys.argv[1]]()
            opts.save()
    else:
        menu_window()