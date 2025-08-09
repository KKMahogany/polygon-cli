from . import colors

verbose = False

# Not intended to be seen except for debugging issues with the CLI
def debug(*args, **kwargs):
    if verbose:
        colors.debug(*args, **kwargs)
