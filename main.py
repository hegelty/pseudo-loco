import time
import send


def main():
    send.init()
    message = send.TextMessage()
    room = "카봇커 봇 분양/실험방"
    message.text("Hello World!").mention("헤겔").text("dufjaud")
    send.send_message(room, message)
    send.send_file(room, "17527-Article Text-21021-1-2-20210518.pdf")
    send.send_message(room, send.TextMessage().text("테스트2").lw())
    send.send_message(room, send.TextMessage().text("테스트3"))
    send.send_file(room, "main.py")


if __name__ == '__main__':
    main()
