from picamera import PiCamera
import datetime
from time import sleep
import sys
import os
from lobe import ImageModel

from helpers import getserial
from models.prediction import Prediction
from data_stream.BigQueryClient import BigQueryClient

CAPTURING = False
CLASSIFYING = False
fullname = ""

# Lobe TF Lite model 1 (~2.5k images) 
#model = ImageModel.load('./trained_models/TFLite/model1')
# Lobe TF Lite model 2 (10k+ images) 
model = ImageModel.load('./trained_models/TFLite/model2')

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
    print("This item is: " + label + " (" + percentage + "%)")
    CLASSIFYING = False
    if label == "trash":
        print("This goes in the waste bin")
    elif label == "battery":
        print("This can be brought to a battery recycling centre")
    elif label == "paper":
        print("This goes in the recycling bin")
    elif label == "plastic":
        print("This goes in the recycling bin")
    elif label == "cardboard":
        print("This goes in the recycling bin") 
    elif label == "brown-glass":
        print("This can be brought to the bottle bank") 
    elif label == "white-glass":
        print("This can be brought to the bottle bank") 
    elif label == "green-glass":
        print("This can be brought to the bottle bank") 
    elif label == "metal":
        print("This can be brought to a metal recycling centre") 
    elif label == "compost":
        print("This can be put in the compost bin") 
    else:
        print("Unknown, please research where to dispose of this item correctly")


def calculate_accuracy(result):
    # {"Labels": [["paper", 1.0], ["metal", 9.21433623846113e-11], ["glass", 9.720557556580287e-14], ["cardboard", 7.98967757730494e-14], ["plastic", 4.54364270071673e-15], ["trash", 2.5402109394759417e-15]], "Prediction": "paper"}
    # print(result.prediction)
    percentage = 0
    for item in result.labels:
        if item[0] == result.prediction:
            value = item[1]
            percentage = value/1*100
            percentage = str("{:.2f}".format(percentage))
    return percentage

def send_result(label, percentage):
    bq = BigQueryClient()
    timestamp = datetime.datetime.now()
    
    pred = Prediction()
    pred.set_id(int(timestamp.timestamp()))
    pred.set_device_id(getserial())
    pred.set_prediction(label)
    pred.set_accuracy(percentage)
    pred.set_prediction_datetime(timestamp)
    
    bq.stream_data('hackathon-recycler-damn-iot', 'recycler_dataset', 'predictions_raw', pred)


def rename_image(path, label):
    file_name = os.path.basename(path)
    dir_name = os.path.dirname(path)
    new_name = dir_name + "/" + label + "-" + file_name
    result = os.rename(path, new_name)
    return new_name

def main(path):
    global CLASSIFYING
    global CAPTURING
    try:
        while True:
            if (not CAPTURING and not CLASSIFYING):
                CLASSIFYING = True
                capture(path)
                print("Predicting...")
                result = model.predict_from_file(fullname)
                accuracy = calculate_accuracy(result)
                send_result(result.prediction, accuracy)
                identify(result.prediction, accuracy)
                new_filename = rename_image(fullname, result.prediction)
                print(f'Renaming image to: {new_filename}')
            else:
                print("Please wait a moment and try again")
                if CLASSIFYING:
                    print("The image is currently being classified")
                if CAPTURING:
                    print("The image is currently being captured")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    print("Beginning waste classification...")
    main("./images/")
               
