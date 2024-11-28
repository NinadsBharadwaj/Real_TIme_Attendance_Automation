import tkinter as tk
from tkinter import Message, Text
import cv2, os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
# helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Attendance Management System")

dialog_title = "QUIT"
dialog_text = "Are you sure?"
# answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry("1280x720")
window.configure(background="grey")

# window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# path = "profile.jpg"

# Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
# img = ImageTk.PhotoImage(Image.open(path))

# The Label widget is a standard Tkinter widget used to display a text or image on the screen.
# panel = tk.Label(window, image = img)


# panel.pack(side = "left", fill = "y", expand = "no")

# cv_img = cv2.imread("img541.jpg")
# x, y, no_channels = cv_img.shape
# canvas = tk.Canvas(window, width = x, height =y)
# canvas.pack(side="left")
# photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
# Add a PhotoImage to the Canvas
# canvas.create_image(0, 0, image=photo, anchor=tk.NW)

# msg = Message(window, text='Hello, world!')

# Font is a tuple of (font_family, size_in_points, style_modifier_string)


message = tk.Label(
    window,
    text="Real Time Attendance Automation System",
    fg="black",
    bg="grey",
    font=("times", 30, "italic bold underline"),
)

message.place(x=200, y=20)

lbl = tk.Label(
    window,
    text="Enter ID",
    width=20,
    height=2,
    bg="grey",
    font=("times", 15, " bold "),
)
lbl.place(x=400, y=200)

txt = tk.Entry(window, width=20, bg="white", font=("times", 15, " bold "))
txt.place(x=700, y=215)

lbl2 = tk.Label(
    window,
    text="Enter Name",
    width=20,
    bg="grey",
    height=2,
    font=("times", 15, " bold "),
)
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window, width=20, bg="white", font=("times", 15, " bold "))
txt2.place(x=700, y=315)

lbl3 = tk.Label(
    window,
    text="Notification : ",
    width=20,
    bg="grey",
    height=2,
    font=("times", 15, " bold "),
)
lbl3.place(x=400, y=400)

message = tk.Label(
    window,
    text="",
    bg="grey",
    width=30,
    height=2,
    activebackground="yellow",
    font=("times", 15, " bold "),
)
message.place(x=700, y=400)

lbl3 = tk.Label(
    window,
    text="Attendance : ",
    width=20,
    bg="grey",
    height=2,
    font=("times", 15, " bold  underline"),
)
lbl3.place(x=400, y=600)


message2 = tk.Label(
    window,
    text="",
    bg="grey",
    activeforeground="green",
    width=30,
    height=2,
    font=("times", 15, " bold "),
)
message2.place(x=700, y=600)


def clear():
    txt.delete(0, "end")
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, "end")
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = txt.get()
    name = txt2.get()
    if is_number(Id) and name != "":
        cam = cv2.VideoCapture(2)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                # Saving the captured face in the dataset folder TrainingImage
                cv2.imwrite(
                    "TrainingImage/"
                    + name
                    + "."
                    + Id
                    + "."
                    + str(sampleNum)
                    + ".jpg",
                    gray[y : y + h, x : x + w],
                )
                cv2.imshow("frame", img)
            if cv2.waitKey(100) & 0xFF == ord("q"):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        file_path = "StudentDetails/StudentDetails.csv"
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a+", newline="") as csvFile:
            writer = csv.writer(csvFile)
            if not file_exists:
                writer.writerow(
                    ["Id", "Name"]
                )  # Write headers if the file is new
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if is_number(Id):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if name.isalpha():
            res = "Enter Numeric Id"
            message.configure(text=res)


def TrainImages():
    recognizer = (
        cv2.face_LBPHFaceRecognizer.create()
    )  # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert("L")
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, "uint8")
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def get_current_session():
    if not os.path.exists("session_counter.txt"):
        with open("session_counter.txt", "w") as f:
            f.write("1")  # Start with session 1 if the file doesn't exist
        return 1
    with open("session_counter.txt", "r") as f:
        return int(f.read())

# Function to update the session number in the file
def increment_session():
    current_session = get_current_session()
    with open("session_counter.txt", "w") as f:
        f.write(str(current_session + 1))
    return current_session

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Initialize the recognizer
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ["Id", "Name", "Date", "Time"]
    attendance = pd.DataFrame(columns=col_names)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for x, y, w, h in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y: y + h, x: x + w])
            if conf < 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                aa = df.loc[df["Id"] == Id]["Name"].values[0]  # Use the correct Id
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
            else:
                Id = "Unknown"
                tt = str(Id)
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)

        attendance = attendance.drop_duplicates(subset=["Id"], keep="first")
        cv2.imshow("im", im)
        if cv2.waitKey(1) == ord("q"):
            break

    # Get the session number and increment it
    session_number = increment_session()
    file_name = f"Attendance/Session {session_number}.csv"
    attendance.to_csv(file_name, index=False)

    cam.release()
    cv2.destroyAllWindows()
    res = attendance
    message2.configure(text=res)
clearButton = tk.Button(
    window,
    text="Clear",
    command=clear,
    width=5,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
clearButton.place(x=950, y=210)
clearButton2 = tk.Button(
    window,
    text="Clear",
    command=clear2,
    width=5,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
clearButton2.place(x=950, y=310)
takeImg = tk.Button(
    window,
    text="Take Images",
    command=TakeImages,
    width=10,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
takeImg.place(x=200, y=500)
trainImg = tk.Button(
    window,
    text="Train Images",
    command=TrainImages,
    width=10,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
trainImg.place(x=500, y=500)
trackImg = tk.Button(
    window,
    text="Track Images",
    command=TrackImages,
    width=10,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
trackImg.place(x=800, y=500)
quitWindow = tk.Button(
    window,
    text="Quit",
    command=window.destroy,
    width=10,
    height=1,
    activebackground="Red",
    font=("times", 15, " bold "),
)
quitWindow.place(x=1100, y=500)


window.mainloop()
