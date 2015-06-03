# gnome-app-folder

A CLI manager for Gnome's app-folders

Tested on Gnome 3.16.2

## Requirements

* docopt
* Gnome python bindings

## Usages

### Query what folders exist

`gnome-app-folder list`

### Make a new folder

`gnome-app-folder new folder`

### Add to the folder

`gnome-app-folder add folder gvim.desktop`

### Query what is in the folder

`gnome-app-folder list folder`

### Remove from the folder

`gnome-app-folder remove folder gvim.desktop`

### Delete folder

`gnome-app-folder delete folder`

## TODO

* edit folder settings like `name`
