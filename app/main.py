"""Main Python application file for the EEL-CRA demo."""

import os
import pathlib
import platform
import random
import sys

import eel
from nwpy import scan, get_default_iface_name_linux, list_interfaces

UI_FOLDER = (pathlib.Path(__file__) / '../../ui').absolute()


@eel.expose('defaultInterface')
def default_interface():
    return get_default_iface_name_linux()

@eel.expose('listInterfaces')
def eel_list_interfaces():
    return list_interfaces()

@eel.expose('scan')
def scan_network(iface):
    """Scan the network for hosts."""
    return scan(iface)

def start_eel(develop):
    """Start Eel with either production or development configuration."""

    if develop:
        directory = (UI_FOLDER / 'src').absolute()
        app = None
        page = {'port': 3000}
    else:
        directory = UI_FOLDER / 'build'
        app = 'chrome-app'
        page = 'index.html'

    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

    eel.say_hello_js('Python World!')   # Call a JavaScript function (must be after `eel.init()`)

    

    eel_kwargs = dict(
        host='localhost',
        port=8888,
        size=(1280, 800),
    )
    try:
        eel.start(page, mode=app, **eel_kwargs)
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start(page, mode='edge', **eel_kwargs)
        else:
            raise


if __name__ == '__main__':
    import sys

    # Pass any second argument to enable debugging
    start_eel(develop=len(sys.argv) == 2)