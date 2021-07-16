from picamera import PiCamera
import datetime
from time import sleep
import sys
import os
from lobe import ImageModel

# Lobe TF Lite model 1 (~2.5k images)
model1 = ImageModel.load('./trained_models/TFLite/model1')
# Lobe TF Lite model 2 (10k+ images)
model2 = ImageModel.load('./trained_models/TFLite/model2')

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

def main(path, model="model1"):
    if os.path.isfile(path):
        print("Predicting...")
        if model=="model1":	
            result = model1.predict_from_file(path)
        else:
            result = model2.predict_from_file(path)
        accuracy = calculate_accuracy(result)
        identify(result.prediction, accuracy)
    else:
        print(f"Image does not exist at {path}")

if __name__ == "__main__":
    print("Beginning waste classification...")
    if (len(sys.argv) -1) >= 1:
                if (len(sys.argv) -1) >=2:
                        main(sys.argv[1], sys.argv[2])
                else:
                        main(sys.argv[1], "model1")
    else:
        main("/home/pi/recycle_damn_iot/test/data/cardboard2.jpg", "model1")
