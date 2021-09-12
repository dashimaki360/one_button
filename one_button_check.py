# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time
import datetime

file_name = "/home/pi/one_button/one_button_log.txt"

def tail(f, window=1):
    """
    Returns the last `window` lines of file `f` as a list of bytes.
    """
    if window == 0:
        return b''
    BUFSIZE = 1024
    f.seek(0, 2)
    end = f.tell()
    nlines = window + 1
    data = []
    while nlines > 0 and end > 0:
        i = max(0, end - BUFSIZE)
        nread = min(end, BUFSIZE)

        f.seek(i)
        chunk = f.read(nread)
        data.append(chunk)
        nlines -= chunk.count(b'\n')
        end -= nread
    return b'\n'.join(b''.join(reversed(data)).splitlines()[-window:])

def is_forget():
    last_log_str = ""
    with open(file_name, 'rb') as f:
        last_log_str = tail(f, 1).decode('utf-8')
        print("last_log_str: {}".format(last_log_str) )
    last_log = datetime.datetime.strptime(last_log_str,'%Y-%m-%d %H:%M:%S')
    diff = datetime.datetime.now() - last_log
    print("diff: {}".format(diff))
    if diff > datetime.timedelta(hours=13):
        print("TRUE")
        return True
    else:
        print("FALSE")
        return False

def main():
    led_red_pin = 27 # 13番端子

    # GPIO初期化
    wiringpi.wiringPiSetupGpio()
    # GPIOを出力モード（1）に設定
    wiringpi.pinMode( led_red_pin, 1 )
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    wiringpi.pullUpDnControl( led_red_pin, 1 )

    while True:
        
        # check button log
        if is_forget():
            wiringpi.digitalWrite(led_red_pin, 1)
            sleep_time = 5
        else:
            wiringpi.digitalWrite(led_red_pin, 0)
            sleep_time = 600
        time.sleep(sleep_time)
    
if __name__ == "__main__":
    main()






