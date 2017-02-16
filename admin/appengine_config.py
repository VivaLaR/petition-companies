import os.path
import sys

# This allows packages in local lib folder to be used by GAE
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))


def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser
