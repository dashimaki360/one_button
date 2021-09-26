import time
import datetime
import threading

import wiringpi

import one_button_common

led_state = "done"


def calc_state(now_datetime, last_log_datetime):
    # AM
    margin = datetime.timedelta(hours=4)
    if 18 > now_datetime.hour >= 6:
        fast = datetime.datetime(now_datetime.year,
                                 now_datetime.month,
                                 now_datetime.day,
                                 6, 0, 0, 0,)
    # PM
    elif now_datetime.hour >= 18:
        fast = datetime.datetime(now_datetime.year,
                                 now_datetime.month,
                                 now_datetime.day,
                                 18, 0, 0, 0,)
    else:
        fast = datetime.datetime(now_datetime.year,
                                 now_datetime.month,
                                 now_datetime.day - 1,
                                 18, 0, 0, 0,)

    late = fast + margin
    if last_log_datetime > fast:
        return "done"
    if now_datetime > late:
        return "forget"
    else:
        return "yet"


def get_last_log_datetime():
    last_log_str = ""
    with open(one_button_common.log_file_name, 'rb') as f:
        last_log_str = one_button_common.tail(f, 1).decode('utf-8')
        print("last_log_str: {}".format(last_log_str))

    try:
        last_log = datetime.datetime.strptime(last_log_str, '%Y-%m-%d %H:%M:%S')
    except:
        return -1
    return last_log


def led_control_thread():
    global led_state
    led_state = "done"
    flip = 0
    while True:
        if led_state == "done":
            wiringpi.digitalWrite(one_button_common.led_red_pin, 0)
        elif led_state == "forget":
            wiringpi.digitalWrite(one_button_common.led_red_pin, flip)
            flip = (flip + 1) % 2
        elif led_state == "yet":
            wiringpi.digitalWrite(one_button_common.led_red_pin, 1)
        time.sleep(1)


def gpio_init():
    # GPIO初期化
    wiringpi.wiringPiSetupGpio()
    # GPIOを出力モード（1）に設定
    wiringpi.pinMode(one_button_common.led_red_pin, 1)
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    wiringpi.pullUpDnControl(one_button_common.led_red_pin, 1)


def main():
    global led_state
    gpio_init()

    th1 = threading.Thread(target=led_control_thread)
    th1.start()

    while True:
        # check button log
        state = calc_state(datetime.datetime.now(), get_last_log_datetime())
        print(state)
        if state == "done":
            led_state = "done"
            sleep_time = 5
        elif state == "forget":
            led_state = "forget"
            sleep_time = 5
        elif state == "yet":
            led_state = "yet"
            sleep_time = 5
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
