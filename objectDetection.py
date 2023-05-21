# imports for the computer vision model, video input from the USB camera and video output to screen
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# import for real-time feedback (text-to-speech)
import subprocess

# import for GPIO library to detect push button state
import RPi.GPIO as GPIO

# initializing button pin 
but_pin = 15  
GPIO.setmode(GPIO.BOARD)
GPIO.setup(but_pin, GPIO.IN)

# setup the detection model, camera and display
net = detectNet("ssd-mobilenet-v2", threshold=0.1)
camera = videoSource("/dev/video0")     
display = videoOutput("display://0") 

# set of labeled classes
classes = ["unlabeled", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "street sign", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eye glasses", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "mirror", "dining table", "window", "desk", "toilet", "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# main logic loop
while display.IsStreaming():
    # capture an image using the camera
    img = camera.Capture()

    if img is None: # capture timeout
        continue
    
    # go through all the identified objects, selecting the one with the highest confidence value
    maxConfidence = 0
    maxClass = 0
    detections = net.Detect(img)
    for i in range(len(detections)):
        print(classes[detections[i].ClassID])
        if detections[i].Confidence > maxConfidence:
            maxConfidence = detections[i].Confidence
            maxClass = classes[detections[i].ClassID]
    
    # if push button is pressed, use text-to-speech to provide real-time feedback regarding the object classified
    if GPIO.input(but_pin) == 0:
        subprocess.call(['espeak-ng', str(maxClass)])

    # display input image with bounded object segmentations, labels, and confidence values   
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
