from picamera import PiCamera
import datetime
from time import sleep
import sys
import os
from lobe import ImageModel

CAPTURING = False
CLASSIFYING = False
fullname = ""

# Load Lobe TF model
#model = ImageModel.load('/home/pi/recycle_damn_iot/lobe/model')

def capture(path):
    global fullname
    camera = PiCamera()
    try:
        CAPTURING = True
        camera.rotation=180
        #camera.resolution = (2592, 1944)
        #camera.framerate = 15
        camera.start_preview(alpha=200)
        sleep(3) #allow for light to adjust
        timestamp = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        filename = "%s.jpg" % timestamp
        fullname = path + filename
        camera.capture(fullname)
        print(f"Saving image to {fullname}")
        camera.stop_preview()
        pass
    finally:
        camera.close()
        CAPTURING = False

def identify(label):
    print(label)
    if label == "trash":
        print("This goes in the waste bin")
        sleep(5)
    if label == "paper":
        print("This goes in the recycling bin")
        sleep(5)
    if label == "plastic":
        print("This goes in the recycling bin")
        sleep(5)
    if label == "cardboard":
        print("This goes in the recycling bin") 
        sleep(5)
    if label == "glass":
        print("This can be brought to the bottle bank") 
        sleep(5)
    if label == "metal":
        print("This can be brought to a metal recycling centre") 
        sleep(5)
    else:
        print("Unknown, please research where to dispose of this item correctly")
    CLASSIFYING = False

def main(path):
    CLASSIFYING = False
    CAPTURING = False
    while True:
    	if (not CAPTURING and not CLASSIFYING):
#        CLASSIFYING = True
        	capture(path)
#        result = model.predict_from_file(fullname)
#        identify(result.prediction)
    	else:
        	print("Please wait a moment and try again")


if __name__ == "__main__":
    print("Beginning waste classification...")
    main("/home/pi/recycle_damn_iot/images/")
               
