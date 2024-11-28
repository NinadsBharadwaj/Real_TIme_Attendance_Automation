import tkinter as tk
from tkinter import ttk
import cv2, os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

class AttendanceManagementSystem:
    def __init__(self, master):
        self.window = master
        self.window.title("Attendance Management System")
        self.window.geometry("1280x720")
        self.window.configure(background="#f0f0f0")

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 12))
        self.style.configure('Title.TLabel', 
                             font=('Segoe UI', 24, 'bold'), 
                             foreground='#2c3e50')
        self.style.configure('TEntry', font=('Segoe UI', 12))
        self.style.configure('TButton', 
                             font=('Segoe UI', 12, 'bold'), 
                             background='#3498db', 
                             foreground='white')
        
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.configure(style='TFrame')

        # Title
        title_label = ttk.Label(main_frame, 
                                text="Real Time Attendance Automation System", 
                                style='Title.TLabel')
        title_label.pack(pady=(0, 30))

        # Input Frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        # ID Input
        id_label = ttk.Label(input_frame, text="Enter ID", style='TLabel')
        id_label.pack(side=tk.LEFT, padx=(0, 10))
        self.txt = ttk.Entry(input_frame, width=30)
        self.txt.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        clear_button = ttk.Button(input_frame, text="Clear", command=self.clear, width=10)
        clear_button.pack(side=tk.LEFT)

        # Name Input
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=10)
        name_label = ttk.Label(name_frame, text="Enter Name", style='TLabel')
        name_label.pack(side=tk.LEFT, padx=(0, 10))
        self.txt2 = ttk.Entry(name_frame, width=30)
        self.txt2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        clear_button2 = ttk.Button(name_frame, text="Clear", command=self.clear2, width=10)
        clear_button2.pack(side=tk.LEFT)

        # Notification Area
        notification_frame = ttk.Frame(main_frame)
        notification_frame.pack(fill=tk.X, pady=10)
        notification_label = ttk.Label(notification_frame, text="Notification:", style='TLabel')
        notification_label.pack(side=tk.LEFT, padx=(0, 10))
        self.message = ttk.Label(notification_frame, text="", width=50)
        self.message.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Attendance Frame
        attendance_frame = ttk.Frame(main_frame)
        attendance_frame.pack(fill=tk.X, pady=10)
        attendance_label = ttk.Label(attendance_frame, text="Attendance:", style='TLabel')
        attendance_label.pack(side=tk.LEFT, padx=(0, 10))
        self.message2 = ttk.Label(attendance_frame, text="", width=50)
        self.message2.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        buttons = [
            ("Take Images", self.TakeImages),
            ("Train Images", self.TrainImages),
            ("Track Images", self.TrackImages),
            ("Quit", self.window.destroy)
        ]

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

    def clear(self):
        self.txt.delete(0, tk.END)
        self.message.config(text="")

    def clear2(self):
        self.txt2.delete(0, tk.END)
        self.message.config(text="")

    # The rest of the methods (TakeImages, TrainImages, TrackImages, etc.) 
    # remain exactly the same as in the original code
    def is_number(self, s):
        # (Same implementation as original)
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

    def TakeImages(self):
        # (Same implementation as original)
        Id = self.txt.get()
        name = self.txt2.get()
        if self.is_number(Id) and name != "":
            # ... rest of the original TakeImages method
            cam = cv2.VideoCapture(0)
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
            file_exists = os.path.isfile(file_path)
            with open(file_path, "a+", newline="") as csvFile:
                writer = csv.writer(csvFile)
                if not file_exists:
                    writer.writerow(["Id", "Name"])
                writer.writerow(row)
            csvFile.close()
            self.message.config(text=res)
        else:
            if self.is_number(Id):
                res = "Enter Alphabetical Name"
                self.message.config(text=res)
            if name.isalpha():
                res = "Enter Numeric Id"
                self.message.config(text=res)

    def TrainImages(self):
        # (Same implementation as original)
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, Id = self.getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        res = "Image Trained"
        self.message.config(text=res)

    def getImagesAndLabels(self, path):
        # (Same implementation as original)
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert("L")
            imageNp = np.array(pilImage, "uint8")
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids

    def get_current_session(self):
        # (Same implementation as original)
        if not os.path.exists("session_counter.txt"):
            with open("session_counter.txt", "w") as f:
                f.write("1")
            return 1
        with open("session_counter.txt", "r") as f:
            return int(f.read())

    def increment_session(self):
        # (Same implementation as original)
        current_session = self.get_current_session()
        with open("session_counter.txt", "w") as f:
            f.write(str(current_session + 1))
        return current_session

    def TrackImages(self):
        # (Same implementation as original)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
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
                    aa = df.loc[df["Id"] == Id]["Name"].values[0]
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

        session_number = self.increment_session()
        file_name = f"Attendance/Session {session_number}.csv"
        attendance.to_csv(file_name, index=False)

        cam.release()
        cv2.destroyAllWindows()
        res = attendance
        self.message2.config(text=str(res))

def main():
    root = tk.Tk()
    app = AttendanceManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()