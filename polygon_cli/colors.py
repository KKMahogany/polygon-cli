import colorama

colorama.init(autoreset=True)


def _colored(color):
    return lambda message, *args: color + message.format(*args) + colorama.Style.RESET_ALL


error = _colored(colorama.Fore.RED)
warning = _colored(colorama.Fore.YELLOW)
success = _colored(colorama.Fore.GREEN)
info = _colored(colorama.Fore.CYAN)
