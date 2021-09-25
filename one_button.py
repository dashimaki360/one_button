import time
import datetime

import wiringpi

import one_button_common


def gpio_init():
    # GPIO初期化
    wiringpi.wiringPiSetupGpio()
    # GPIOを出力モード（1）に設定
    wiringpi.pinMode(one_button_common.button_pin, 0)
    wiringpi.pinMode(one_button_common.led_green_pin, 1)
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    wiringpi.pullUpDnControl(one_button_common.button_pin, 2)
    wiringpi.pullUpDnControl(one_button_common.led_green_pin, 1)


def main():
    gpio_init()

    while True:
        # GPIO端子の状態を読み込む
        # ボタンを押すと「0」、放すと「1」になる
        # GPIOの状態が0V(0)であるか比較
        if(wiringpi.digitalRead(one_button_common.button_pin) == 0):
            wiringpi.digitalWrite(one_button_common.led_green_pin, 1)
            timestamp = datetime.datetime.strftime(datetime.datetime.now(),
                                                   '%Y-%m-%d %H:%M:%S')
            print(timestamp)
            with open(one_button_common.log_file_name, 'a') as f:
                print(timestamp, file=f)
            time.sleep(2)  # sleep 2sec to avoid double count
        wiringpi.digitalWrite(one_button_common.led_green_pin, 0)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
