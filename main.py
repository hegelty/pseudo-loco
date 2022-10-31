import time
import send


def main():
    send.init()
    start = time.perf_counter()
    message = send.TextMessage()
    message.text("테스트 메세지")
    message.mention("헤겔")
    message.lw()
    message.text("테스트")
    send.send_message("카봇커 봇 분양/실험방", message)

    #send.send_file("카봇커 봇 분양/실험방", "C:\\Users\\skxod\\Downloads\\a.png")
    #send.send_file("카봇커 봇 분양/실험방", "C:\\Users\\skxod\\Downloads\\17527-Article Text-21021-1-2-20210518.pdf")
    end = time.perf_counter()
    print(f'{(end - start)*1000}ms')


if __name__ == '__main__':
    main()
