import time

# 日志打印
def log(*args):
    t = time.time()
    tt = formattime(t)
    the_time = []
    for tts in tt:
        the_time.append(tts)
    time_str = ''.join(the_time)
    the_args = []
    for arg in args:
        the_args.append(str(arg))
    args_str = ''.join(the_args)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(time_str + ' ' + args_str + '\r\n')
    print(tt, *args)

# 时间格式化打印
def formattime(timestamp):
    tf = '%Y/%m/%d %H:%M:%S'
    ft = time.strftime(tf, time.localtime(timestamp))
    return ft

