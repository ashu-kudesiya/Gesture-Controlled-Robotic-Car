import cv2
import sys
import serial
import serial.tools.list_ports
from cvzone.HandTrackingModule import HandDetector
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass


# Initialize the controller configuration
@dataclass
class ControllerConfig:
    '''
        Is a Special class, which automatically creates the special methods like __init__ and __repr__ 
        Will use it to store three variables
        1. object of cam
        2. hand detector object

    '''
    # Object of camera
    cam = cv2.VideoCapture(0)
    cam.set(3, 1080)
    cam.set(4, 720)

    # Object of hand detector class
    detector = HandDetector(detectionCon=0.5, maxHands=1)

    # defining the port
    port = 'COM3'

    # Establishing the serial communication
    ser = serial.Serial(port, 9600, timeout=1)


# Create a class to send the commands to Arduino via bluetooth
class SendCommands:
    def __init__(self, count):
        '''
            count - no. of fingers up
            controllerconfig - object of the above data class ControllerConfig


        '''
        logging.info("Sending command configuration starts")
        self.controllerconfig = ControllerConfig()
        logging.info("Sending command configuration completed")
        self.count = count

    # Create a method to send the message to arduino

    def send_message(self):
        '''
            1. Reads the data(no. of fingers up)
            2. encode the data
            3. write the encoded data to the serial monitor of arduino

        '''
        try:
            # Convert the count of fingers to string
            num_fingers_str = str(self.count)
            logging.info("Writing the encoded message to serial monitor")

            # Write the code to serial monitor
            self.controllerconfig.ser.write(num_fingers_str.encode())

        except Exception as e:
            logging.info("Error occured while sendinf the command")
            raise CustomException(e, sys)


# Create a class to control the car
class Controller:
    def __init__(self):
        logging.info("Controller configuration starts")
        self.controllerconfig = ControllerConfig()
        logging.info("Controller configuartion completed")

    # Create a method to move the car
    def move_car(self):
        '''
            1. create a frame/window of the what the cam is capturing
            2. find hands using the detector object of Handetecor class
            3. counts the no. of fingers up
            4. puts  text of no. of fingers up
            5. puts the text forward, backward, lrft, right, stop according to the no. of fingers up
            6. creates the object of class SendCommands
            7. sends the data{no. of fingers up} using controlCar method of class SendCommands
            8. displays the frame 

        '''
        try:

            while True:
                logging.info("Capturing frames from the cam")

                # get the image of from the system cam
                ret, frame = self.controllerconfig.cam.read()
                logging.info("Captured frame")

                # Flip the frame
                frame = cv2.flip(frame, 1)

                logging.info("Finding hand in the captured frame")

                # Find/detect the hands using the methods of HandDetector class
                hands, frame = self.controllerconfig.detector.findHands(frame)
                logging.info("Found hand")

                if hands:
                    hands1 = hands[0]
                    logging.info("Counting how many finger are up")

                    # Count the number of fingers up
                    fingers = self.controllerconfig.detector.fingersUp(hands1)
                    count = fingers.count(1)

                    # Put text for number of fingers that are up
                    logging.info("Putting text for no. of fingures up")
                    cv2.putText(frame, str(count), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                                5, (255, 0, 0), 10)

                    if count == 5:
                        logging.info("Putting text MOVE FORWARD ")
                        cv2.putText(frame, 'MOVE FORWARD', (5, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 10)

                    elif count == 0:
                        logging.info("Putting text STOP")
                        cv2.putText(frame, 'STOP', (5, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 10)

                    elif count == 1:
                        logging.info("Putting text TURN LEFT")
                        cv2.putText(frame, 'TURN LEFT', (5, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 10)

                    elif count == 2:
                        logging.info("Putting text TURN RIGHT")
                        cv2.putText(frame, 'TURN RIGHT', (5, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 10)

                    elif count == 3:
                        logging.info("Putting text MOVE BACKWARD")
                        cv2.putText(frame, 'MOVE BACKWARD', (5, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 10)

                    logging.info("Sending commands to the arduino")

                    # Send command to Arduino based on the number of fingers up
                    car_controller = SendCommands(count)
                    logging.info("Commands sent")
                    logging.info("Controlling the car")
                    car_controller.send_message()

                logging.info("Displaying the frame")

                # Display the frame
                cv2.imshow('Frame', frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
        except KeyboardInterrupt as k:
            logging.info("Error occured while controlling the car")


if __name__ == '__main__':
    Car = Controller()
    Car.move_car()
