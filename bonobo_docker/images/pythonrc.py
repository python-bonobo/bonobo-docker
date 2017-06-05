# ~/.pythonrc


def _enable_syntax_completion():
    try:
        import readline
    except ImportError:
        print("Module readline not available.")
    else:
        import rlcompleter
        readline.parse_and_bind("tab: complete")


def _enable_shell_colors():
    import sys
    from colorama import Fore, Style
    sys.ps1 = Fore.LIGHTWHITE_EX + '🐵 >' + Fore.RESET + ' '
    sys.ps2 = Fore.BLACK + '..' + Fore.LIGHTBLACK_EX + '.' + Fore.RESET + ' '


_enable_syntax_completion()
_enable_shell_colors()
del _enable_syntax_completion
del _enable_shell_colors

# Preload bonobo
bonobo = __import__('bonobo')
