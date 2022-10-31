from io import BytesIO, StringIO
import win32con as wcon
import win32api as wapi
import win32gui as wgui
import win32clipboard as wclip
from PIL import Image
import pyautogui as pg
import pywinauto
import pygetwindow as gw
import pyperclip
import time
import queue

message_que = queue.Queue()
sending = False
kakao_window = 0


class TextMessage():
    data = []

    def text(self, text: str):
        self.data.append({
            'type': 'text',
            'data': text
        })

    def mention(self, target: str):
        self.data.append({
            'type': 'mention',
            'data': target
        })

    def lw(self):
        self.data.append({
            'type': 'lw',
            'data': ''
        })


def init():
    global kakao_window
    kakao_window = wgui.FindWindow(None, "카카오톡")
    if kakao_window == 0:
        print("카카오톡이 실행되지 않았습니다.")
        exit(0)


# 엔터 입력
def enter(win):
    wapi.PostMessage(win, wcon.WM_KEYDOWN, wcon.VK_RETURN, 0)
    time.sleep(0.01)
    wapi.PostMessage(win, wcon.WM_KEYUP, wcon.VK_RETURN, 0)


# 채팅창 선택
def set_room(room):
    chat_window = wgui.FindWindow(None, room)
    if chat_window == 0:
        chat_window = open_room(room)
        if chat_window == 0:
            return -1
    for i in range(10):
        try:
            chat_box = wgui.FindWindowEx(chat_window, None, "RICHEDIT50W", None)
            if chat_box == -1:
                raise ()
            return chat_box
        except Exception as e:
            time.sleep(0.1)
    return -1


# 채팅창 열기
def open_room(room):
    global kakao_window
    win1 = wgui.FindWindowEx(kakao_window, None, "EVA_ChildWindow", None)
    win2_friends = wgui.FindWindowEx(win1, None, "EVA_Window", None)
    win2_rooms = wgui.FindWindowEx(win1, win2_friends, "EVA_Window", None)

    friends_search = wgui.FindWindowEx(win2_friends, None, "Edit", None)
    rooms_search = wgui.FindWindowEx(win2_rooms, None, "Edit", None)

    wapi.SendMessage(rooms_search, wcon.WM_SETTEXT, 0, room)
    time.sleep(0.15)
    for i in range(3):
        enter(rooms_search)
        time.sleep(0.1)
        chat_window = wgui.FindWindow(None, room)
        if chat_window != 0:
            return chat_window

    wapi.SendMessage(friends_search, wcon.WM_SETTEXT, 0, room)
    time.sleep(0.15)
    for i in range(3):
        enter(friends_search)
        time.sleep(0.1)
        chat_window = wgui.FindWindow(None, room)
        if chat_window != 0:
            return chat_window

    return -1


def send_message(room, message: TextMessage):
    message_que.put({
        "type": 'text',
        "room": room,
        "data": message
    })
    if not sending:
        sender()


def send_file(room, filepath):
    message_que.put({
        "type": "file",
        "room": room,
        "data": filepath
    })
    if not sending:
        sender()


def sender():
    global sending
    sending = True
    while not message_que.empty():
        message = message_que.get()
        room = message["room"]
        message_type = message["type"]
        if message_type == 'text':
            sender_text(room, message["data"])
        elif message_type == 'file':
            sender_file(room, message["data"])
    sending = False


def sender_text(room, message: TextMessage):
    win = gw.getWindowsWithTitle(room)
    if not win:
        set_room(room)
        win = gw.getWindowsWithTitle(room)
        time.sleep(0.3)
    win = win[0]
    if win.isActive == False:
        pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()
    text = ""
    for data in message.data:
        if data["type"] == "text":
            text += data["data"]
        elif data["type"] == "lw":
            text += "\u200b" * 500
        elif data["type"] == "mention":
            pyperclip.copy(text + " @" + data['data'])
            pg.hotkey('ctrl', 'v')
            time.sleep(0.4)
            text = ""
            pg.press('tab')
    if not text == "":
        pyperclip.copy(text)
        pg.hotkey('ctrl', 'v')
    pg.press('enter')
    return


def sender_file(room, filepath):
    win = gw.getWindowsWithTitle(room)
    if not win:
        set_room(room)
        win = gw.getWindowsWithTitle(room)
        time.sleep(0.3)
    win = win[0]
    if win.isActive == False:
        pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()

    time.sleep(0.2)
    pg.hotkey('ctrl', 't')
    time.sleep(0.3)
    pg.press('tab', presses=5, interval=0.02)
    time.sleep(0.05)
    pg.press('enter')
    pg.write("\\".join(filepath.split('\\')[:-1]))
    pg.press('enter')
    time.sleep(0.2)
    pg.press('tab', presses=6, interval=0.05)
    time.sleep(0.1)
    pg.write(filepath.split('\\')[-1])
    time.sleep(0.05)
    pg.press('enter')

    return
