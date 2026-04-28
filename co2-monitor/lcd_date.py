# -*- coding: utf-8 -*-
#!/usr/bin/python3

from time import sleep
import datetime
import json
import smbus
import mh_z19
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# ===== MQTT設定 =====
MQTT_BROKER = "192.168.0.140"   # MQTTブローカー
MQTT_PORT = 1883
MQTT_TOPIC = "co2/data"
MQTT_CLIENT_ID = "co2-pi28"

# ===== LED =====
LED_Y = 23
LED_R = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_Y, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_R, GPIO.OUT, initial=GPIO.LOW)

# ===== LCD =====
I2C_ADDR = 0x3f
LCD_WIDTH = 16

LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)

# ===== MQTT接続 =====
def mqtt_connect():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("MQTT connected:", MQTT_BROKER)
    return client

def mqtt_publish(client, co2):
    payload = {
        "type": "co2",
        "co2": co2,
        "unit": "ppm",
        "source": "192.168.0.28",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    client.publish(MQTT_TOPIC, json.dumps(payload), qos=0)
    print("MQTT送信:", payload)

# ===== LCD処理 =====
def fit16(message):
    return str(message)[:LCD_WIDTH].ljust(LCD_WIDTH, " ")

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    sleep(0.01)

def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    sleep(E_DELAY)

def lcd_string(message, line):
    message = fit16(message)
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# ===== LED制御 =====
def set_leds(co2):
    GPIO.output(LED_Y, GPIO.LOW)
    GPIO.output(LED_R, GPIO.LOW)

    if isinstance(co2, int):
        if 1000 <= co2 < 1500:
            GPIO.output(LED_Y, GPIO.HIGH)
        elif co2 >= 1500:
            GPIO.output(LED_R, GPIO.HIGH)

# ===== メイン処理 =====
def main():
    lcd_init()
    mqtt_client = mqtt_connect()

    while True:
        try:
            local_time = datetime.datetime.now()
            data = mh_z19.read_all()
            co2 = data.get("co2", None)

            if co2 is None:
                co2_display = "---"
            else:
                co2_display = co2

            line1 = local_time.strftime("%m/%d %H:%M")
            line2 = f"CO2:{co2_display} ppm"

            lcd_string(line1, LCD_LINE_1)
            lcd_string(line2, LCD_LINE_2)

            set_leds(co2)

            # CO2値が取得できた時だけMQTT送信
            if isinstance(co2, int):
                try:
                    mqtt_publish(mqtt_client, co2)
                except Exception as e:
                    print("MQTT送信エラー:", e)
                    try:
                        mqtt_client = mqtt_connect()
                        mqtt_publish(mqtt_client, co2)
                    except Exception as e2:
                        print("MQTT再送失敗:", e2)

        except Exception as e:
            print("ERROR:", e)
            lcd_string("SENSOR ERROR", LCD_LINE_1)
            lcd_string("CHECK MH-Z19", LCD_LINE_2)
            GPIO.output(LED_Y, GPIO.LOW)
            GPIO.output(LED_R, GPIO.LOW)

        sleep(2)

try:
    print("Start:", datetime.datetime.now())
    main()

except KeyboardInterrupt:
    pass

finally:
    try:
        lcd_byte(0x01, LCD_CMD)
    except:
        pass
    GPIO.cleanup()
