from . import config
from . import global_vars
from . import utils

# Polygon API to list files returns only metadata for each file.
# This class represents that metadata.
#
# You actually have to call get_content to call the API and get the data.
#
# If you want to work with the file, convert it to an appropriate LocalFile before using it.
class PolygonFile:
    def __init__(self):
        # Directly from the File object returned by the API
        self.name = None
        self.date = None
        self.size = None

        # Our internal concept of file type -- not polygon's.
        # See local_file.py and subdirectory_paths for a list of valid types
        self.type = None

        # Field to save statement content for get_statements_list. It returns all
        # the content, so no need to issue API requests for each piece of the statement
        # individually.
        self.statement_content = None

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
            if self.statement_content is not None:
                # Pre-populated by get_statements_list for efficiency.
                # Doing an API request per section (name, legend, input
                # format, output format etc.) will be annoyingly slow.
                file_text = self.statement_content
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
