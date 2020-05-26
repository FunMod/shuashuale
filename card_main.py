from mfrc522 import SimpleMFRC522
import pymysql
import os
from gpiozero import Button
import RPi.GPIO as GPIO
reader = SimpleMFRC522()


class Card(object):  # 定义Card类
    def __init__(self):
        self.conn = pymysql.connect(  # 连接MySQL数据库
            host='localhost',
            port=3306,
            database='card_test',
            user='root',
            password='zzu2017',
            charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        GPIO.cleanup()
        print('异常退出！')

    def id_get(self):  # 获取卡片内容（互动标签为action，学习标签为read）
        id, text = reader.read()
        return text

    def con_get(self, con):  # 获取con内容（标签对应的本地文件）
        sql = "select * from card_01 where name = %s"
        self.cursor.execute(sql, con)
        con = self.cursor.fetchone()
        return con[2]

    def read(self, text):  # 语音输出方法
        cmd = "mplayer " + text
        os.system(cmd)

    def Butt(self):  # 按钮方法
        button = Button(2)

        while True:
            if button.is_pressed:
                pass
            else:
                pass

    def listen(self):
        os.system("./iat_sample ")
        try:
            with open("text.txt", "r") as file:
                result_text = file.read()
            return result_text
        except KeyError:
            print("KeyError")

    def rec(self):
        os.system("arecord -d 3 -r 16000 -c 1 -t wav -f S16_LE temp.wav")

    def wrong(self):
        self.read('voice/wrong.wav')
        self.id_get()
        self.read('voice/ding.wav')
        self.rec()
        ans = self.listen()
        return ans

    def run(self):  # 执行程序的方法
        # 接受来自NFC的信息并判断下一步操作:选择模式
        while True:
            # self.read('voice/hello.wav')
            text = self.id_get()
            print(text)
            if 'action' in text:  # 判断操作卡片指令是否为互动
                print('已选择互动模式')
                pass
            elif 'read' in text:  # 判断操作卡片指令是否为朗读
                print('已选择学习模式')
                #  朗读模式：刷卡直接输出语音
                self.read(self.con_get(text[0:3]))
            elif 'guess' in text:  # 语音答题功能
                self.cursor.execute("""select * from card_guess where id >= 
                ((select max(id) from card_guess)-
                (select min(id) from card_guess)) * rand()
                 + (select min(id) from card_guess) limit 1""")  # 从数据库中随机取一条谜语
                result = self.cursor.fetchone()
                self.read(result[2])
                self.id_get()  # 刷卡后开启答题
                self.read('voice/ding.wav')
                self.rec()
                ans = self.listen()
                if result[3] in ans:
                    self.read('voice/right.wav')
                else:
                    ans = self.wrong()
                    if result[3] in ans:
                        self.read('voice/right.wav')
                    else:
                        ans = self.wrong()
                        if result[3] in ans:
                            self.read('voice/right.wav')
                        else:
                            self.read('voice/tips.wav')
                            self.read(result[4])
            else:
                self.read('voice/hello_again.wav')  # 不属于以上两种情况则语音提示重新选择操作模式


def main():  # 由Card类定义主函数对象
    card = Card()
    card.run()  # 调用run方法


if __name__ == '__main__':  # 这里执行主程序main
    # while True:  # 循环执行主函数。出现错误重新运行
    try:
        main()
    except BaseException:  # 捕获异常退出
        Card().__del__
