import sensor, image, time, math, lcd, os
from pyb import UART
from pyb import Pin
from pyb import Timer


def mirobot_finish_moving():
    inByte = ''
    print('start')
    while inByte != '<':
       if uart.any() > 0:
            temp = uart.read(1)
            #print(temp)
            inByte = temp.decode('gbk')
            #inByte = uart.readline().decode('gbk')
            #print(inByte)
    print('okay')
 
#或者 
'''def mirobot_finish_moving():
    inByte = ''
    print('start')
    while inByte.find('<')<0:
       if uart.any() > 0:
            time.sleep(500)
            inByte = uart.readline().decode('gbk')
            print(inByte)
    print('okay')'''

value = './dfg.txt'

high_z = 50
bx = 160
by = 120
cy = 0
cx = 0

# Set up the serial port
uart = UART(3, 115200)

#Set color threshold
w_threshold = (63, 100, -128, 127, -128, 127)
thresholds = [(0, 100, 25, 127, -128, 127),    #red
              (0, 100, -128, -18, 11, 127),    #green
              (1, 100, -128, 127, -128, -20)]  #blue
              #(42, 67, -9, 15, 19, 127)

# Set the pwm output of led
tim = Timer(4, freq=1000)           #Hertz frequency
Led = tim.channel(3, Timer.PWM, pin=Pin("P9"), pulse_width_percent=10)

lcd.init()

# Set button
Key = Pin('P6', Pin.IN, Pin.PULL_UP)
keyvalue = Key.value() # Get key value

#Send reset command
#uart.write("$40 = 1\n")
uart.write("$H\n")
mirobot_finish_moving()
#time.sleep(5000)

# 摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
img = sensor.snapshot()
clock = time.clock()

#等待机械臂返回数据
'''while 1:
    if uart.any():
        time.sleep(5000)
        a = uart.readline().decode()
        print(a)
        break
print("ok\n")'''

#机械臂初始化指令
uart.write("M20 G90 G01 F5000\n")
uart.write("M3S0\n")
#mirobot_finish_moving()
#print('ok')

#标定
if keyvalue==0:

    uart.write('X220Y0'+'z'+str(high_z)+'\n') #下降到预备位置
    #mirobot_finish_moving()
    #time.sleep(3000)
    img.draw_string(10,110, "put,and key") #提示放物块
    img = sensor.snapshot()
    lcd.display(img) # lcd显示
    keytime = 0
    while 1:
        while Key.value()==0:
            keytime+=1
            time.sleep(1)
        if keytime > 8000:
            print('rst')
            #重启
            break
        elif keytime > 1000:
            #校准相对位置
            while 1:
                find=0
                img = sensor.snapshot()
                for blob in img.find_blobs(thresholds, x_stride=5, y_stride=5,pixels_threshold=50):
                    if blob.code() == 1:
                        img.draw_string(blob.x(), blob.y() + 10, 'R')
                        img.draw_cross(blob.cx(), blob.cy())
                        img.draw_rectangle(blob.rect())
                        bx=blob.cx()
                        by=blob.cy()
                        print('颜色坐标：',blob.cx(), blob.cy())
                        img = sensor.snapshot()
                        find=1
                        break

                if find == 1:
                    break
            #记录
            f = open(value,'w')
            f.write(str(high_z)+'\n')
            f.write(str(bx)+'\n')
            f.write(str(by)+'\n')
            print('变量写入...')
            print('初始高度：',high_z)
            print('x相对坐标：',bx)
            print('y相对坐标：',by)
            f.close()
            break
        elif keytime > 10:
            #下降一格
            high_z-=1
            uart.write('z'+str(high_z)+'\n') #下降到预备位置
            if high_z < -10:
                print('error\n')
                break
        keytime = 0

# 读取变量数据
try:
    f = open(value,'r')
    high_z = int(f.readline())
    bx = int(f.readline())
    by = int(f.readline())
    print('变量读出...')
    print('初始高度：',high_z)
    print('x相对坐标：',bx)
    print('y相对坐标：',by)
except:
    f = open(value,'w')
    f.write(str(high_z)+'\n')
    f.write(str(bx)+'\n')
    f.write(str(by)+'\n')
    print('变量写入...')
    print('初始高度：',high_z)
    print('x相对坐标：',bx)
    print('y相对坐标：',by)
    f.close()
else:
    f.close()

#uart.write("Z50\n")
uart.write("X100Y-100Z100\n")
#time.sleep(5000)
mirobot_finish_moving()

while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img) # lcd显示

    if uart.any():
        a = uart.readline().decode()

    for blob in img.find_blobs(thresholds, x_stride=5, y_stride=5,pixels_threshold=50):
        color = 'w'
        if blob.code() == 1:
            color = 'R'
            img.draw_string(blob.x(), blob.y() + 10, 'R')
        elif blob.code() == 2:
            color = 'G'
            img.draw_string(blob.x(), blob.y() + 10, 'G')
        elif blob.code() == 4:
            color = 'B'
            img.draw_string(blob.x(), blob.y() + 10, 'B')

        if blob.code():
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_rectangle(blob.rect())
            print('中心坐标：',bx, by)
            print('颜色坐标：',blob.cx(), blob.cy())
            y = 0+(blob.cx()-bx+cy) #准备计算
            x = 220+(blob.cy()-by+cx)
            print('相对坐标：',x, y)
            img = sensor.snapshot()
            lcd.display(img) # lcd显示
            if x>270 or x<150:
                break
            elif y>100 or y<-100:
                break

            #if idle==0:
            output_str="x%d y%d" % (x, y)
            uart.write(output_str+'\n') # 移动到上方
            uart.write("M3S1000\n") # 开启气泵
            print('输出坐标：'+output_str+'\n\n')
            uart.write('Z'+str(high_z)+'\n') # 下降
            uart.write('G4P0.1') # 开启气泵
            uart.write("Z100\n") # 提升
            uart.write("X100Y-100\n")
            if color == 'R':
                uart.write("X70Y-200\n")
                mirobot_finish_moving()
            elif color == 'G':
                uart.write("X30Y-200\n")
                mirobot_finish_moving()
            elif color == 'B':
                uart.write("X-30Y-200\n")
                mirobot_finish_moving()
            uart.write("M3S0\n") # 关气泵
            #time.sleep(12000)
            mirobot_finish_moving()
            break
