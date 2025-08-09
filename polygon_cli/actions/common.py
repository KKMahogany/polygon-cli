# For methods common to all actions
import json
import os

from .. import config
from .. import global_vars
from .. import json_encoders
from .. import utils
from ..problem import ProblemSession


def fatal(error):
    print(error)
    exit(1)

# Initialise credentials and session data (global_vars.problem, config.*),
# or die if it can't be found.
#
# Only has one option at the moment, verbosity
def load_session_with_options(options):
    _load_session()
    return True # Used to return false on fail, now just dies


def save_session():
    session_data = global_vars.problem.dump_session()
    session_data_json = json.dumps(
            session_data,
            sort_keys=True,
            indent='  ',
            default=json_encoders.my_json_encoder)
    utils.safe_rewrite_file(_session_file_path(), session_data_json)


def _load_session():
    # TODO: I don't like that this utility has to have the working directory
    # be the root of the problem directory.
    if os.path.exists(_session_file_path()):
        session_data_json = open(_session_file_path(), 'r').read()
    elif os.path.exists(os.path.join('..', _session_file_path())):
        os.chdir('..')
        session_data_json = open(_session_file_path(), 'r').read()
    else:
        fatal('No session found. Use init first and make sure you are in the right directory')

    session_data = json.loads(
            session_data_json,
            object_hook=json_encoders.my_json_decoder)

    config.setup_login_by_url(session_data['polygon_name'])
    global_vars.problem = ProblemSession(
            session_data['polygon_name'],
            session_data["problemId"],
            pin=None)

    global_vars.problem.use_ready_session(session_data)

def _session_file_path():
    return os.path.join(config.internal_directory_path, 'session.json')


