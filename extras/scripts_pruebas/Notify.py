import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
Notify.init("Test App")

# A raw file name/path
Notify.Notification.new(
    "Ding!",
    "Time is up.",
    "/home/dtron/image.png"
).show()

# Or a icon name in the theme
Notify.Notification.new(
    "Ding!",
    "Time is up.",
    "dialog-information" # dialog-warn, dialog-error
).show()
