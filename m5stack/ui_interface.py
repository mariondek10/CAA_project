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

def draw_speed_icon(speed):
    # Efface la zone icone
    lcd.fillRect(0, 118, 320, 32, DARK)
    lcd.font(lcd.FONT_DefaultSmall)
    
    if speed < 15:
        # Tortue — cercle avec 4 pattes
        lcd.fillCircle(20, 134, 10, TEAL)
        lcd.fillCircle(20, 134, 6, DARK)
        lcd.fillCircle(20, 128, 5, TEAL)
        lcd.fillRect(10, 138, 4, 6, TEAL)
        lcd.fillRect(16, 138, 4, 6, TEAL)
        lcd.fillRect(22, 138, 4, 6, TEAL)
        lcd.fillRect(28, 138, 4, 6, TEAL)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "TORTUE")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "< 15 km/h")

    elif speed < 40:
        # Lapin — corps ovale + oreilles
        lcd.fillCircle(20, 136, 8, TEAL)
        lcd.fillCircle(20, 126, 5, TEAL)
        lcd.fillRect(14, 112, 4, 12, TEAL)
        lcd.fillRect(22, 112, 4, 12, TEAL)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "LAPIN")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "15-40 km/h")

    else:
        # Cheetah
        lcd.fillTriangle(6, 134, 20, 122, 20, 146, TEAL)
        lcd.fillTriangle(18, 134, 32, 122, 32, 146, TEAL_LT)
        lcd.fillRect(30, 132, 8, 4, WHITE)
        lcd.setTextColor(TEAL_LT, DARK)
        lcd.text(46, 128, "CHEETAH")
        lcd.setTextColor(GREY, DARK)
        lcd.text(46, 138, "> 40 km/h")

def init_screen():
    lcd.clear()
    lcd.fillScreen(BG)
    lcd.fillRect(0, 0, 320, 28, BAR)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(PURPLE, BAR)
    lcd.text(8, 6, "BIKE TRACKER")
    lcd.fillRect(252, 4, 64, 20, TEAL)
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(WHITE, TEAL)
    lcd.text(257, 9, "WiFi OK")
    lcd.fillRect(0, 28, 320, 2, PURPLE)

def update_display(speed, lat, lon, has_fix, lora_ok=False):
    status_col = TEAL_LT if has_fix else RED
    lcd.fillRect(0, 32, 320, 18, DARK)
    lcd.font(lcd.FONT_Default)
    lcd.setTextColor(status_col, DARK)
    lcd.text(6, 36, "GPS: LOCKED" if has_fix else "GPS: SEARCHING")
    if has_fix:
        lcd.setTextColor(GREY, DARK)
        lcd.text(130, 36, "{:.4f},{:.4f}".format(lat, lon))
    lcd.fillRect(0, 52, 320, 100, DARK)
    lcd.font(lcd.FONT_DefaultSmall)
    lcd.setTextColor(GREY, DARK)
    lcd.text(126, 56, "SPEED")
    lcd.font(lcd.FONT_DejaVu56)
    lcd.setTextColor(WHITE, DARK)
    lcd.text(55, 65, "{:.1f}".format(speed))
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(GREY, DARK)
    lcd.text(238, 108, "km/h")
    draw_speed_icon(speed)
    lcd.fillRect(0, 155, 320, 1, BAR)
    lcd.fillRect(0, 156, 320, 50, DARK)
    lcd.font(lcd.FONT_DejaVu18)
    lcd.setTextColor(GREY, DARK)
    lcd.text(12, 160, "LAT")
    lcd.text(118, 160, "LON")
    lcd.text(228, 160, "LoRa")
    lcd.setTextColor(TEAL_LT, DARK)
    lcd.text(6, 177, "{:.4f}".format(lat) if has_fix else "---")
    lcd.text(112, 177, "{:.4f}".format(lon) if has_fix else "---")
    if lora_ok:
        lcd.fillRect(220, 175, 64, 20, TEAL)
        lcd.setTextColor(WHITE, TEAL)
        lcd.text(226, 180, "TX OK")
    else:
        lcd.fillRect(220, 175, 64, 20, DARK)
        lcd.setTextColor(RED, DARK)
        lcd.text(226, 180, "NO TX")
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

show_boot_screen()
import time
time.sleep(2)
init_screen()
update_display(5.0, 46.5154, 6.6151, True, False)
