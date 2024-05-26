# PicoW Unicorn Clock
# Nick Stevens Sept 2023

#Import Libraries
import network
import socket
import time
import struct

from picounicorn import PicoUnicorn
from machine import Pin

picounicorn = PicoUnicorn()

#setup NTP
NTP_DELTA = 2208988800 + 14400  # subtract 1 hour = 3600 seconds to get GMT + 1
host = "pool.ntp.org"

#WIFI Variables
ssid = 'g6'
password = '12345678'

#colours and number definitions

numbers3x6 = [
    2,5,5,5,5,2, # Zero
    2,6,2,2,2,7, # one
    2,5,1,2,4,7, # two
    7,1,2,1,1,6, # three
    5,5,5,7,1,1, # four
    7,4,6,1,1,6, # five
    2,4,6,5,5,2, # six
    7,1,2,2,4,4, # seven
    2,5,2,5,5,2, # eight
    2,5,5,3,1,2  # nine
]

numbers = numbers3x6
fontheight = 6

white =    [255,255,255]
red =      [255,0,0]
orange =   [255,128,0]
green =    [0,255,0]
blue =     [0,0,255]
yellow =   [255,255,0]
cyan =     [0,255,255]
magenta =  [255,0,255]
pink =     [255,128,128]
cyan2 =    [128,255,255]
green2 =   [128,255,128]
purple =   [128,128,255]
lime =     [128,255,0]
mint =     [0,255,128]
blue3 =    [0,128,255]

dwhite =   [128,128,128]
dred =     [128,0,0]
dorange =  [128,64,0]
dgreen =   [0,128,0]
dblue =    [0,0,128]
dyellow =  [128,128,0]
dcyan =    [0,128,128]
dmagenta = [128,0,128]
dpink =    [128,64,64]
dcyan2 =   [64,128,128]
dgreen2 =  [64,128,64]
dpurple =  [64,64,128]
dlime =    [64,128,0]
dmint =    [0,128,64]
dblue3 =   [0,64,128]

colours1 = [white,red,orange,green,blue,yellow,cyan,magenta,pink,cyan2,green2,purple,lime,mint,blue3]
colours2 = [dwhite,dred,dorange,dgreen,dblue,dyellow,dcyan,dmagenta,dpink,dcyan2,dgreen2,dpurple,dlime,dmint,dblue3]
colours = colours1
colour_sel1 = 1
colour_sel2 = 1
colour_sel3 = 1
colour_sel4 = 1
tick_col = 2

#digit colours
current_col1 = colours[colour_sel1] 
current_col2 = colours[colour_sel2]
current_col3 = colours[colour_sel3]
current_col4 = colours[colour_sel4]
current_tick = colours[tick_col]

#startup light
picounicorn.set_pixel(0, 0, 255, 0, 0)

#plagerised from "picow_ntp_client.py" by aallan
def set_time():
    picounicorn.set_pixel(0, 0, 255, 128, 0) #set pixel to orange while getting time
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except OSError as exc:
        if exc.args[0] == 110: # ETIMEOUT
            time.sleep(2)
            pass
    finally:
        s.close()
    
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    picounicorn.set_pixel(0, 0, 0, 0, 0)

#display the number in a position and colour
def display_number(xp, yp, c, number):
    for x in range(3):
        for y in range(fontheight):
            binary = "{:03b}".format(numbers[(number * fontheight) + y])
            if binary[x] == "1":
                picounicorn.set_pixel(xp+x,yp+y,c[0],c[1],c[2])
            else:
                picounicorn.set_pixel(xp+x,yp+y,0,0,0)
            
#connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
    
max_wait = 20
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    picounicorn.set_pixel(0, 0, 0, 255, 0)
    time.sleep(.5)
    picounicorn.set_pixel(0, 0, 0, 0, 0)
    time.sleep(.5)

if wlan.status() != 3:
    picounicorn.set_pixel(0, 0, 255, 0, 0)
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

#set the time from NTP
set_time()
print(time.localtime())
#startup light off
picounicorn.set_pixel(0, 0, 0, 0, 0)
#setup the unicorn display
w = picounicorn.get_width()
h = picounicorn.get_height()

#button not pressed
butt = ""

#main loop
while True:

    nowtime= time.localtime()
    Tyear, Tmonth, Tday, Thour, Tmin, Tsec, Tweekday, Tyearday = (nowtime)
    Ftime = "{:02d}"
    time_hour = Ftime.format(Thour)
    time_mins = Ftime.format(Tmin)
    time_secs = Ftime.format(Tsec)
    
    time_hour1 = int(time_hour[0])
    time_hour2 = int(time_hour[1])
    time_mins1 = int(time_mins[0])
    time_mins2 = int(time_mins[1])
     
    display_number(0,0,current_col1,time_hour1) #hour digit 1
    display_number(4,0,current_col2,time_hour2) #hour digit 2
    
    display_number(9,0,current_col3,time_mins1) # min digit 1
    display_number(13,0,current_col4,time_mins2) # min digit 2
    
    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        #cycle thu hour digit colours
        butt="A"
        print(butt)
        colour_sel1 = (colour_sel1 + 1) % 15
        colour_sel2 = (colour_sel2 + 1) % 15
        time.sleep(.3)
        
    if picounicorn.is_pressed(picounicorn.BUTTON_B):
        #cycle thu tick colours
        butt="B"
        print(butt)
        tick_col = (tick_col + 1) % 15
        time.sleep(.3)
        
    if picounicorn.is_pressed(picounicorn.BUTTON_X):
        #cycle thu min digit colours
        butt="X"
        print(butt)
        colour_sel3 = (colour_sel3 + 1) % 15
        colour_sel4 = (colour_sel4 + 1) % 15
        time.sleep(.3)
        
    if picounicorn.is_pressed(picounicorn.BUTTON_Y):
        #dark or light
        butt="Y"
        print(butt)
        if colours == colours1:
            colours = colours2
        else:
            colours = colours1 
        time.sleep(.3)
        
    butt = ""
    time.sleep(.1)
    
    #update digit colours
    current_col1 = colours[colour_sel1] 
    current_col2 = colours[colour_sel2]
    current_col3 = colours[colour_sel3]
    current_col4 = colours[colour_sel4]
    current_tick = colours[tick_col]
    
    #seconds is even
    if int(time_secs) % 2 == 0:
        #seconds tick pattern on
        picounicorn.set_pixel(7,6,current_tick[0],current_tick[1], current_tick[2])
        picounicorn.set_pixel(8,6,current_tick[0],current_tick[1], current_tick[2])
        
    #seconds is odd
    else:
        #seconds tick pattern off
        picounicorn.set_pixel(7,6,0,0,0)
        picounicorn.set_pixel(8,6,0,0,0)

