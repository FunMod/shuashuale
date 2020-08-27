from mfrc522 import SimpleMFRC522
import pymysql
import os
import random
from gpiozero import Button
import RPi.GPIO as GPIO
reader = SimpleMFRC522()


def tr_digit_to_zn(digit):  # 数字转汉字函数
    # 940,2400,0452
    digit = str(digit)
    length = len(digit)
    digit = digit[::-1]
    split = []
    sp_nums = range(0, length, 4)
    for i in sp_nums:
        split.append(digit[i: i + 4][::-1].zfill(4))
    # print(split)
    d_digit_to_zn = {
        0: "零",
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
    }
    res_zn_list = []
    split_count = len(split)
    for i, e in enumerate(split):
        zn = ''
        for j, each in enumerate(e):
            if each == '0':
                if j == 0 and i == split_count - 1:
                    pass
                elif e[j - 1] == '0':
                    pass
                elif e[j:].strip('0'):
                    zn += '零'
            else:
                zn += d_digit_to_zn[int(each)] + {0: '千', 1: '百', 2: '十', 3: ''}[j]
        zn = zn + {0: '', 1: '万', 2: '亿'}[i]
        res_zn_list.append(zn)
    res_zn_list.reverse()
    res_zn = ''.join(res_zn_list)
    # print(res_zn)

    res_zn = [e for e in res_zn]
    for i, e in enumerate(res_zn):
        if e in '百千':
            try:
                if res_zn[i - 1] == '二':
                    res_zn[i - 1] = '两'
            except:
                pass
    res_zn = ''.join(res_zn)

    if res_zn.startswith('一十'):
        res_zn = res_zn[1:]

    if res_zn.startswith('二') and res_zn[1] in ['万', '亿']:
        res_zn = '两' + res_zn[1:]

    return res_zn


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

    def tts(self, text):  # TTS文本合成语音
        cmd = "tts_sample " + text
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
        os.system("arecord -d 1 -r 16000 -c 1 -t wav -f S16_LE temp.wav")

    def calculate(self, f):
        # sym = ['＋', '－', '×', '÷']
        # f = random.randint(0, 3)
        n1 = random.randint(1, 10)
        n2 = random.randint(1, 10)
        result = 0
        if f == 0:  # 加法
            result = n1 + n2
            n1 = tr_digit_to_zn(n1)
            n2 = tr_digit_to_zn(n2)
            question = n1 + '加' + n2 + '等于'
        elif f == 1:  # 减法，要先比较大小，防止输出负数
            n1, n2 = max(n1, n2), min(n1, n2)
            result = n1 - n2
            n1 = tr_digit_to_zn(n1)
            n2 = tr_digit_to_zn(n2)
            question = n1 + '减' + n2 + '等于'
        elif f == 2:  # 乘法
            result = n1 * n2
            n1 = tr_digit_to_zn(n1)
            n2 = tr_digit_to_zn(n2)
            question = n1 + '乘' + n2 + '等于'
        elif f == 3:  # 除法，要比较大小，并循环取整除
            n1, n2 = max(n1, n2), min(n1, n2)
            while n1 % n2 != 0:
                n1 = random.randint(1, 10)
                n2 = random.randint(1, 10)
                n1, n2 = max(n1, n2), min(n1, n2)
            result = int(n1 / n2)
            n1 = tr_digit_to_zn(n1)
            n2 = tr_digit_to_zn(n2)
            question = n1 + '除' + n2 + '等于'
        print(question)
        result_0 = result
        result = tr_digit_to_zn(result)
        return (question, result, result_0)

    def wrong(self):
        self.read('voice/wrong.wav')
        self.id_get()
        self.read('voice/ding.wav')
        self.rec()
        ans = self.listen()
        return ans

# TODO 讲语音识别结果转换为拼音字母，可以提高容错率

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
            elif 'calculate' in text:
                cal = self.calculate(int(text[9]))
                print(cal[0])
                self.tts(cal[0])
                self.id_get()  # 刷卡后开启答题
                self.read('voice/ding.wav')
                self.rec()
                ans = self.listen()
                print(cal[2])
                #  ans = ans + tr_digit_to_zn(ans)
                if tr_digit_to_zn(cal[2]) or str(cal[2]) in ans:
                    self.read('voice/right.wav')
                else:
                    self.read('voice/tips.wav')
                    self.tts(cal[1])                              
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
