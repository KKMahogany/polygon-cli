import os

from . import config
from . import global_vars
from . import utils


# This class represents a "file" object in the local workspace
#
# When polygon_filename is None, this means that the given object is local
# only.
class LocalFile:
    def __init__(self, filename=None, dir=None, name=None, type=None, polygon_filename=None, tag=None):
        """

        :type filename: str or None
        :type dir: str or None
        :type name: str or None
        :type type: str or None
        :type polygon_filename: str or None
        :type tag: str or None
        """

        if type == 'statement':
            assert filename is not None
            assert dir is not None
            assert name is not None
            lang = os.path.basename(dir)
            dir = os.path.dirname(dir)
            filename = lang + '/' + filename
            name = lang + '/' + name

        self.filename = filename
        self.dir = dir
        self.name = name
        self.type = type
        self.polygon_filename = polygon_filename
        self.tag = tag

    def __repr__(self):
        return str(self.__dict__)

    # Constructor-like method for loading from a json_encoders.py dump
    def by_dict(self, data):
        for key in data.keys():
            if key != '__type':
                setattr(self, key, data[key])

    def get_path(self):
        """

        :rtype: str
        """
        return os.path.join(self.dir, self.filename)

    # When a file is pulled down from polygon (via "update" say), a snapshot
    # of its contents are saved in this location to prevent us from accidentally
    # clobbering changes made directly in the web client.
    #
    # NOTE THAT THIS DOES NOT NECESSARILY DEFEND AGAINST OVERWRITING METADATA
    # I STILL NEED TO VERIFY THE BEHAVIOUR THERE
    def get_internal_path(self):
        """

        :rtype: str
        """
        # TODO: This will break if there are multiple files of the same name
        # e.g. a generator called main.cpp and a solution called main.cpp
        return os.path.join(config.internal_directory_path, self.filename)

    # Upload a file for the first time to polygon. If it already exists, you
    # should use "update" instead.
    def upload(self):
        assert self.polygon_filename is None
        file = open(self.get_path(), 'rb')
        content = file.read()
        if self.type == 'script':
            if not global_vars.problem.upload_script(content):
                return False
        elif self.type == 'statement':
            if not global_vars.problem.upload_statement(self.filename, content):
                return False
        elif not global_vars.problem.upload_file(self.filename, self.type, content, True, self.tag):
            return False
        utils.safe_rewrite_file(self.get_internal_path(), content)
        self.polygon_filename = self.filename
        return True

    def update(self):
        assert self.polygon_filename is not None
        file = open(self.get_path(), 'rb')
        content = file.read()
        if self.type == 'script':
            if not global_vars.problem.upload_script(content):
                return False
        elif self.type == 'statement':
            if not global_vars.problem.upload_statement(self.filename, content):
                return False
        elif not global_vars.problem.upload_file(self.filename, self.type, content, False):
            return False
        utils.safe_rewrite_file(self.get_internal_path(), content)
        return True
