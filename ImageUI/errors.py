from ImageUI import Settings
from ImageUI import Colors
import traceback


def ShowError(Type, Message):
    try:
        while Message.startswith('\n'):
            Message = Message[1:]
        while Message.endswith('\n'):
            Message = Message[:-1]
        if Settings.DevelopmentMode == False:
            Message = f"{Colors.RED}>{Colors.NORMAL} " + Message.replace("\n", f"\n{Colors.RED}>{Colors.NORMAL} ")
        print(f"{Colors.RED}{Type}{Colors.NORMAL}\n{Message}\n")
    except:
        print(f"Failed to parse the following error message:\n{Type}\n{Message}\n\nTraceback:\n{str(traceback.format_exc())}")