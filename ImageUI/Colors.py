RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
NORMAL = "\033[0m"


THEME = "Dark"

TEXT_COLOR = (255, 255, 255) if THEME == "Dark" else (0, 0, 0)
GRAY_TEXT_COLOR = (155, 155, 155) if THEME == "Dark" else (100, 100, 100)

BUTTON_COLOR = (42, 42, 42) if THEME == "Dark" else (236, 236, 236)
BUTTON_HOVER_COLOR = (47, 47, 47) if THEME == "Dark" else (231, 231, 231)

SWITCH_COLOR = (60, 60, 60) if THEME == "Dark" else (208, 208, 208)
SWITCH_HOVER_COLOR = (65, 65, 65) if THEME == "Dark" else (203, 203, 203)
SWITCH_KNOB_COLOR = (28, 28, 28) if THEME == "Dark" else (250, 250, 250)
SWITCH_ENABLED_COLOR = (255, 200, 87) if THEME == "Dark" else (184, 95, 0)
SWITCH_ENABLED_HOVER_COLOR = (255, 200, 87) if THEME == "Dark" else (184, 95, 0)

DROPDOWN_COLOR = (42, 42, 42) if THEME == "Dark" else (236, 236, 236)
DROPDOWN_HOVER_COLOR = (47, 47, 47) if THEME == "Dark" else (231, 231, 231)

POPUP_COLOR = (42, 42, 42) if THEME == "Dark" else (236, 236, 236)
POPUP_OUTLINE_COLOR = (155, 155, 155) if THEME == "Dark" else (100, 100, 100)
POPUP_PROGRESS_BAR_COLOR = (255, 200, 87) if THEME == "Dark" else (184, 95, 0)