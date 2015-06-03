#!/usr/bin/env python3
"""gnome-app-folder

Usage:
    gnome-app-folder list [<folder>]
    gnome-app-folder new <folder>
    gnome-app-folder delete <folder> [--force]
    gnome-app-folder add <folder> (FILES ...)
    gnome-app-folder remove <folder> (FILES ...)
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

def list_folder(folder):
    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    for key in folder_settings.list_keys():
        print(key, ":" ,folder_settings.get_value(key))

def add_files(folder, files):
    if folder not in get_folders():
        print("Error: The folder '{}' does not exist".format(folder))
        return

    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    files_list = folder_settings.get_strv('apps')
    added_files = []
    for file in files:
        if file not in files_list:
            files_list.append(file)
            added_files.append(file)
        else:
            print('Warning: {} already exists in {}'.format(file, folder))

    if len(added_files) > 0:
        folder_settings.set_strv('apps', files_list)
        print("Successfully added", *added_files)

def remove_files(folder, files):
    if folder not in get_folders():
        print("Error: The folder '{}' does not exist".format(folder))
        return

    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    files_list = folder_settings.get_strv('apps')
    removed_files = []
    for file in files:
        if file in files_list:
            files_list.remove(file)
            removed_files.append(file)
        else:
            print('Warning: {} is not in {}'.format(file, folder))

    if len(removed_files) > 0:
        folder_settings.set_strv('apps', files_list)
        print("Successfully removed", *removed_files)


def new_folder(folder):
    list = get_folders()
    if folder in list:
        print("Error: {} already exists".format(folder))
        return

    list.append(folder)

    gsettings = Gio.Settings.new(SCHEMA_APP_FOLDER)
    if not gsettings.set_strv('folder-children', list):
        print("Error: Unknwon error occured")
        return

    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    folder_settings.set_string('name', folder)

    print("{} successfully added".format(folder))

def delete_folder(folder):
    list = get_folders()
    if folder not in list:
        print("Error: {} does not exists".format(folder))
        return

    list.remove(folder)

    # Clean folder settings
    folder_settings = Gio.Settings.new_with_path(SCHEMA_FOLDER, gen_folder_path(folder))
    for key in folder_settings.list_keys():
        folder_settings.reset(key)

    app_folder_settings = Gio.Settings.new(SCHEMA_APP_FOLDER)
    if not app_folder_settings.set_strv('folder-children', list):
        print("Error: Unknwon error occured")
        return

    print("{} successfully removed".format(folder))

if __name__ == '__main__':
    args = docopt(__doc__, version=VERSION)
    if args['list']:
        if args['<folder>']:
            list_folder(args['<folder>'])
        else:
            for folder in get_folders():
                print(folder)

    elif args['new']:
        new_folder(args['<folder>'])

    elif args['delete']:
        delete_folder(args['<folder>'])

    elif args['add']:
        add_files(args['<folder>'], args['FILES'])

    elif args['remove']:
        remove_files(args['<folder>'], args['FILES'])
