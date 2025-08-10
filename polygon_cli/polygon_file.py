from . import config
from . import global_vars
from . import utils

# This class represents a "file" object on polygon. It generally
# corresponds 1:1 to "files" you upload, except statements are sort of
# a special case.
#
# On polygon, a statement is divided into semantic sections (name,
# legend, input format etc.). Under the hood polygon has a separate
# .tex file for each of these, so it is still 1:1.
class PolygonFile:
    def __init__(self):
        self.name = None
        # See subdirectory_paths for a list of valid types
        self.type = None
        self.date = None
        self.size = None
        self.content = None

    @staticmethod
    def to_byte(value, encoding):
        return value.encode(encoding=encoding) if encoding else value.encode()

    def __repr__(self):
        return str(self.__dict__)

    # Constructor-like method for loading from a json_encoders.py dump
    def by_dict(self, data):
        for key in data.keys():
            if key != '__type':
                setattr(self, key, data[key])

    def get_content(self):
        """

        :rtype: bytes
        """
        if self.type == 'script':
            file_text = global_vars.problem.load_script()
        elif self.type == 'solution':
            file_text = global_vars.problem.send_api_request('problem.viewSolution', {'name': self.name}, False)
        elif self.type == 'statement':
            if self.content is not None:
                # Pre-populated by get_statements_list for efficiency.
                # Doing an API request per section (name, legend, input
                # format, output format etc.) will be annoyingly slow.
                file_text = self.content
            else:
                data = global_vars.problem.send_api_request('problem.statements', {})
                lang, name = self.name.split('/')
                data = data.get(lang, {})
                if name.endswith(".tex"):
                    name = name[:-4]
                else:
                    print(f'Unexpected non-latex statement file {name}')
                    assert(False)
                encoding = data.get('encoding', None)
                content = data.get(name, None)
                file_text = PolygonFile.to_byte(content, encoding)
        else:
            file_text = global_vars.problem.send_api_request('problem.viewFile',
                                                             {'name': self.name,
                                                              'type': utils.get_api_file_type(self.type)}, False)
        return file_text

    # Map from polygon path to local path (sort of PolygonFile to LocalFile)
    def get_default_local_dir(self):
        if self.type in list(config.subdirectory_paths.keys()):
            return config.subdirectory_paths[self.type]
        raise NotImplementedError("loading files of type %s" % self.type)
