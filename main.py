import time
import send


def main():
    send.init()
    start = time.perf_counter()
    message = send.TextMessage()
    message.text("Hello World!")
    message.mention("시계톡톡")
    message.text("dufjaud")
    message.mention("성빈2")
    send.send_message("카봇커 봇 분양/실험방", message)

    #.send_file("카봇커 봇 분양/실험방", "main.py")
    #send.send_file("카봇커 봇 분양/실험방", "17527-Article Text-21021-1-2-20210518.pdf")
    end = time.perf_counter()
    print(f'{(end - start)*1000}ms')


if __name__ == '__main__':
    main()
