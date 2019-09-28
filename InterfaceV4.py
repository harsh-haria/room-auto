import os
import shutil
import fnmatch
import tkinter as tk
from PIL import Image as i1
import numpy as np
from cv2 import *
from cv2 import CascadeClassifier as CC
from cv2 import face as f1
from cv2 import VideoCapture as vc
from cv2 import imwrite as im
import pickle
from tkinter import *
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox


class Interfacer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Create, Read, Update, Delete, Train):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select Option!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        create_Button = Button(self, text="Create", font=controller.title_font, bg="tomato", cursor="circle",
                            command=lambda: controller.show_frame("Create"))

        read_button = tk.Button(self, text="Read", font=controller.title_font, bg="tomato", cursor="circle",
                            command=lambda: controller.show_frame("Read"))

        update_button = tk.Button(self, text="Update", font=controller.title_font, bg="tomato", cursor="circle",
                            command=lambda: controller.show_frame("Update"))

        delete_button = tk.Button(self, text="Delete", font=controller.title_font, bg="tomato", cursor="circle",
                            command=lambda: controller.show_frame("Delete"))

        train_button = tk.Button(self, text="Train", font=controller.title_font, bg="tomato", cursor="circle",
                            command=lambda: controller.show_frame("Train"))
        
        create_Button.pack(padx=5, pady=30, ipadx=5, ipady=5)
        read_button.pack(padx=5, pady=30, ipadx=5, ipady=5)
        update_button.pack(padx=5, pady=30, ipadx=5, ipady=5)
        delete_button.pack(padx=5, pady=30, ipadx=5, ipady=5)
        train_button.pack(padx=5, pady=30, ipadx=5, ipady=5)

