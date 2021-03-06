import numpy as np
import argparse
import cv2 as cv
import time
import os
from yolo_utils import infer_image
from pathlib import Path

FLAGS = []

def yolo_detect(frames,labelh,net):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-l', '--labels',
                        type=str,
                        default='./yolov3-coco/coco-labels',
                        help='Path to the file having the labels in a new-line seperated way.')

    parser.add_argument('-c', '--confidence',
                        type=float,
                        default=0.5,
                        help='The model will reject boundaries which has a \
				probabiity less than the confidence value. \
				default: 0.5')

    parser.add_argument('-th', '--threshold',
                        type=float,
                        default=0.3,
                        help='The threshold to use when applying the Non-Max Suppresion')                                     

    FLAGS, unparsed = parser.parse_known_args()
    
  
    # Get the labels
    labels = open(FLAGS.labels).read().strip().split('\n')
    # Intializing colors to represent each label uniquely
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
    # Get the output layer names of the model
    layer_names = net.getLayerNames()
    
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
   
    height , width =  None, None
    writer = None
    count = 0
    for frame in frames:
        print("frame count :",count)
        detect = 0
        if(count%2==0):
            if width is None or height is None:
                width = frame.shape[1]
                height  = frame.shape[0]
            
            detect = infer_image(net, layer_names, height, width, frame, colors, labels, FLAGS,labelh)
        count += 1
        if detect == 0:
            continue
        else:
            return detect
    return detect
    

 
