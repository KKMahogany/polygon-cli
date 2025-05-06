from .common import *


def process_download_last_package(options):
    raise NotImplementedError


def add_parser(subparsers):
    parser_download_package = subparsers.add_parser(
            'download_package',
            help="Downloads package"
    )
    parser_download_package.set_defaults(func=process_download_last_package)
