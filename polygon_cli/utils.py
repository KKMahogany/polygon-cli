#!/usr/bin/env python

import os
import re
import shutil
import sys
from subprocess import Popen, PIPE
import subprocess

from . import config


def read_file(filename):
    f = open(filename, 'rb')
    l = f.readlines()
    f.close()
    return l


# Used in a bunch of places
def safe_rewrite_file(path, content, openmode='wb'):
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if openmode.endswith('b'):
        content = convert_to_bytes(content)
    if os.path.exists(path):
        # I'm really unclear on what this is for.
        shutil.copy(path, path + ".$$$")
        open(path, openmode).write(content)
        os.remove(path + '.$$$')
    else:
        open(path, openmode).write(content)


# Only used in the update command
def _merge_files(old, our, theirs):
    if open(old, 'rb').read().splitlines() == open(theirs, 'rb').read().splitlines():
        return 'Not changed'
    p = Popen(_get_merge_tool(old, our, theirs), stdout=PIPE, shell=True)
    diff3out, _ = p.communicate()
    return_value = 'Merged'
    if p.returncode == 1:
        print('Conflict in file %s' % our)
        return_value = 'Conflict'
    elif p.returncode != 0:
        raise Exception("diff3 failed!")
    if return_value != 'Conflict':
        safe_rewrite_file(our, diff3out, 'wb')
    else:
        safe_rewrite_file(our + '.diff', diff3out, 'wb')
        shutil.copy(theirs, our + '.new')
    return return_value

# Only used in the update command
def safe_update_file(old_path, new_path, content):
    open(old_path + '.new', 'wb').write(content)
    return_value = _merge_files(old_path, new_path, old_path + '.new')
    shutil.move(old_path + '.new', old_path)
    return return_value


def _diff_files(old, our, theirs):
    subprocess.run(_get_diff_tool(old, our, theirs),
                   stdout=sys.stdout,
                   shell=True)

def diff_file_with_content(old_path, new_path, content):
    open(old_path + '.new', 'wb').write(content)
    _diff_files(old_path, new_path, old_path + '.new')


def get_local_solutions():
    return os.listdir(config.solutions_path)


# When script is changed, need to check if groupings are specified.
# If so, we need to update test groups.
def need_update_groups(content):
    match = re.search(rb"<#-- *group *([-0-9]*) *(score *(\d*))? *(depends *([-0-9]* +)*)? *-->", content)
    return match is not None


def convert_to_bytes(x):
    if isinstance(x, bytes):
        return x
    return bytes(str(x), 'utf8')


def get_api_file_type(type):
    if type == 'source' or type == 'resource':
        return type
    if type == 'attachment':
        return 'aux'
    return None

def _get_merge_tool(old, our, theirs):
    if sys.platform == 'darwin':
        return ' '.join(["diff3", "--merge", our, old, theirs])
    else:
        return ' '.join(["diff3", "--strip-trailing-cr", "--merge", our, old, theirs])

def _get_diff_tool(old, our, theirs):
    return ' '.join(["diff", theirs, our])


