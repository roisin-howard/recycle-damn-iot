from picamera import PiCamera
import datetime
from time import sleep
import sys
import os
from lobe import ImageModel

CAPTURING = False
CLASSIFYING = False
fullname = ""

# Lobe TF Lite model working
model = ImageModel.load('./trained_models/TFLite')
# Lobe Tensor Flow model not working
#model = ImageModel.load('/home/pi/recycle_damn_iot/trained_models/TensorFlow')

def capture(path):
    global fullname, CAPTURING
    camera = PiCamera()
    try:
        print("Capturing image...")
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


def identify(label, percentage):
    global CLASSIFYING
    print("This item is: " + label + "(" + percentage + "%)")
    CLASSIFYING = False
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


def parse_result(result):
    # {"Labels": [["paper", 1.0], ["metal", 9.21433623846113e-11], ["glass", 9.720557556580287e-14], ["cardboard", 7.98967757730494e-14], ["plastic", 4.54364270071673e-15], ["trash", 2.5402109394759417e-15]], "Prediction": "paper"}
    # print(result.prediction)
    percentage = 0
    for item in result.labels:
        print(item)
        if item[0] == result.prediction:
            value = item[1]
            percentage = value/1*100
            percentage = str("{:.2f}".format(percentage))
    return percentage


def main(path):
    global CLASSIFYING
    global CAPTURING
    while True:
        if (not CAPTURING and not CLASSIFYING):
            CLASSIFYING = True
            capture(path)
            print("Predicting...")
            result = model.predict_from_file(fullname)
            percentage = parse_result(result)
            identify(result.prediction, percentage)
        else:
            print("Please wait a moment and try again")
            if CLASSIFYING:
                print("The image is currently being classified")
            if CAPTURING:
                print("The image is currently being captured")


if __name__ == "__main__":
    print("Beginning waste classification...")
    main("./images/")
               
