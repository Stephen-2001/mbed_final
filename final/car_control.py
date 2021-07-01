import time
import serial
import sys,tty,termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
    # d1 = 0
    # d2 = 0
    # check1 = 1
    # check2 = 0

    # while(check1):
    #     k = inkey()
    #     if k == ' ':
    #         check1 = 0
    #         check2 = 1 
    #         break
    #     digit = int(k)
    #     d1 = 10 * d1 + digit
    # while(check2):
    #     k = inkey()
    #     if k == ' ':
    #         check2 = 0
    #         break
    #     digit = int(k)
    #     d2 = 10 * d2 + digit
    k = input()
    d1 = int(k)
    k = input()
    d2 = int(k)
    k = input()
    if k == 'east':
        print(d1)
        print(d2)
        print('back_first_time')
        s.write("/goStraight/run -100 \n".encode())
        
        time.sleep(d1/15)
        print('turn')
        s.write("/turn/run 100 0.01 \n".encode())
        
        time.sleep(1.2)
        print('back_second_time')
        s.write("/goStraight/run -100 \n".encode())
        d2 = d2 + 7
        time.sleep(d2/15)
        s.write("/stop/run \n".encode())
    elif k == 'west':
        print(d1)
        print(d2)
        print('back_first_time')
        s.write("/goStraight/run -100 \n".encode())
        time.sleep(d1/15)
        print('turn')
        s.write("/turn/run 100 -0.01 \n".encode())
        time.sleep(1.2)
        print('back_second_time')
        s.write("/goStraight/run -100 \n".encode())
        d2 = d2 + 7
        time.sleep(d2/15)
        s.write("/stop/run \n".encode())
    else:
        print ("not an arrow key!")

    return 1

if len(sys.argv) < 1:
    print ("No port input")
s = serial.Serial(sys.argv[1])
while get():
    i = 0