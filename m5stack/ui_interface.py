from m5stack import lcd
import time

BG      = 0x000000
DARK    = 0x050510
BAR     = 0x1a1a2e
TEAL    = 0x1D9E75
TEAL_LT = 0x5DCAA5
PURPLE  = 0x534AB7
GREY    = 0x888780
WHITE   = 0xFFFFFF
RED     = 0xFF4444
ORANGE      = 0xEF9F27  
ORANGE_DARK = 0xBA7517  
BEIGE       = 0xF5C4B3 
BLACK       = 0x000000

# Drawings functions 
def draw_turtle(x, y):
    lcd.fillCircle(x, y, 12, TEAL)
    lcd.fillCircle(x-5, y, 10, TEAL)
    lcd.fillCircle(x+5, y, 10, TEAL)
    lcd.fillCircle(x, y-4, 10, TEAL)
    lcd.fillCircle(x, y+4, 10, TEAL)
    lcd.fillCircle(x, y, 7, DARK)
    lcd.fillCircle(x, y-4, 2, TEAL)
    lcd.fillCircle(x, y+4, 2, TEAL)
    lcd.fillCircle(x-4, y, 2, TEAL)
    lcd.fillCircle(x+4, y, 2, TEAL)
    lcd.fillCircle(x, y-15, 5, TEAL)
    lcd.fillCircle(x-2, y-16, 1, DARK)  
    lcd.fillCircle(x+2, y-16, 1, DARK) 
    lcd.fillCircle(x-13, y-7, 4, TEAL) 
    lcd.fillCircle(x+13, y-7, 4, TEAL) 
    lcd.fillCircle(x-13, y+7, 4, TEAL)  
    lcd.fillCircle(x+13, y+7, 4, TEAL)  
    lcd.fillCircle(x, y+16, 3, TEAL)
    
def draw_bunny(x, y):
    lcd.fillCircle(x, 136, 8, TEAL)
    lcd.fillCircle(x, 126, 5, TEAL)
    lcd.fillRect(x-6, y-12, 4, 12, TEAL)
    lcd.fillRect(x+2, y-12, 4, 12, TEAL)

def draw_lion(x, y):
    lcd.fillCircle(x,    y,    13, ORANGE_DARK)
    lcd.fillCircle(x-10, y-7,   6, ORANGE_DARK)
    lcd.fillCircle(x+10, y-7,   6, ORANGE_DARK)
    lcd.fillCircle(x-13, y+1,   5, ORANGE_DARK)
    lcd.fillCircle(x+13, y+1,   5, ORANGE_DARK)
    lcd.fillCircle(x-10, y+10,  5, ORANGE_DARK)
    lcd.fillCircle(x+10, y+10,  5, ORANGE_DARK)
    lcd.fillCircle(x,    y+13,  5, ORANGE_DARK)
    
    lcd.fillCircle(x, y, 10, ORANGE)
    
    lcd.fillCircle(x-8, y-8, 4, ORANGE)
    lcd.fillCircle(x+8, y-8, 4, ORANGE)
    lcd.fillCircle(x-8, y-8, 2, ORANGE_DARK)
    lcd.fillCircle(x+8, y-8, 2, ORANGE_DARK)
    
    lcd.fillCircle(x-3, y-2, 2, BLACK)
    lcd.fillCircle(x+3, y-2, 2, BLACK)
    lcd.fillCircle(x-4, y-3, 1, WHITE)
    lcd.fillCircle(x+2, y-3, 1, WHITE)
    
    lcd.fillCircle(x, y+4, 4, BEIGE)
    lcd.fillCircle(x, y+2, 1, BLACK)

    lcd.fillCircle(x-6, y+4, 1, BLACK)
    lcd.fillCircle(x-9, y+3, 1, BLACK)
    lcd.fillCircle(x+6, y+4, 1, BLACK)
    lcd.fillCircle(x+9, y+3, 1, BLACK)

def draw_speed_icon(speed):
    lcd.fillRect(0, 118, 320, 32, DARK)
    lcd.font(lcd.FONT_DefaultSmall)
    
    if speed < 15:
        draw_turtle(20 ,134)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "TORTOISE")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "< 15 km/h")
    elif speed < 25:
        draw_bunny(20, 134)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "BUNNY")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "15-25 km/h")
    else:
        draw_lion(20, 134)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "LION")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "> 25 km/h")

