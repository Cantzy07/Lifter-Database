import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import numpy as np
import cv2
import math

# Load Model
interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_thunder_3.tflite')
interpreter.allocate_tensors()

# ears and eyes points
UNWANTED_POINTS = [1, 2, 3, 4]

# EDGES is a dictionary
# Each key is a set of points connecting each point to another ex: (0,1) point 0 -> point 1
# Each value specifies a color
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


# Class to use to get metrics on the body of image given
class MoveNetRig:
    # Get x,y coords of each keypoint on the body and store in points
    def get_keypoints(frame, keypoints, confidence_threshold):
        points = [0] * 17  # initial points before set to a list holding x,y coords in each index
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

        for index, kp in enumerate(shaped):
            ky, kx, kp_conf = kp
            if index not in UNWANTED_POINTS:  # don't draw ears and eyes
                if kp_conf > confidence_threshold:
                    points[index] = [round(kx, 4), round(ky, 4)]
        return points

    def get_distances(frame, keypoints, edges, confidence_threshold):
        distances = [0] * 14  # distances between each of the joints
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

        joint_count = 0

        for edge, color in edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]

            if p1 not in UNWANTED_POINTS and p2 not in UNWANTED_POINTS:  # don't draw ear connections
                if c1 > confidence_threshold and c2 > confidence_threshold:
                    distance = round(math.sqrt((x1-x2)**2 + (y1-y2)**2), 5)
                    distances[joint_count] = distance
                    joint_count += 1
        return distances

    def make_predictions(input_image):
        # Setup input and output
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Make predictions
        interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        interpreter.invoke()
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

        return keypoints_with_scores

# # Rigging in real time using a webcam
# # Draw Keypoints
# def draw_keypoints(frame, keypoints, confidence_threshold):
#     y, x, c = frame.shape
#     shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

#     for index, kp in enumerate(shaped):
#         ky, kx, kp_conf = kp
#         if index not in UNWANTED_POINTS:  #don't draw ears and eyes
#             if kp_conf > confidence_threshold:
#                 cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)


# # Draw Edges
# def draw_connections(frame, keypoints, edges, confidence_threshold):
#     y, x, c = frame.shape
#     shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

#     for edge, color in edges.items():
#         p1, p2 = edge
#         y1, x1, c1 = shaped[p1]
#         y2, x2, c2 = shaped[p2]

#         if p1 not in UNWANTED_POINTS and p2 not in UNWANTED_POINTS:  #don't draw ear connections
#             if (c1 > confidence_threshold) and (c2 > confidence_threshold):
#                 cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)


# if __name__ == "__main__":
#     # Make Detections
#     cap = cv2.VideoCapture(0)

#     while cap.isOpened():
#         ret, frame = cap.read()

#         # Reshape image
#         img = frame.copy()
#         img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
#         input_image = tf.cast(img, dtype=tf.float32)

#         # Setup input and output
#         input_details = interpreter.get_input_details()
#         output_details = interpreter.get_output_details()

#         # Make predictions
#         interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
#         interpreter.invoke()
#         keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

#         # Rendering
#         draw_connections(frame, keypoints_with_scores, EDGES, 0.6)
#         draw_keypoints(frame, keypoints_with_scores, 0.6)

#         cv2.imshow('MoveNet Thunder', frame)

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