class Create(tk.Frame):

    def checkEntry():
        if(Name_label.get() and Age_label.get() and pass_label.get() and filename):
            for name in files:
                if(Name_label.get()==name):
                    msg = messagebox.showinfo("Error", "Same username is being used by other user!")
                else:
                    Create.submit()
        else:
            msg = messagebox.showinfo("Error", "Please fill all the correct information")

    def forName(inp):
        if inp in "abcdefghijklmnopqrstuvwxyz":
            return True
        else:
            return False
        
    def forAge(inp):
        if inp.isdigit():
            #if inp>=100:
            return True
        #elif inp is " ":
            #return True
        else:
            return False

    def path():
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))

    def show_message():
        msg2 = messagebox.showinfo("NOTE","Make sure that the video file is named 'video.mp4'")
        msg = messagebox.showinfo("This is the path", filename)

    def submit():
        """Config File"""
        #try:
        global location
        location = "D:\\programming\\pytho"
        
        f = open((location+"\\CONFIG\\"+Name_label.get()+".txt").lower(), "w+")
        f.write(Name_label.get())
        f.write(" ")
        f.write(Age_label.get())
        f.write(" ")
        f.write(pass_label.get())
        f.write(" ")
        #f.write(f"{cv1.get()}")
        #f.write(" ")
        f.write(f"{cv2.get()}")
        f.write(" ")
        f.write(f"{cv3.get()}")
        f.write(" ")
        f.write(f"{cv4.get()}")
        f.write(" ")
        f.write(f"{cv5.get()}")
        f.write(" ")
        #f.write(f"{cv6.get()}")
        #f.write(" ")
        f.close()

        
        

        os.mkdir(location+"\\images\\"+Name_label.get())

        #shutil.move(Name_label.get()+".txt", location+"\\"+Name_label.get())
        #shutil.move(Name_label.get()+".txt",location+"\\CONFIG")
        """Video Part"""
        shutil.move(filename, location)
        msg = messagebox.showinfo("Update", "The Profile Submission is completed!")

        #os.system('python '+location+"\\images\\"+Name_label.get()+"\\"+"split.py")
        #os.system("python split.py")
        vidcap = vc('video.mp4')
        success,image = vidcap.read()
        count = 0
        success = True
        print("loaded!")
        while success:
            success,image = vidcap.read()
            im(location+"\\images\\"+Name_label.get()+"\\frame%d.jpg" % count, image)# save frame as JPEG file
            print('Read a new frame: ', success)
            count +=1
        else:
            pass
        os.remove(location+"\\images\\"+Name_label.get()+"\\frame{}.jpg".format(count-1))
        msg = messagebox.showinfo("Update", "Split Complete")
        print(len(fnmatch.filter(os.listdir(location+"\\images\\"+Name_label.get()), '*.jpg')))
        return None
        #for i in range()
        #try:
            #shutil.move("video.mp4", filename)
        #except:
            #print("video was copied!")
        #os.remove("video.mp4")
        #except:
            #print("Some Error Occoured!")
        

    def __init__(self, parent, controller):
        global Name_label, Age_label, pass_label
        global cv1, cv2, cv3, cv4, cv5, cv6
        global rgb_v
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="This is page 1").grid(row=0,column=1)
        # label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="<--------",
                           command=lambda: controller.show_frame("StartPage")).grid(row=0, column=2)
        """Main"""
        label = tk.Label(self, text="Enter Details!", font=controller.title_font).grid(row=1, columnspan=3)

        name = tk.Label(self, text="Name").grid(row=2, padx=5, pady=5, ipadx=5, ipady=5)

        age = tk.Label(self, text="Age").grid(row=3, padx=5, pady=5, ipadx=5, ipady=5)

        Gender = tk.Label(self, text="Gender").grid(row=4, padx=5, pady=5, ipadx=5, ipady=5)

        Name_label = tk.Entry(self)
        Age_label = tk.Entry(self)
        Name_label.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        Age_label.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        reg1 = self.register(Create.forName)
        Name_label.config(validate="key",validatecommand=(reg1,"%S"))

        reg2 = self.register(Create.forAge)
        Age_label.config(validate="key", validatecommand=(reg2,"%P"))
    
        password = tk.Label(self, text="Password").grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        pass_label = tk.Entry(self)
        pass_label.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        cv1 = IntVar()
        male = tk.Radiobutton(self, text="Male", variable=cv1, value=1)
        female = tk.Radiobutton(self, text="Female", variable=cv1, value=0)
        male.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        female.grid(row=5, column=2, padx=5, pady=5, ipadx=5, ipady=5)

        buttonWidget = tk.Button(self, text="Select the Video", command=Create.path).grid(row=6, columnspan=3, padx=5,
                                                                                           pady=6, ipadx=5, ipady=5)

        show_path = tk.Button(self, text="View the path of the Video", command=Create.show_message).grid(row=7,
                                                                                                          columnspan=3,
                                                                                                          padx=5,
                                                                                                          pady=5,
                                                                                                          ipadx=5,
                                                                                                          ipady=5)

        hr = tk.Label(self, text="-----------------------------------------------------------------------").grid(row=8,
                                                                                                                 padx=5,
                                                                                                                 pady=5,
                                                                                                                 ipadx=5,
                                                                                                                 ipady=5,
                                                                                                                 columnspan=3)

        device_details_label = tk.Label(self, text="Device Details!", font=controller.title_font).grid(row=9,
                                                                                                       columnspan=3)

        AC = tk.Label(self, text="A.C.").grid(row=10, padx=5, pady=5, ipadx=5, ipady=5)
        cv2 = IntVar()
        ac1 = tk.Radiobutton(self, text="OFF", variable=cv2, value=0).grid(row=10, column=1)
        ac2 = tk.Radiobutton(self, text="ON", variable=cv2, value=1).grid(row=10, column=2)

        Fan = tk.Label(self, text="FAN").grid(row=11, padx=5, pady=5, ipadx=5, ipady=5)
        cv3 = IntVar()
        fan1 = tk.Radiobutton(self, text="OFF", variable=cv3, value=0).grid(row=11, column=1)
        fan2 = tk.Radiobutton(self, text="ON", variable=cv3, value=1).grid(row=11, column=2)

        lg1 = tk.Label(self, text="Light1").grid(row=12, padx=5, pady=5, ipadx=5, ipady=5)
        cv4 = IntVar()
        lg1_1 = tk.Radiobutton(self, text="OFF", variable=cv4, value=0).grid(row=12, column=1)
        lg1_2 = tk.Radiobutton(self, text="ON", variable=cv4, value=1).grid(row=12, column=2)

        lg2 = tk.Label(self, text="Light2").grid(row=13, padx=5, pady=5, ipadx=5, ipady=5)
        cv5 = IntVar()
        lg2_1 = tk.Radiobutton(self, text="OFF", variable=cv5, value=0).grid(row=13, column=1)
        lg2_2 = tk.Radiobutton(self, text="ON", variable=cv5, value=1).grid(row=13, column=2)

        """rgb = tk.Label(self, text="RGB").grid(row=14, padx=5, pady=5, ipadx=5, ipady=5)
        cv6 = IntVar()
        lg2_1 = tk.Checkbutton(self, text="OFF", variable=cv6, onvalue=0, offvalue=1).grid(row=14, column=1)
        rgb_v = tk.Entry(self).grid(row=14, column=2, padx=5, pady=5, ipadx=5, ipady=5)"""

        buttonWidget = tk.Button(self, text="Submit!!!!",
                                 font=controller.title_font,
                                 command=Create.checkEntry).grid(row=15, columnspan=3, padx=5,pady=5, ipadx=5, ipady=5)

