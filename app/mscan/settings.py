from pathlib import Path
import argparse
import logging

# Command line arguments
parser = argparse.ArgumentParser("Mscan", description="Modern network scanner")
parser.add_argument("--port", default=8000, required=False, type=int)
parser.add_argument("--host", default="127.0.0.1", required=False)
args = parser.parse_args()

# General Settings
DEV_MODE = False
LOG_LEVEL = logging.INFO if DEV_MODE else logging.CRITICAL

# Server settings
PROTOCOL = 'http'
HOST = args.host
PORT = args.port

# UI settings
UI_BUILD_PATH = (Path(__file__).parent / ("../../ui/build" if DEV_MODE else 'static')).resolve().absolute()
UI_BUILD_PATH.mkdir(exist_ok=True)
