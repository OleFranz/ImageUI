from ImageUI import settings
from ImageUI import colors

def ShowError(Type, Message):
    while Message.startswith('\n'):
        Message = Message[1:]
    while Message.endswith('\n'):
        Message = Message[:-1]
    if settings.DevelopmentMode == False:
        Message = f"{colors.RED}>{colors.NORMAL} " + Message.replace("\n", f"\n{colors.RED}>{colors.NORMAL} ")
    print(f"{colors.RED}{Type}{colors.NORMAL}\n{Message}\n")