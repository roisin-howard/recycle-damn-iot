from uuid import uuid4
from datetime import datetime

class Prediction(object):
    _id = int()
    _device_id = str()
    _prediction = str()
    _accuracy = float()
    _prediction_datetime = datetime.utcnow()

    def set_id(self, value):
        self._id = value

    def get_id(self):
        return self._id

    def set_device_id(self, value):
        self._device_id = value

    def get_device_id(self):
        return self._device_id

    def set_prediction(self, value):
        self._prediction = value

    def get_prediction(self):
        return self._prediction

    def set_accuracy(self, value):
        self._accuracy = value

    def get_accuracy(self):
        return self._accuracy

    def set_prediction_datetime(self, value):
        self._prediction_datetime = value

    def get_prediction_datetime(self):
        return self._prediction_datetime