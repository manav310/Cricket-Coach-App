# Cricket Coach App

A system to analyze and enhance cricket coaching using advanced machine learning models.

---

## Getting Started

Follow the steps below to set up the project on your local machine.

---

### 1. Clone the Repository

Clone the repository using the following command:

```bash
git clone https://github.com/manav310/Cricket-Coach-App.git
```
---

### 2. Install Requirements

Navigate to the cricket_coach_app directory in the backend folder and install the required dependencies: 

```bash
pip install -r requirements.txt
```

---

### 3. Download Pre-trained Models
Download the pre-trained models from this Google Drive link: https://drive.google.com/drive/u/0/folders/1fBm8pgQee1dxrFpvOL8LmvhJ7xJ5o4PG

best_model.pth
yolov8x.pt

---

### 4. Place the Pre-trained Models
Place the best_model.pth file in the cricket_coach_app folder within the backend directory.
Place the yolov8x.pt file in the models folder within the backend directory.

---

### 5. Update utils.py
Navigate to the play_style folder inside the cricket_coach_app directory in the backend and edit the utils.py file:

Comment out line 39.
Update the path_to_model on line 40 with the path to the best_model.pth file.

---

### 6. Configure IP Address

Open your terminal and run the following command to get your IPv4 address:

ipconfig
Copy your IPv4 address.

Update the following:

i. Add your IPv4 address to the ALLOWED_HOSTS in settings.py inside the cricket_coach directory.
ii. Replace any occurrences of the previous IP address in the frontend code files with your new IPv4 address.

---

### 7. Run the Application

Generate the apk using 'flutter build apk' command in android studio.
Once all the above steps are complete, run the following commands in the backend directory:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
