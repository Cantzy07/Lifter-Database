import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import numpy as np
from MoveNet import MoveNetRig, EDGES
from models import db, PositionalPoints
import cv2

class PositionalPointsFactory:
    def create_positional_point(lifter_id, frame):
        confidenceThreshold = 0.6

        # Remove alpha channel if present
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Reshape image
        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
        input_image = tf.cast(img, dtype=tf.float32)

        # Ensure the input image has the shape (1, 256, 256, 3)
        input_image = np.array(input_image)
        if input_image.shape != (1, 256, 256, 3):
            raise ValueError(f"Input image must have shape (1, 256, 256, 3), but got {input_image.shape}")

        keypoints_with_scores = MoveNetRig.make_predictions(input_image)

        keypoints = MoveNetRig.get_keypoints(frame, keypoints_with_scores, confidenceThreshold)
        distances = MoveNetRig.get_distances(frame, keypoints_with_scores, EDGES, confidenceThreshold)

        # make list into a string so it can be turned to json data
        keypointsString = PositionalPointsFactory.stringifyPoints(keypoints)
        distancesString = ','.join(map(str, distances))

        # Create a new PositionalPoints instance
        new_positional_point = PositionalPoints(points=(keypointsString + ";"), distances=(distancesString + ";"), lifter_id=lifter_id)
        
        return new_positional_point
    
    def stringifyPoints(keypoints):
        list_strings = [' '.join(map(str, sublist)) if isinstance(sublist, list) else str(sublist) for sublist in keypoints]
        result_string = ','.join(list_strings)
        return result_string
