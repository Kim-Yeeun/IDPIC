
import RPi.GPIO as GPIO
import time
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 23
echo = 24

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

print("\n*** This is ID Picture Program ***\n")

# Enter File Name
while True:
	print("---------------------------------------------------------------------------")
	print("1. Please enter the file name. (ex.Jeny.jpg, lisa.png) : ", end='')
	file_name = input()
	file_extension = file_name[len(file_name)-4:]
	if file_extension == '.jpg' or file_extension == '.png':
		break
	else:
		print("\nIt's not correct file extension!")
		print("You can use only '.jpg' or '.png'\n")
		continue
print("---------------------------------------------------------------------------\n")

print("---------------------------------------------------------------------------")
print("2. Please adjust the distance to take a ID Picture")
print("---------------------------------------------------------------------------\n")

time.sleep(2)

# set buzzer
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 100)

def buzzer_on():
	p.start(10)
	time.sleep(0.5)
	p.stop()

# set button
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# set LED
red_pin = 17
GPIO.setup(red_pin, GPIO.OUT)
green_pin = 27
GPIO.setup(green_pin, GPIO.OUT)
blue_pin = 22
GPIO.setup(blue_pin, GPIO.OUT)

# Measurement Distance
try:
	while True:
		GPIO.output(trig, True)
		time.sleep(0.00001)
		GPIO.output(trig, False)
		
		while GPIO.input(echo) == 0:
			pulse_start = time.time()
		while GPIO.input(echo) == 1:
			pulse_end = time.time()
			
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 34300 / 2
		distance = round(distance, 2)
		time.sleep(1)
		if distance <= 40: # buzzer on
			GPIO.output(red_pin, 1)
			time.sleep(0.5)
			print("It's too close!")
			buzzer_on()
			GPIO.output(red_pin, 0)
			time.sleep(0.5)
			continue
		elif distance >= 70:
			GPIO.output(blue_pin, 1)
			time.sleep(0.5)
			print("It's too far!")
			buzzer_on()
			GPIO.output(blue_pin, 0)
			time.sleep(0.5)
			continue
		else:
			GPIO.output(green_pin, 1)
			print("\n---------------------------------------------------------------------------")
			print("3. It's ready to take a picture.")
			print("   The camera will be on soon...")
			print("---------------------------------------------------------------------------\n")
			time.sleep(5)
			
			with picamera.PiCamera() as camera:
				camera.resolution = (640, 480)
				camera.start_preview()
				while GPIO.input(15) == 0:
					time.sleep(0.1)
				time.sleep(1)
				camera.capture(file_name)
				camera.stop_preview()
			GPIO.output(green_pin, 0)
			time.sleep(0.5)
			while True:
				YN = 0
				print("---------------------------------------------------------------------------")
				print("4. Do you want to take a picture again? (Yes / No) : ", end='')
				answer = input()
				print("---------------------------------------------------------------------------")
				if answer == 'No':
					break
				elif answer == 'Yes':
					YN = 1
					break
				else:
					print("You can only answer 'Yes' or 'No'\n")
					continue
			if YN == 0:
				print("\n*** The Program will be end ***")
				GPIO.cleanup()
				break
except KeyboardInterrupt:
	print("Measurement stopped by User")
	GPIO.cleanup()
	

