from .local_file import LocalFile
from .polygon_file import PolygonFile


def my_json_encoder(obj):
    if isinstance(obj, PolygonFile):
        # TODO: I don't think this should be possible, so I'm going
        # to assert false here
        raise TypeError("This should not be able to be a PolygonFile")
        res = obj.__dict__
        res.update({'__type': 'PolygonFile'})
        return res
    if isinstance(obj, LocalFile):
        res = obj.__dict__
        res.update({'__type': 'LocalFile'})
        return res
    raise TypeError("Unknown type in my_json_encoder")


def my_json_decoder(dct):
    if '__type' not in dct:
        return dct
    if dct['__type'] == 'PolygonFile':
        # TODO: I don't think this should be possible, so I'm going
        # to assert false here
        raise TypeError("This should not be able to be a PolygonFile")
        res = PolygonFile()
        res.by_dict(dct)
        return res
    if dct['__type'] == 'LocalFile':
        res = LocalFile()
        res.by_dict(dct)
        return res
    raise TypeError("Unknown type in my_json_decoder")
