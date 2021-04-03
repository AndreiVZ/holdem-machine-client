import time
import random
import win32api
import win32con
import pyautogui


def click_on_area(x1, y1, x2=None, y2=None, clicks=1):
    """Клик левой кнопкой мыши по указанной области экрана

    :param x1, y1: левый верхний угол области
    :param x2, y2: правый нижний угол области (если не указан, то равен x1, y1)
    :param clicks: кол-во кликов
    """
    if not x2 or not y2:
        x2, y2 = x1, y1

    x_dest = random.randint(min(x1, x2), max(x1, x2))
    y_dest = random.randint(min(y1, y2), max(y1, y2))
    x_cur, y_cur = win32api.GetCursorPos()

    random_max = 15
    if abs(x_cur - x_dest) > abs(y_cur - y_dest):
        random_max_x = random_max
        random_max_y = round(random_max / (abs(x_cur - x_dest) / max(abs(y_cur - y_dest), 1)), 0)
        random_max_y = max(random_max_y, 1)
    else:
        random_max_x = round(random_max / (abs(y_cur - y_dest) / max(abs(x_cur - x_dest), 1)), 0)
        random_max_x = max(random_max_x, 1)
        random_max_y = random_max
    got_dest = False

    while x_cur != x_dest or y_cur != y_dest:
        x_cur, y_cur = win32api.GetCursorPos()

        if abs(x_dest - x_cur) <= random_max_x and abs(y_dest - y_cur) <= random_max_y:
            x_random = abs(x_dest - x_cur) if x_dest - x_cur >= 0 else - abs(x_dest - x_cur)
            y_random = abs(y_dest - y_cur) if y_dest - y_cur >= 0 else - abs(y_dest - y_cur)
            got_dest = True
        else:
            x_random = random.randint(1, random_max_x) if x_dest - x_cur >= 0 else - random.randint(1, random_max_x)
            y_random = random.randint(1, random_max_y) if y_dest - y_cur >= 0 else - random.randint(1, random_max_y)

        win32api.SetCursorPos((x_cur + x_random, y_cur + y_random))
        time_random = random.randint(1, 4) / 1000
        time.sleep(time_random)
        if got_dest:
            break

    for i in range(clicks):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        if clicks > 1:
            time.sleep(0.1)


def write_on_area(bet=0):
    """Ввод ставки bet (размер в ББ) по месту курсора"""
    if bet:
        pyautogui.write(str(bet), interval=0.1)
        time.sleep(0.2)
