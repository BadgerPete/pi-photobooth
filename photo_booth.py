#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess, random
from picamera import PiCamera
from time import strftime

camEffects = ['colorswap', 'sketch', 'negative', 'solarize', 'watercolor', 'posterise', 'none']

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
#GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 18 
POSE_LED = 22 
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
#GPIO.setup(BUTTON_LED, GPIO.OUT)
#GPIO.setup(PRINT_LED, GPIO.OUT)
#GPIO.output(BUTTON_LED, True)
#GPIO.output(PRINT_LED, False)

camera = PiCamera()
# Rotate camera if upside down
#camera.rotation = 180

#camera.resolution = (2592, 1944)
#camera.framerate = 15

while True:
  cEffect1 = random.choice(camEffects)
  currentEffect = random.choice(camEffects)
  cEffect2 = currentEffect
  while (cEffect1 == currentEffect):
    currentEffect = random.choice(camEffects)
    cEffect2 = currentEffect
  currentEffect = random.choice(camEffects)
  cEffect3 = currentEffect
  while (cEffect1 == currentEffect and cEffect2 == currentEffect):
    currentEffect = random.choice(camEffects)
    cEffect3 = currentEffect
  currentEffect = random.choice(camEffects)
  cEffect4 = currentEffect
  while (cEffect1 == currentEffect and cEffect2 == currentEffect and cEffect3 == currentEffect):
    currentEffect = random.choice(camEffects)
    cEffect4 = currentEffect
  if (GPIO.input(SWITCH)):
    snap = 0
    while snap < 4:
      print("pose!")
      
      # Show on screen the preview
      #camera.start_preview()
      # Choose random effect for picture
      cEffect = random.choice(camEffects)
      while (cEffect == currentEffect):
        cEffect = random.choice(camEffects)
      currentEffect = cEffect
      camera.image_effect = currentEffect

      #GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      rightNow = strftime("%H%M%S")
      print "SNAP at {0}".format(rightNow)
      camera.resolution = (2592, 1944)
      camera.framerate = 15
      camera.capture("/home/pi/photobooth_images/photobooth{0}.jpg".format(rightNow))
      snap += 1
      #gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      #gpout = subprocess.check_output('camera.capture("/home/pi/photobooth_images/photobooth%H%M%S.jpg")', stderr=subprocess.STDOUT, shell=True)
      #print(gpout)
      #if "ERROR" not in gpout: 
      #  snap += 1
      #GPIO.output(POSE_LED, False)
      time.sleep(0.5)
    print("please wait for the photo booth to get ready...")
    #GPIO.output(PRINT_LED, True)
    # build image and send to printer
    # DO NOT PRINT but make into a photo booth strip
    subprocess.call("/home/pi/scripts/photobooth/assemble_and_print false", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    time.sleep(10)
    print("ready for next round")
    #GPIO.output(PRINT_LED, False)
    #GPIO.output(BUTTON_LED, True)
