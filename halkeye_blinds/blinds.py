import sys
import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        "Error importing RPi.GPIO!  " +
        "This is probably because you need superuser privileges.  " +
        "You can achieve this by using 'sudo' to run your script")


PIN_COMMON = 9
PIN_CHANNEL2 = 5
PIN_CHANNEL1 = 7
PIN_CLOSE = 11
PIN_OPEN = 13

CMD_OPEN = [PIN_OPEN]
CMD_CLOSE = [PIN_CLOSE]
CMD_CHANNEL = {
    "1": [GPIO.HIGH, GPIO.HIGH],
    "2": [GPIO.LOW, GPIO.HIGH],
    "3": [GPIO.HIGH, GPIO.LOW],
    "4": [GPIO.LOW, GPIO.LOW]
}

INVERSE_CHANNELS = ["1", "2", "4"]

if len(sys.argv) != 3:
    print("%s <channel> <open|close>" % sys.argv[0])
    sys.exit()

print("Setting mode")
GPIO.setmode(GPIO.BOARD)
# Channel Select 2 - 5
GPIO.setup(PIN_CHANNEL2, GPIO.OUT, initial=GPIO.LOW)
# Channel Select 1 - 7
GPIO.setup(PIN_CHANNEL1, GPIO.OUT, initial=GPIO.LOW)
# Close - 11
GPIO.setup(PIN_CLOSE, GPIO.OUT, initial=GPIO.LOW)
# Open - 13
GPIO.setup(PIN_OPEN, GPIO.OUT, initial=GPIO.LOW)

channel = str(sys.argv[1])
mode = str(sys.argv[2])
if channel in INVERSE_CHANNELS:
    print("inversing")
    if mode == "open":
        mode = "close"
    elif mode == "close":
        mode = "open"

print("select channel %s" % channel)
GPIO.output([PIN_CHANNEL1, PIN_CHANNEL2], CMD_CHANNEL[channel])
time.sleep(0.5)
print("select %s" % mode)
if mode == "close":
    GPIO.output(CMD_CLOSE, [GPIO.HIGH] * len(CMD_CLOSE))
if mode == "open":
    GPIO.output(CMD_OPEN, [GPIO.HIGH] * len(CMD_OPEN))
time.sleep(1)
GPIO.cleanup()
