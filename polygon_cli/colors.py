import colorama

colorama.init(autoreset=True)

def _colored(color):
    # TODO: Does this need kwargs?
    return lambda message, *args: color + message.format(*args) + colorama.Style.RESET_ALL


# TODO: These should be more clearly named that they just color the string and don't print it.
error = _colored(colorama.Fore.RED)
warning = _colored(colorama.Fore.YELLOW)
success = _colored(colorama.Fore.GREEN)
info = _colored(colorama.Fore.CYAN)

def _print_colored(color):
    return lambda message, *args, **kwargs: print(color + message + colorama.Style.RESET_ALL, *args, **kwargs)

debug = _print_colored(colorama.Fore.LIGHTBLACK_EX)
