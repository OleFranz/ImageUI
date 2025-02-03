from ImageUI import settings
from ImageUI import colors
import traceback


def ShowError(Type, Message):
    try:
        while Message.startswith('\n'):
            Message = Message[1:]
        while Message.endswith('\n'):
            Message = Message[:-1]
        if settings.DevelopmentMode == False:
            Message = f"{colors.RED}>{colors.NORMAL} " + Message.replace("\n", f"\n{colors.RED}>{colors.NORMAL} ")
        print(f"{colors.RED}{Type}{colors.NORMAL}\n{Message}\n")
    except:
        print(f"Failed to parse the following error message:\n{Type}\n{Message}\n\nTraceback:\n{str(traceback.format_exc())}")