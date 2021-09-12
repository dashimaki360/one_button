# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time
import datetime

file_name = "/home/pi/one_button/one_button_log.txt"

def main():
    # ボタンを繋いだGPIOの端子番号
    button_pin = 17 # 11番端子
    # led_red_pin = 27 # 13番端子
    led_green_pin = 22 # 15番端子


    # GPIO初期化
    wiringpi.wiringPiSetupGpio()
    # GPIOを出力モード（1）に設定
    wiringpi.pinMode( button_pin, 0 )
    wiringpi.pinMode( led_green_pin, 1 )
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    wiringpi.pullUpDnControl( button_pin, 2 )
    wiringpi.pullUpDnControl( led_green_pin, 1 )



    while True:
        # GPIO端子の状態を読み込む
        # ボタンを押すと「0」、放すと「1」になる
        # GPIOの状態が0V(0)であるか比較
        if( wiringpi.digitalRead(button_pin) == 0 ):
    #         print ("Switch ON")
            wiringpi.digitalWrite(led_green_pin, 1)
            timestamp = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
            print(timestamp)
            with open(file_name, 'a') as f:
                print(timestamp, file=f)
            time.sleep(2) #sleep 5sec to avoid double count
            
        wiringpi.digitalWrite(led_green_pin, 0)
        time.sleep(0.2)
    
if __name__ == "__main__":
    main()
