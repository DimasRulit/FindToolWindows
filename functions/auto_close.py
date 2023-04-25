import win32api
import time

def mouse_click(root, result_queue):
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    midWidth = int((width + 1) / 2)
    midHeight = int((height + 1) / 2)

    state_left = win32api.GetKeyState(0x01)  # Left button up = 0 or 1. Button down = -127 or -128
    state_right = win32api.GetKeyState(0x02)

    while True:
        left_state = win32api.GetKeyState(0x01)
        if left_state != state_left:  # Left button state changed
            state_left = left_state
            if left_state < 0:
                x, y = win32api.GetCursorPos()
                if not (root.winfo_rootx() <= x <= root.winfo_rootx() + root.winfo_width() and
                        root.winfo_rooty() <= y <= root.winfo_rooty() + root.winfo_height()):
                    text_1 = 'clicked'
                    result_queue.put(text_1)

            else:
                print('Left Button Released')

        right_state = win32api.GetKeyState(0x02)
        if right_state != state_right:  # Right button state changed
            state_right = right_state
            print(right_state)
            if right_state < 0:

                x, y = win32api.GetCursorPos()
                if not (root.winfo_rootx() <= x <= root.winfo_rootx() + root.winfo_width() and
                        root.winfo_rooty() <= y <= root.winfo_rooty() + root.winfo_height()):
                    text_1 = 'clicked'
                    result_queue.put(text_1)
                # Do something when right button is pressed
            else:
                print('Right Button Released')

        time.sleep(0.001)
