#author: hanshiqiang365 （微信公众号）
import requests, random, urllib, time
from lxml import etree
import ctypes


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLUE = 0x09          # 蓝色
FOREGROUND_GREEN = 0x0a         # 绿色
FOREGROUND_RED = 0x0c           # 红色
FOREGROUND_YELLOW = 0x0e        # 黄色
FOREGROUND_WHITE = 0x0f         # 白色

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

# 设置CMD文字颜色
def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

# 重置文字颜色为白色
def resetColor():
    set_cmd_text_color(FOREGROUND_WHITE)

# 在CMD中以指定颜色输出文字
def cprint(mess, color):
    color_dict = {
                  '蓝色': FOREGROUND_BLUE,
                  '绿色': FOREGROUND_GREEN,
                  '红色': FOREGROUND_RED,
                  '黄色': FOREGROUND_YELLOW,
                  '白色': FOREGROUND_WHITE
                 }
    set_cmd_text_color(color_dict[color])
    print(mess)
    resetColor()

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    html = requests.get(url, headers = headers)
    html.encoding = 'gb2312'
    html = html.text
    return html

def get_quote(data):
    idiom = urllib.parse.quote(data,encoding='gb2312')
    return idiom

def check_chengyu(q):
    url='http://chengyu.t086.com/chaxun.php?q={}&t=ChengYu'.format(get_quote(q))
    datas= etree.HTML(get_html(url)).xpath('//tr/td/a/font/text()')
    if len(datas)>0:
        return True
    else:
        return False

def get_chengyu_random(q):
    url='http://chengyu.t086.com/chaxun.php?q1={}&q2=&q3=&q4='.format(get_quote(q))
    datas= etree.HTML(get_html(url)).xpath('//tr/td/a/text()')
    if len(datas) ==1:
        answer = q+ datas[0]
        return answer
    elif len(datas)>1:
        answer = q+ datas[random.randint(0,len(datas)-1)]
        return answer
    else:
        return False

MODE = str(input('Choose MODE(1 for 人工接龙, 2 for 机器接龙): '))
while True:
    try:
        if MODE == '1':
            enter = str(input('请输入一个成语开始：'))
            if check_chengyu(enter):
                while enter != 'exit':
                    answer = get_chengyu_random(enter[-1])
                    if answer is False:
                        cprint('【失败】机器接龙接接不下去了，接龙结束！','红色')
                        MODE = 0
                        break
                    else:
                        cprint('机器回复（随机策略）：%s'%answer,'黄色')
                        enter = str(input('您的回复：'))
                        if check_chengyu(enter) is False:
                            cprint('【失败】您输入的不是一个成语，接龙结束！','红色')
                            MODE = 0
                            break                            
            else:
                cprint('【失败】您输入的不是一个成语，请重新输入！','红色')
                
            MODE = 0
        if MODE == '2':
            enter = input('请输入一个成语开始：')
            if check_chengyu(enter):
                for i in range(100):
                    answer = get_chengyu_random(enter[-1])
                    if answer is False:
                        cprint('【失败】随机策略机器接龙接不下去了，接龙结束！','红色')
                        MODE = 0
                        break
                    else:
                        cprint('机器回复（随机策略）：%s'%answer,'黄色')
                        enter = answer
            else:
                cprint('【失败】您输入的不是一个成语，请重新输入！','红色')

            print('（*****最多展示前100回接龙。*****）')
            MODE = 0
    finally:
        if MODE not in ['1','2']:
            MODE = str(input('Choose MODE(1 for 人工接龙, 2 for 机器接龙): '))
