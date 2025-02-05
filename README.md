# 📸 Face-Recognition-Based-Attendance-Management-System

## 📝 Overview

This project is a real-time attendance automation system using face recognition. It utilizes OpenCV for image processing, Tkinter for the GUI, and CSV for storing attendance data.

## ⚙️ Prerequisites

Ensure you have Python 3 installed on your system along with pip (Python package manager).

## 🚀 Setup Instructions

Follow these steps to set up and run the project:

## 📂 Step 1: Extract the Project

After unzipping the project, open the project directory.

## 📁 Step 2: Create Required Directories

Manually create the following empty directories inside the project folder:

  >Attendance

  >ImagesUnknown

  >TrainingImage

  >TrainingImageLabel

OR Run This command

```mkdir Attendance ImagesUnknown TrainingImage TrainingImageLabel```

## 📦 Step 3: Install Dependencies

Open a Command Prompt or Terminal in the project directory and run:

```shell
pip install -r required.txt --user 
pip install opencv-contrib-python --upgrade --user
```

## ▶️ Step 4: Run the Project

Start the program by running:
```shell
python train.py
```
## 🎯 How to Use the System

- Enter Numeric ID and Name in the respective input fields.

- Click on Take Images 📷.

- A new window will open and activate the webcam to capture images.

- The system will automatically capture images.

- If the window does not close automatically, press q to exit.

- Click on Train Images 🏋️ to train the model with the captured images.

- Click on Track Images 🎭.

- The webcam will recognize faces and display the corresponding names.

Press q to close the window.

Navigate to the Attendance 📁 folder in the project directory.

A .csv file containing attendance records (ID, Name, Date, and Time) will be generated.

## 🔢 Session Counter

The system keeps track of attendance sessions using a session counter stored in a file called session_counter.txt.

Each session is incremented automatically when a new tracking session starts.

Attendance records are stored in separate session-based CSV files, such as Session 1.csv, Session 2.csv, etc.

This ensures that attendance records are organized by session.

## 👥 Multi-Person Training and Attendance

Train multiple users by following the same steps for each individual.

While marking attendance, the system can recognize multiple faces in a single frame.

## 🛠️ Support

For any issues or improvements, feel free to raise an Issue in the repository.

💡 Happy Coding! 🚀
