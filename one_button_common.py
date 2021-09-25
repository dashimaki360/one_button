log_file_name = "/home/pi/one_button/one_button_log.txt"

# ボタンを繋いだGPIOの端子番号
button_pin = 11 # 23番端子
led_red_pin = 2 # 3番端子
led_green_pin = 4 # 7番端子

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