class Read(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="List of Users", font=controller.title_font)
        label2 = tk.Label(self,text="Restart the Apllication to update the list")
        label.pack(side="top", fill="x", pady=10)
        label2.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="<--------",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side = TOP)
        scrollbar = Scrollbar(self)
        scrollbar.pack( side = RIGHT, fill=Y )
        
        w = Label(self, text="Label: ")
        mylist = Listbox(self, yscrollcommand = scrollbar.set )
        #for line in range(100):
        #    mylist.insert(END, w.cget("text") + str(line))
        
        path = 'D:\\programming\\pytho\\CONFIG'
        global files 
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if '.txt' in file:
                    #files.append(os.path.join(r, file))
                    files.append(file)
                    x = file.replace(".txt","")
                    #print(x)
                    mylist.insert(END,x)
        mylist.pack( side = LEFT,expand = YES, fill = BOTH )
        scrollbar.config( command = mylist.yview )

class Update(tk.Frame):

    def checkEntry():
        flag=0
        print(*files)
        print(Name_label2.get()+".txt")
        #print("details "+Name_label2.get(),Age_label2.get(),pass_label2.get())
        if(Name_label2.get() and Age_label2.get() and pass_label2.get()):
            for name in files:
                if(Name_label2.get()+".txt"==name):
                    flag=1
                else:
                    flag=0
            if(flag==1):
                Update.updateo()
            else:
                msg = messagebox.showinfo("Error", "No user found with this name")
        else:
            msg = messagebox.showinfo("Error", "Please fill all the correct information")

    def forName(inp):
        if inp in "abcdefghijklmnopqrstuvwxyz":
            return True
        else:
            return False
        
    def forAge(inp):
        if inp.isdigit():
            #if inp>=100:
            return True
        #elif inp is " ":
            #return True
        else:
            return False

    def updateo():
        try:
            
            config_file = open(("D:\\programming\\pytho\\CONFIG\\"+Name_label2.get()+".txt").lower(), "r")
            contents = config_file.read()
            config_file.close()
            data = contents.split()
            #print(*data)
            if(data[2]==pass_label2.get()):
                #print(f"{data[2]} password match {pass_label2.get()}" )
                f = open(("D:\\programming\\pytho\\CONFIG\\"+Name_label2.get()+".txt").lower(), "w+")
                f.write(Name_label2.get())
                f.write(" ")
                f.write(Age_label2.get())
                f.write(" ")
                f.write(pass_label2.get())
                f.write(" ")
                #f.write(f"{data[3]}")
                #f.write(" ")
                f.write(f"{cv22.get()}")
                f.write(" ")
                f.write(f"{cv32.get()}")
                f.write(" ")
                f.write(f"{cv42.get()}")
                f.write(" ")
                f.write(f"{cv52.get()}")
                f.write(" ")
                #f.write(f"{cv6.get()}")
                #f.write(" ")
                f.close()
                msg = messagebox.showinfo("Update", "Profile Updated!")
        except:
            print("Some Error Occured!")

    def __init__(self, parent, controller):
        global Name_label2, Age_label2, pass_label2
        global cv12, cv22, cv32, cv42, cv52, cv62
        global rgb_v2
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="This is page 1").grid(row=0,column=1)
        # label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="<--------",
                           command=lambda: controller.show_frame("StartPage")).grid(row=0, column=2)
        """Main"""
        label = tk.Label(self, text="Update Details!", font=controller.title_font).grid(row=1, columnspan=3)

        name = tk.Label(self, text="Name").grid(row=2, padx=5, pady=5, ipadx=5, ipady=5)

        age = tk.Label(self, text="Age").grid(row=3, padx=5, pady=5, ipadx=5, ipady=5)

        Gender = tk.Label(self, text="Gender").grid(row=4, padx=5, pady=5, ipadx=5, ipady=5)

        Name_label2 = tk.Entry(self)
        Age_label2 = tk.Entry(self)
        Name_label2.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        Age_label2.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        reg11 = self.register(Update.forName)
        Name_label2.config(validate="key",validatecommand=(reg11,"%S"))

        reg22 = self.register(Update.forAge)
        Age_label2.config(validate="key", validatecommand=(reg22,"%P"))

        password = tk.Label(self, text="Password").grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        pass_label2 = tk.Entry(self)
        pass_label2.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        hr = tk.Label(self, text="-----------------------------------------------------------------------").grid(row=8,
                                                                                                                 padx=5,
                                                                                                                 pady=5,
                                                                                                                 ipadx=5,
                                                                                                                 ipady=5,
                                                                                                                 columnspan=3)

        device_details_label = tk.Label(self, text="Device Details!", font=controller.title_font).grid(row=9,
                                                                                                       columnspan=3)

        AC = tk.Label(self, text="A.C.").grid(row=10, padx=5, pady=5, ipadx=5, ipady=5)
        cv22 = IntVar()
        ac1 = tk.Radiobutton(self, text="OFF", variable=cv22, value=0).grid(row=10, column=1)
        ac2 = tk.Radiobutton(self, text="ON", variable=cv22, value=1).grid(row=10, column=2)

        Fan = tk.Label(self, text="FAN").grid(row=11, padx=5, pady=5, ipadx=5, ipady=5)
        cv32 = IntVar()
        fan1 = tk.Radiobutton(self, text="OFF", variable=cv32, value=0).grid(row=11, column=1)
        fan2 = tk.Radiobutton(self, text="ON", variable=cv32, value=1).grid(row=11, column=2)

        lg1 = tk.Label(self, text="Light1").grid(row=12, padx=5, pady=5, ipadx=5, ipady=5)
        cv42 = IntVar()
        lg1_1 = tk.Radiobutton(self, text="OFF", variable=cv42, value=0).grid(row=12, column=1)
        lg1_2 = tk.Radiobutton(self, text="ON", variable=cv42, value=1).grid(row=12, column=2)

        lg2 = tk.Label(self, text="Light2").grid(row=13, padx=5, pady=5, ipadx=5, ipady=5)
        cv52 = IntVar()
        lg2_1 = tk.Radiobutton(self, text="OFF", variable=cv52, value=0).grid(row=13, column=1)
        lg2_2 = tk.Radiobutton(self, text="ON", variable=cv52, value=1).grid(row=13, column=2)

        """rgb = tk.Label(self, text="RGB").grid(row=14, padx=5, pady=5, ipadx=5, ipady=5)
        cv62 = IntVar()
        lg2_1 = tk.Checkbutton(self, text="OFF", variable=cv6, onvalue=0, offvalue=1).grid(row=14, column=1)
        rgb_v2 = tk.Entry(self).grid(row=14, column=2, padx=5, pady=5, ipadx=5, ipady=5)"""

        buttonWidget = tk.Button(self, text="Update!!!!",
                                 font=controller.title_font,
                                 command=Update.checkEntry).grid(row=15, columnspan=3, padx=5,pady=5, ipadx=5, ipady=5)




