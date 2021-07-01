import pyb, sensor, image, time, math
THRESHOLD = (0, 100)
BINARY_VISIBLE = True
enable_lens_corr = False
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time = 2000)
clock = time.clock()

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
check = 0
while(True):
   if (check > 20): break
   clock.tick()
   img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()
   line = img.get_regression([(255, 255) if BINARY_VISIBLE else THRESHOLD], robust=True)
   if (line):
      img.draw_line(line.line(), color=127)
      # info = (line.x1(), line.y1(), line.x2(), line.y2(), line.length(), line.theta(), line.rho())
      print(line)
      theta = line.theta()
      rho = line.rho()

      if (rho < 0):
         theta = 180 - theta
      magnitude = abs(rho) / math.cos(math.radians(theta))
      diff = magnitude - 40  # the spatial differenence between middle and present position
      if (abs(diff) <= 15 and theta < 30):
         print("gostraight")
         uart.write(("/goStraight/run 40 \n").encode())
      elif (abs(diff) >= 15 and diff < 0 and theta > 45):
         print("turn_left")
         uart.write(("/turn/run 40 0.75\n").encode())
      elif (abs(diff) >= 15 and diff > 0 and theta > 45):
         print("turn_right")
         uart.write(("/turn/run 40 -0.75\n").encode())
      #elif (abs(diff) <= 30):
         #print("gostraight")
         #uart.write(("/goStraight/run 40 \n").encode())
      elif (diff < 0):
         print("turn_left")
         uart.write(("/turn/run 40 0.75\n").encode())
      elif (diff > 0):
         print("turn_right")
         uart.write(("/turn/run 40 -0.75\n").encode())
      else:
         print("stop")
         check += 1
         uart.write(("/stop/run \n").encode())
      time.sleep_ms(100)
      print("diff = %d theta = %d \n" % (diff, theta))
   else:
      print("stop")
      check += 1
      uart.write(("/stop/run \n").encode())
      time.sleep_ms(100)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
   return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

flag = 1
while(flag):
   clock.tick()
   img = sensor.snapshot()
   for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
      #img.draw_rectangle(tag.rect(), color = (255, 0, 0))
      #img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
      print(tag)
      if ((degrees(tag.y_rotation()) > 0 and degrees(tag.y_rotation())<3) or (degrees(tag.y_rotation()) > 357 and degrees(tag.y_rotation())<360)):
         print("stop2")
         uart.write(("/stop/run \n").encode())
         flag = 0
         break
      if degrees(tag.y_rotation()) > 3 and degrees(tag.y_rotation()) < 90:
         print("turn_left")
         print("%d" % degrees(tag.y_rotation()))
         uart.write(("/turn/run 30 0.5\n").encode())
         time.sleep(1)
      elif degrees(tag.y_rotation()) < 357 and degrees(tag.y_rotation()) > 270 :
         print("turn _right")
         print("%d" % degrees(tag.y_rotation()))
         uart.write(("/turn/run 30 -0.5\n").encode())
         time.sleep(1)
      else:
         print("go_Straight")
         uart.write(("/goStraight/run 30 \n").encode())

uart.write(("/pingcheck/run \n").encode())
      ## The conversion is nearly 6.2cm to 1 -> translation
      ##print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            ##degrees(tag.x_rotation()), degrees(tag.y_rotation()))
      ##print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
      ### Translation units are unknown. Rotation units are in degrees.
      ##uart.write(("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args).encode())
   ##uart.write(("FPS %f\r\n" % clock.fps()).encode())
uart.write(("finish\n").encode())
