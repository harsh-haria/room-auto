import numpy as np
import cv2
import pickle
import time
import RPi.GPIO as GPIO

master1=[]
switch=[]
master_name=""

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
labels = {"person_name":1}
with open("labels.pickle","rb") as f:
    labels = pickle.load(f)
    labels= {v:k for k,v in labels.items()}
class facedetection:
    def loop():
        try:
            cap = cv2.VideoCapture(0)
            while True:
                #Capture frame-by-frame
                ret,frame=cap.read()
                cv2.imshow("frame1",frame)
                #cv2.imshow("frame2",gray)
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
                for(x,y,w,h) in faces: #for printing the face detected values
                    #print(x,y,w,h)
                    roi_gray=gray[y:y+h,x:x+w]#(yCord_start, yCord_end)
                    roi_color=frame[y:y+h,x:x+w]
                    #global master_name
                    id_, conf = recognizer.predict(roi_gray)
                    global master_name
                    master_name = labels[id_]
                    if conf>=45 and conf<=85:
                        print(id_," ",conf," ",labels[id_])
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        name = labels[id_]
                        color=(255,255,255)
                        stroke = 2
                        cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
                    img_item = "my-img.jpg"#saving picture
                    img_item1 = "my_img.jpg"
                    cv2.imwrite(img_item,roi_gray)#display result frame
                    cv2.imwrite(img_item1,roi_color)
                    color=(255,0,255)#not rgb but bgr
                    stroke=2
                    end_cord_x = x+w
                    end_cord_y = y+h
                    cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)
                cv2.imshow("frame1",frame)
                if(master_name): #actually no need for it could have been directly done
                    master1.append(master_name)
                    break
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
                    #exit()
            cap.release()
            cv2.destroyAllWindows()
            print("Facial Data found")
            print(master1[0])
        except IndexError:
            print("UPDATE: data not found!")

    def switchdata():
        try:
            #g = open("H:\\home\\pi\\python\\CONFIG\\abcd","r")
            #g = open("D:\\programming\\python\\CONFIG\\"+master1[0]+".txt","r")#for windows
            config_file = open("/home/pi/python/CONFIG/"+master1[0]+".txt","r")#for linux
            if(config_file.mode=="r"):
                contents = config_file.read()
            #print(contents)
            data = contents.split()
            #switch.append(data[3])
            switch.append(data[4])
            switch.append(data[5])
            switch.append(data[6])
            switch.append(data[7])
            switch.append(data[8])
            #print(*switch)
            #time.sleep(10)
            for i in range(0,5):
                print(switch[i])
        except IndexError:
            print("Some Error was encountered")

class pins:
    def setgpio():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        global relay_1
        relay_1 = 5
        global relay_2
        relay_2 = 6
        global relay_3
        relay_3 = 13
        global relay_4
        relay_4 = 19
        global relay_5
        relay_5 = 26
        global button_exito
        button_exito = 15
        GPIO.setup(relay_1, GPIO.OUT)
        GPIO.setup(relay_2, GPIO.OUT)
        GPIO.setup(relay_3, GPIO.OUT)
        GPIO.setup(relay_4, GPIO.OUT)
        GPIO.setup(relay_5, GPIO.OUT)
        GPIO.output(relay_1, False)
        GPIO.output(relay_2, False)
        GPIO.output(relay_3, False)
        GPIO.output(relay_4, False)
        GPIO.output(relay_5, False)                
        GPIO.setup(button_exito,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    def gpio():
        if(switch[0]==1):
            GPIO.output(relay_1,GPIO.LOW)
        if(switch[1]==1):
            GPIO.output(relay_2,GPIO.LOW)
        if(switch[2]==1):
            GPIO.output(relay_3,GPIO.LOW)
        if(switch[3]==1):
            GPIO.output(relay_4,GPIO.LOW)
        if(switch[4]==1):
            GPIO.output(relay_5,GPIO.LOW)
        time.sleep(2)
        
    def exito():
        GPIO.output(relay_1,GPIO.HIGH)
        GPIO.output(relay_2,GPIO.HIGH)
        GPIO.output(relay_3,GPIO.HIGH)
        GPIO.output(relay_4,GPIO.HIGH)
        GPIO.output(relay_5,GPIO.HIGH)
        GPIO.cleanup()

    #def button_callback(channel):
        #print("the button was pushed! now exiting....")

try:
    while True:
        loop()
        switchdata()
        setgpio()
        gpio()
        while True:
            if GPIO.input(15)==GPIO.HIGH:
                print("Button was pushed!")
                exito()
                #a = input()
                #if(a):
                switch = []
                master1 = []
                master_name=""
                time.sleep(0.5)
                break
except:
    print("some errorm occured")
    GPIO.cleanup()
