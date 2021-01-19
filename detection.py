"""Lookout was constructed by two University of Ryerson 2nd Year
    Computer Science students: Gursharan Grewal and Ajaybir Singh Randhawa.
    It is meant to provide security to students who have to leave their devices
    unattended due to various reasons in public places. This product requires 
    access to webcam for it to work."""

#Import all files needed
from imutils.video import VideoStream
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from colorama import Fore, Style

import os
import numpy as np
import smtplib
import argparse
import datetime
import imutils
import time
import cv2
import pyautogui
os.system("cls")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\u001b[37m'

path = os.getcwd()
relative_path = path + '\screenshot.png'

email_user = 'protection.alert@yahoo.com'
email_password = 'pgfjydlmikowcwbn'
def intro():
    print(bcolors.OKBLUE + """
     __      __       .__                               
    /  \    /  \ ____ |  |      ____    _____    _____    _____ 
    \   \/\/   // __ \|  |    _/ ___\  /  _  \  /     \__/ __  \  
     \        /\  ___/|  |___ \  \___ (  <_>  )/   Y Y   \  ___/ 
      \__/\  /  \___  >______/ \_____> \_____/ \ |__|_|  /\___  >
           \/       \/          \/              \/     \/     \/ 
    """+ bcolors.WHITE)
    print(bcolors.OKBLUE + """
    Lookout is a Python program developed by Ajaybir Randhawa and Gursharan Grewal, 
    making use of the OpenCV library and its real-time computer vision functionality. When
    activated, the application detects for movement around the user's workspace by making 
    use of the devices camera. The detection sensitivity can be modified by the user to 
    enforce protection at various ranges to accomodate for all types of environments. When 
    triggered, the program sends the user an alert using the provided email, attaching the 
    image containing the activity for its security measures.""" + bcolors.WHITE)
    print(bcolors.HEADER + """

    .___                   __                            __   .__                         
    |   |  ____    _______/  |_ _______  __ __   ____  _/  |_ |__|  ____    ____    ______
    |   | /    \  /  ___/\   __/\_  __ \|  |  \_/ ___\ \   __\|  | /  _ \  /    \  /  ___/
    |   ||   |  \ \___ \  |  |   |  | \/|  |  /\  \___  |  |  |  |(  <_> )|   |  \ \___ \ 
    |___||___|  //____  > |__|   |__|   |____/  \___  > |__|  |__| \____/ |___|  //____  >
              \/      \/                            \/                         \/      \/                                                                                                                
    """+ bcolors.WHITE)
    print(bcolors.OKBLUE + """
    Press A at any time to stop the program
    This program will require access to your webcam. If
    any major disturbances occur in the determined webcams range
    it will take a screenshot and terminate.
    NOTE: Please leave the frame prior to countdown being completed
    as any attempt to move after countdown will trigger it. User will
    have 10 seconds to leave the cameras range."""+ bcolors.WHITE)                                                                         

def changearea():
    area = int(input(bcolors.OKGREEN + """Please enter a number between 100-1300.
    The number will choose a threshold, if the threshold is too 
    high more movement will be allowed in the cameras range. If
    threshold is too low, any possible movement in the cameras range
    will trigger the program. """ + bcolors.WARNING + "LOWER THRESHOLD FOR DIMLY LIT AREAS" + bcolors.OKGREEN + """
    1200 will pick up movement in 3' of the camera.
    1000 will pick up movement in 6' of camera.""" + bcolors.HEADER + "(DEFAULT)" + bcolors.OKGREEN + """
    720 will pick up movement in 9' of the camera.
    """ + bcolors.WHITE))
    while area <500 or type(area) is not int or area > 1300:
        print(bcolors.FAIL + "Invalid input! Please enter an integer value of 100-1300 without commas."+ bcolors.WHITE)
        area = int(input(bcolors.WHITE + "Please enter a threshold number:"))
    return area

def stop():
    print(bcolors.HEADER + """
      ________                     .___ _________                 
     /  _____/   ____    ____    __| _/ \_____   \ ___.__.  ____  
    /   \  ___  /  _ \  /  _ \  / __ |   |   |  _/<   |  |_/ __ \ 
    \    \_\  \(  <_> )(  <_> )/ /_/ |   |   |   \ \___  |\  ___/ 
     \______  / \____/  \____/ \____ |   |_____  / / ____| \___  >
            \/                      \/         \/  \/          \/ 
    """ + bcolors.WHITE)
    print(bcolors.OKCYAN + """
    ------------------------------------------------------------
            BY: Ajaybir Randhawa and Gursharn Grewal
                    Ryerson University, 2021
    ------------------------------------------------------------""" + bcolors.WHITE)

intro()
end = False
#Check for proper area size
ans = str(input(bcolors.WHITE + "Do you wish to edit area size? (No will use Default) [Yes/No]")).lower()
while ("yes" != ans) and ("no" != ans):
    print(bcolors.FAIL + "Invalid input! Please enter Yes or No."+ bcolors.WHITE)
    ans = input(bcolors.WHITE + "Do you wish to edit area size? (No will use Default) [Yes/No]").lower()

if ans.lower() == "yes":
    area = changearea()
else:
    area = 1000

email_send = input(bcolors.WHITE + 'Enter the email you want to receive the alert on:')
#Loop to check for proper email
while ("@" not in email_send) or ('.' not in email_send):
    print(bcolors.FAIL + "Invalid input! Please re-enter correct email address"+ bcolors.WHITE)
    email_send = input(bcolors.WHITE + "Enter the email you want to receive the alert on: ")

subject = 'Security Alert'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = """Hello, 
    This email is to inform you that we have detected unexpected movement near your device. If you are not near your device, please make sure it is safe and secured. The attachment below contains an image of the movement detected. 

Confidential Transmissions: 
    This message is intended only for the use of the individual to whom it is addressed, and may contain information that is privileged and confidential. If the reader of this message is not the intended recipient, you are hereby notified that any dissemination, distribution, or copying of this communication is strictly prohibited. 
    If you have received this communication in error, please notify the sender immediately by replying to the email and confirming that you have permanently deleted the original transmission, including attachments, without making a copy."""
msg.attach(MIMEText(body, 'plain'))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src = 0).start()
	time.sleep(2.0)
# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
counter = 10
while counter >0:
    color = bcolors.OKBLUE if counter > 3 else bcolors.WARNING
    print(color + f"Starting in {counter}" + bcolors.WHITE)
    time.sleep(1)
    counter-=1
# loop over the frames of the video
while True:
    #Grab the current frame and detect if it exists
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "NULL Activity - Safe"

	# if frame is not grabbed, the video feed has been ended
    if frame is None:
        break

    #Resize the frame, convert to grey scale, Current frame is now called 'gray'
    frame = imutils.resize(frame, width=1000)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    #If frames have not been initialized
    if firstFrame is None:
        firstFrame = gray
        continue

    # Literally the entire program works based on the next 5 lines
    
    #Computing the difference between current frame and 1st frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 140, 255, cv2.THRESH_BINARY)[1]

    #Dilate the new image to fill any gaps then find contours on it
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
	# loop over the contours
    for cont in cnts:
        print(cv2.contourArea(cont), area)
        if cv2.contourArea(cont) < area:
            continue
        (x, y, w, h) = cv2.boundingRect(cont)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 2)
        text = "Detected - Unsafe"
        if text != "NULL Activity - Safe" and end != True:
            screenshot = pyautogui.screenshot()
            screenshot.save(relative_path)
            filename='screenshot.png'
            attachment = open(filename, 'rb') #TO allow for email attachment
            part = MIMEBase('application', 'octet-stream') #Allows us to send email and close app
            part.set_payload((attachment).read())
            #So its somewhat secure
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename = ' + filename)
            msg.attach(part)
            try:
                print(bcolors.OKBLUE + "Sending Email"+ bcolors.WHITE)
                server = smtplib.SMTP("smtp.mail.yahoo.com", 587)
                server.starttls()
                server.login(email_user, email_password)
                server.sendmail(email_user, email_send, msg.as_string())
                server.quit()
                end = True
                print(bcolors.OKGREEN + "Email sent" + bcolors.WHITE)
            except :
                print("Error, Email not sent.")
			
    # Text on Frames
    cv2.putText(frame, "Lookout Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    #User control
    cv2.imshow("Lookout", frame)
    #If user comes back and wishes to end program 
    ctrlAbort = cv2.waitKey(1) & 0xFF
    if ctrlAbort == ord("a"):
        break
    if end==True:
        break

stop()
#Close any open windows and end video
if args.get("video", None):
    vs.stop()
cv2.destroyAllWindows()