class Delete(tk.Frame):

    def deleto():
        try:
            path = 'D:\\programming\\pytho\\CONFIG'
            files = []
            for r, d, f in os.walk(path):
                for file in f:
                    if '.txt' in file:
                        x = file.replace(".txt","")
                        files.append(x.lower())
            for i in files:
                if(i==name.get() and passw.get()=="admin"):
                    msg = messagebox.askquestion("Update", "Are you sure you want to delete the profile?")
                    if msg=="yes":
                        os.remove("D:\\programming\\pytho\\CONFIG\\"+name.get()+".txt")
                        shutil.rmtree("D:\\programming\\pytho\\images\\"+name.get())
                        msg = messagebox.showinfo("Update", "Profile Removed!")
            #exit()
        except:
            print("Some Eerror Occured!")

        
    def __init__(self, parent, controller):
        global name, passw
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="<--------",
                           command=lambda: controller.show_frame("StartPage")).grid(row=0, columnspan=3)
        label = tk.Label(self, text="Delete Profile", font=controller.title_font).grid(row=1, columnspan=3)
        label2 = tk.Label(self,text="Enter Name",font=controller.title_font).grid(row=2,column=0, padx=5, pady=5, ipadx=5, ipady=5)
        label3 = tk.Label(self,text="Enter Root pass",font=controller.title_font).grid(row=3,column=0, padx=5, pady=5, ipadx=5, ipady=5)
        name = tk.Entry(self)
        name.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=5)
        passw = tk.Entry(self)
        passw.grid(row=3, column=2, padx=5, pady=5, ipadx=5, ipady=5)
        submit_button = tk.Button(self, text="Delete",font=controller.title_font,
                           command=Delete.deleto).grid(row=4, columnspan=3)
        
       

