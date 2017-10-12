import sys
import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        "Error importing RPi.GPIO!  " +
        "This is probably because you need superuser privileges.  " +
        "You can achieve this by using 'sudo' to run your script")


PIN_BANK1_COMMON = 9
PIN_BANK1_CHANNEL2 = 5
PIN_BANK1_CHANNEL1 = 7
PIN_BANK1_CLOSE = 11
PIN_BANK1_OPEN = 13

PIN_BANK2_COMMON = 39
PIN_BANK2_CHANNEL2 = 37
PIN_BANK2_CHANNEL1 = 35
PIN_BANK2_CLOSE = 33
PIN_BANK2_OPEN = 31

CMD_CHANNEL = {
    "1": [[PIN_BANK1_CHANNEL1, PIN_BANK1_CHANNEL2], [GPIO.HIGH, GPIO.HIGH]],
    "2": [[PIN_BANK1_CHANNEL1, PIN_BANK1_CHANNEL2], [GPIO.LOW, GPIO.HIGH]],
    "3": [[PIN_BANK1_CHANNEL1, PIN_BANK1_CHANNEL2], [GPIO.HIGH, GPIO.LOW]],
    "4": [[PIN_BANK1_CHANNEL1, PIN_BANK1_CHANNEL2], [GPIO.LOW, GPIO.LOW]],

    "5": [[PIN_BANK2_CHANNEL1, PIN_BANK2_CHANNEL2], [GPIO.HIGH, GPIO.HIGH]],
    "6": [[PIN_BANK2_CHANNEL1, PIN_BANK2_CHANNEL2], [GPIO.LOW, GPIO.HIGH]],
    "7": [[PIN_BANK2_CHANNEL1, PIN_BANK2_CHANNEL2], [GPIO.HIGH, GPIO.LOW]],
    "8": [[PIN_BANK2_CHANNEL1, PIN_BANK2_CHANNEL2], [GPIO.LOW, GPIO.LOW]]
}

INVERSE_CHANNELS = ["1", "2", "4"]

if len(sys.argv) != 3:
    print("%s <channel> <open|close>" % sys.argv[0])
    sys.exit()

print("Setting mode")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_BANK1_CHANNEL2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK1_CHANNEL1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK1_CLOSE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK1_OPEN, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(PIN_BANK2_CHANNEL2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK2_CHANNEL1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK2_CLOSE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BANK2_OPEN, GPIO.OUT, initial=GPIO.LOW)

channel = str(sys.argv[1])
mode = str(sys.argv[2])
if channel in INVERSE_CHANNELS:
    print("inversing")
    if mode == "open":
        mode = "close"
    elif mode == "close":
        mode = "open"

print("select channel %s" % channel)
GPIO.output(CMD_CHANNEL[channel][0], CMD_CHANNEL[channel][1])
time.sleep(0.5)
print("select %s" % mode)
if mode == "close":
    if channel <= 4:
        GPIO.output(PIN_BANK1_CLOSE, GPIO.HIGH)
    else:
        GPIO.output(PIN_BANK2_CLOSE, GPIO.HIGH)
if mode == "open":
    if channel <= 4:
        GPIO.output(PIN_BANK1_OPEN, GPIO.HIGH)
    else:
        GPIO.output(PIN_BANK2_OPEN, GPIO.HIGH)
time.sleep(1)
GPIO.cleanup()