def init_screen():
    lcd.clear()
    lcd.fillScreen(BG)
    
    lcd.fillRect(0, 0, 320, 28, BAR)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(PURPLE, BAR)
    lcd.text(8, 6, "SPEED TRACKER")
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(WHITE, TEAL)
    lcd.fillRect(0, 28, 320, 2, PURPLE)
    
    lcd.fillRect(0, 222, 320, 18, BAR) 
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.setTextColor(WHITE, BAR)
    lcd.text(15, 226, "START/PAUSE") 
    lcd.text(275, 226, "STOP")

def update_display(speed, lat, lon, has_fix, wifi_ok=False, session_state="STOPPED"):
    gps_col  = TEAL_LT if has_fix else RED
    wifi_col = TEAL_LT if wifi_ok else RED

    lcd.fillRect(200, 2, 120, 24, BAR) 
    lcd.font(lcd.FONT_DejaVu18)
    if session_state == "RUNNING":
        lcd.setTextColor(RED, BAR)
        lcd.text(260, 6, "REC")
    elif session_state == "PAUSED":
        lcd.setTextColor(ORANGE, BAR)
        lcd.text(240, 6, "PAUSE")
    else:
        lcd.setTextColor(GREY, BAR) 
        lcd.text(250, 6, "STOP")

    lcd.fillRect(0, 32, 320, 18, DARK)
    lcd.font(lcd.FONT_Default)

    lcd.setTextColor(gps_col, DARK)
    lcd.text(6, 36, "GPS: LOCKED" if has_fix else "GPS: SEARCHING")

    lcd.setTextColor(wifi_col, DARK)
    lcd.text(200, 36, "Wifi: OK" if wifi_ok else "Wifi: NO Conn")
    
    lcd.fillRect(0, 52, 320, 100, DARK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.setTextColor(GREY, DARK)
    lcd.text(126, 56, "SPEED")
    lcd.font(lcd.FONT_DejaVu56)
    lcd.setTextColor(WHITE, DARK)
    lcd.text(55, 65, "{:.1f}".format(speed))
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(GREY, DARK)
    lcd.text(238, 90, "km/h")
    
    draw_speed_icon(speed)
    
    lcd.fillRect(0, 155, 320, 1, BAR)
    lcd.fillRect(0, 156, 320, 50, DARK)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(GREY, DARK)
    lcd.text(12, 160, "LAT")
    lcd.text(118, 160, "LON")
    
    lcd.setTextColor(TEAL_LT, DARK)
    lcd.text(6, 177, "{:.4f}".format(lat) if has_fix else "---")
    lcd.text(112, 177, "{:.4f}".format(lon) if has_fix else "---")
  
    lcd.fillRect(0, 207, 320, 1, BAR)
    lcd.fillRect(0, 208, 320, 14, BAR)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.setTextColor(GREY, BAR)
    h, m, s = time.localtime()[3:6]
    lcd.text(6, 211, "{:02d}:{:02d}:{:02d}".format(h, m, s))

def show_boot_screen():
    lcd.clear()
    lcd.fillScreen(BG)
    lcd.font(lcd.FONT_DejaVu24)
    lcd.setTextColor(PURPLE, BG)
    lcd.text(50, 70, "BIKE TRACKER")
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(TEAL, BG)
    lcd.text(90, 110, "Starting...")
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(GREY, BG)
    lcd.text(60, 145, "UNIL - CAA Project")
    
def show_config_prompt():
    lcd.clear()
    lcd.fillScreen(BG)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(WHITE, BG)
    lcd.text(40, 60, "CONFIGURE WI-FI?")
    
    lcd.fillRect(20, 110, 280, 50, PURPLE)
    lcd.setTextColor(WHITE, PURPLE)
    
    lcd.text(35, 125, "Touch screen to change")
    
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.setTextColor(GREY, BG)
    lcd.text(25, 190, "No action: Auto-connect in 5s...")

def show_connecting_screen(ssid):
    """ Écran de transition pendant la tentative de connexion """
    lcd.clear()
    lcd.fillScreen(BG)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(TEAL_LT, BG)
    lcd.text(40, 90, "Connecting to Wi-Fi...")
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(WHITE, BG)
    lcd.text(40, 130, "SSID: {}".format(ssid))

def show_wifi_menu(networks):
    lcd.clear()
    lcd.fillScreen(BG)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(PURPLE, BG)
    lcd.text(10, 15, "AVAILABLE NETWORKS:")
    lcd.fillRect(0, 40, 320, 2, PURPLE)
    
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(WHITE, BG)
    
    y = 60
    for ssid in networks[:5]:
        lcd.text(20, y, "- {}".format(ssid))
        y += 30
        
    lcd.fillRect(40, 200, 240, 35, TEAL)
    lcd.setTextColor(WHITE, TEAL)
    lcd.text(55, 212, "Connecting to iPhone...")
