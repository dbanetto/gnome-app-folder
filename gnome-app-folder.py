#!/usr/bin/env python3
"""gnome-app-folder

Usage:
    gnome-app-folder list [<folder>]
    gnome-app-folder new <folder>
    gnome-app-folder delete <folder> [--force]
    gnome-app-folder add <folder> <file>
    gnome-app-folder remove <folder> <file>
    gnome-app-folder --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
from gi.repository import Gio

VERSION='gnome-app-folder 0.1'
SCHEMA_APP_FOLDER = 'org.gnome.desktop.app-folders'
SCHEMA_FOLDER = 'org.gnome.desktop.app-folders.folder'
SCHEMA_FOLDER_PATH = '/org/gnome/desktop/app-folders/folders/{}/'

def gen_folder_path(folder):
    return SCHEMA_FOLDER_PATH.format(folder)

def get_folders():
    gsettings = Gio.Settings.new(SCHEMA_APP_FOLDER)
    return gsettings.get_strv('folder-children')

def new_folder(folder):
    list = get_folders()
    if folder in list:
        print("Error: {} already exists".format(folder))
        return

    list.append(folder)

    gsettings = Gio.Settings.new(SCHEMA_APP_FOLDER)
    if gsettings.set_strv('folder-children', list):
        print("{} successfully added".format(folder))
    else:
        print("Error: Unknwon error occured")

    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    folder_settings.set_string('name', folder)

def delete_folder(folder):
    list = get_folders()
    if folder not in list:
        print("Error: {} does not exists".format(folder))
        return
    list.remove(folder)

    app_folder_settings = Gio.Settings.new(SCHEMA_APP_FOLDER)
    if app_folder_settings.set_strv('folder-children', list):
        print("{} successfully removed".format(folder))
    else:
        print("Error: Unknwon error occured")

    # Clean folder settings
    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    for key in folder_settings.list_keys():
        folder_settings.reset(key)

if __name__ == '__main__':
    args = docopt(__doc__, version=VERSION)
    # print(args) #TODO: Remove me

    if args['list']:
        if args['<folder>']:
            print("Not implemented yet")
        else:
            for folder in get_folders():
                print(folder)
    elif args['new'] and args['<folder>']:
        new_folder(args['<folder>'])
    elif args['delete'] and args['<folder>']:
        delete_folder(args['<folder>'])
    elif args['add']:
        print("Not implemented yet")
    elif args['remove']:
        print("Not implemented yet")
