import win32api
import win32con
import win32gui
import time

import win32process

hwndChild = 0

i = 0
while True:
    hwndChild = win32gui.FindWindowEx(None, hwndChild, None, None)
    print(hwndChild, i, type(hwndChild))
    i += 1
    if hwndChild == 0:
        # print('cann\'t find 同花顺')
        break
    if win32gui.IsWindowVisible(hwndChild):
        win_text = win32gui.GetWindowText(hwndChild)
        # print(win_text[0:3])
        if win_text[0:3] == '同花顺':
            break

print(hwndChild)
if hwndChild != 0:
    print(win32gui.PostMessage(hwndChild, win32con.WM_KEYDOWN, ord('6') & 0xFF, 0))
    print(win32gui.PostMessage(hwndChild, win32con.WM_KEYUP, ord('6') & 0xFF, 0))
    time.sleep(0.3)
    win32gui.SetForegroundWindow(hwndChild)
    self_thread_id = win32api.GetCurrentThreadId()
    fore_thread_id = win32process.GetWindowThreadProcessId(hwndChild)
    print(self_thread_id, fore_thread_id)
    print(win32process.AttachThreadInput(fore_thread_id[0], self_thread_id, True))
    objwnd = win32gui.GetFocus()
    str = '600030'
    win32gui.SendMessage(objwnd, win32con.WM_SETTEXT, 0, str)
    win32gui.PostMessage(objwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.PostMessage(objwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    win32process.AttachThreadInput(fore_thread_id[0], self_thread_id, False)

