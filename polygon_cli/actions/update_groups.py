from .common import *

# Hmm, it seems that this works by using utils.parse_script_groups to read
# <#-- group --> tags out of the Freemarker script file to get test groups,
# but I can't find any references to this method for specifying test groups.
#
# It seems either that this is a custom element of the polygon-cli, or this is
# a deprecated format.
#
# In either case, I think it would be easier not to maintain support for test
# groups until I really understand the semantics here.
def update_groups(options):
    if not load_session_with_options(options):
        fatal('No session known. Use init first.')
    content = global_vars.problem.get_script_content()
    global_vars.problem.update_groups(content)
    save_session()


def add_parser(subparsers):
    parser_update_groups = subparsers.add_parser(
            'update_groups',
            help="Update groups for tests using script file"
    )
    parser_update_groups.set_defaults(func=update_groups)