class Train(tk.Frame):

    def recognizer():
        #try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR,"D:\\programming\\pytho\\images")
        #print(help(CC))
        face_cascade1 = CC('cascades\\data\\haarcascade_frontalface_alt2.xml')
        recognizer = f1.LBPHFaceRecognizer_create()
        current_id = 0
        label_ids = {}
        x_train = []
        y_labels = []

        for root,dirs,files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG") or file.endswith("jpeg"):
                    path = os.path.join(root,file)
                    label = os.path.basename(root).replace(" ","-").lower()
                    #print(label,path)
                    if not label in label_ids:
                        label_ids[label] = current_id
                        current_id+=1
                    id_ = label_ids[label]
                    print(label_ids)
                    #y_labels.append(label)#some number
                    #x_train.append(path)#verify image and turn in numpy array with gray
                    pil_image = i1.open(path).convert("L") #grayscale
                    size = (350,350)
                    final_image = pil_image.resize(size, i1.ANTIALIAS)
                    image_array = np.array(final_image, "uint8")
                    #print(image_array)
                    faces = face_cascade1.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                    for(x,y,w,h) in faces:
                        roi = image_array[y:y+h,x:x+w]
                        x_train.append(roi)
                        y_labels.append(id_)

        #print(y_labels)
        #print(x_train)

        with open("labels.pickle","wb") as f:
            pickle.dump(label_ids,f)

        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("trainner.yml")
        print("Training Complete")
        #except:
            #print("\nSome Error Occured!")
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 4", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="<--------",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        button2 = tk.Button(self, text="Run the Trainer", font=controller.title_font,
                           command=Train.recognizer)
        button2.pack()

if __name__ == "__main__":
    app = Interfacer()
    app.mainloop()
