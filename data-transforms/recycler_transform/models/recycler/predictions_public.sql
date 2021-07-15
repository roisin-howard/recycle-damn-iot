# Basic select to see how datasets get generated
SELECT
    id as prediction_id,
    device_id,
    pred_label as prediction,
    pred_accuracy as accuracy,
    pred_datetime as predicted_on
FROM `hackathon-recycler-damn-iot`.recycler_dataset.predictions_raw