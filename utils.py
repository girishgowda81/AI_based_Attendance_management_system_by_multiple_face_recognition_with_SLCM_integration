import os
import csv
import datetime
from deepface import DeepFace
import pandas as pd
import PIL.Image as Image
import numpy as np
import cv2
import requests
# Register a new user
# def register_face(image, name):
#     # path = f'registered_faces/{name}.jpg'
#     # image.save(path)
#     # return f"{name} registered successfully."
#     if isinstance(image, np.ndarray):
#      image = Image.fromarray(image)

#     path = f"registered_faces/{name}.jpg"
#     image.save(path)

#     return f"{name} registered successfully!"
# def register_face(image, name):
#     if isinstance(image, np.ndarray):
#         image = Image.fromarray(image.astype('uint8'))  # Ensure dtype is uint8

#     path = f"registered_faces/{name}.jpg"
#     image.save(path)
#     return f"{name} registered successfully!"
# import os
# from PIL import Image
# import numpy as np

def register_face(image, name):
    # Convert to PIL Image if it's a NumPy array
    if isinstance(image, np.ndarray):
         # Or any size your model expects

        image = Image.fromarray(image.astype('uint8'))
        image = image.resize((224, 224)) 

    # Ensure the directory exists
    save_dir = "registered_faces"
    os.makedirs(save_dir, exist_ok=True)

    path = os.path.join(save_dir, f"{name}.jpg")
    
    image.save(path)

    return f"{name} registered successfully!"



# Recognize face and mark attendance
# def recognize_and_mark(image):
#     try:
#         result = DeepFace.find(img_path=image, db_path="registered_faces", enforce_detection=False)
#         if len(result) > 0:
#             name = os.path.basename(result[0].iloc[0]["identity"]).split('.')[0]
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             save_attendance(name, timestamp)
#             return f"✅ Attendance marked for {name} at {timestamp}"
#         else:
#             return "❌ Face not recognized."
#     except:
#         return "⚠️ Error in recognition."
# def recognize_and_mark_multiple(image_path):
#     try:
#         # Step 1: Extract faces from the class image
#         faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
#         print(f"[INFO] Detected {len(faces)} face(s).")

#         recognized = []

#         # Loop through each face and match
#         for idx, face_data in enumerate(faces):
#             face_img = face_data["face"]
#             temp_path = f"temp_face_{idx}.jpg"
#             cv2.imwrite(temp_path, face_img)

#             try:
#                 result = DeepFace.find(img_path=temp_path, db_path="registered_faces", enforce_detection=False, model_name="VGG-Face")

#                 # Ensure result is valid
#                 if isinstance(result, list) and len(result) > 0 and not result[0].empty:
#                     identity = os.path.basename(result[0].iloc[0]["identity"])
#                     name = os.path.splitext(identity)[0]
#                     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#                     if save_attendance(name, timestamp):
#                         recognized.append(f"✅ {name} at {timestamp}")
#                     else:
#                         recognized.append(f"🔁 {name} already marked today.")
#                 else:
#                     recognized.append(f"❌ Face {idx+1} not recognized.")

#             except Exception as e:
#                 recognized.append(f"⚠️ Error on face {idx+1}: {str(e)}")

#             finally:
#                 os.remove(temp_path)

#         return recognized

#     except Exception as e:
#         return [f"⚠️ Recognition failed: {str(e)}"]

def recognize_and_mark_multiple(image_path, class_id):
    try:
        faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
        recognized = []

        for idx, face_data in enumerate(faces):
            face_img = face_data["face"]
            temp_path = f"temp_face_{idx}.jpg"
            cv2.imwrite(temp_path, face_img)

            try:
                result = DeepFace.find(img_path=temp_path, db_path="registered_faces", enforce_detection=False, model_name="VGG-Face")

                if isinstance(result, list) and len(result) > 0 and not result[0].empty:
                    identity = os.path.basename(result[0].iloc[0]["identity"])
                    name = os.path.splitext(identity)[0]
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    class_id = get_class_id(timestamp)
                    # Save attendance with the class identifier
                    if save_attendance(name, timestamp, class_id):
                        recognized.append(f"✅ {name} at {timestamp} for Class {class_id}")
                    else:
                        recognized.append(f"🔁 {name} already marked for Class {class_id}.")
                else:
                    recognized.append(f"❌ Face {idx+1} not recognized.")

            except Exception as e:
                recognized.append(f"⚠️ Error on face {idx+1}: {str(e)}")

            finally:
                os.remove(temp_path)

        return "\n".join(recognized)

    except Exception as e:
        return f"⚠️ Recognition failed: {str(e)}"

#Save attendance
# def save_attendance(name, timestamp):
#     with open('attendance.csv', 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([name, timestamp])
# def save_attendance(name, timestamp, class_id):
#     file_path = 'attendance.csv'

#     # Create CSV file with headers if it doesn't exist
#     if not os.path.exists(file_path):
#         with open(file_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(["Name", "Timestamp", "Class"])

#     df = pd.read_csv(file_path)

#     # Avoid duplicate for same person, class, and day
#     today = timestamp.split(" ")[0]
#     if ((df["Name"] == name) & (df["Class"] == class_id) & (df["Timestamp"].str.startswith(today))).any():
#         return False

#     with open(file_path, 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([name, timestamp, class_id])

#     return True

def save_attendance(name, timestamp, class_id):
    file_path = 'attendance.csv'

    # If the file doesn't exist or is empty, write headers
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Timestamp", "Class"])

    # Read the file safely
    df = pd.read_csv(file_path)

    # Avoid duplicate for same person, class, and day
    today = timestamp.split(" ")[0]
    if ((df["Name"] == name) & (df["Class"] == class_id) & (df["Timestamp"].str.startswith(today))).any():
        return False

    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, timestamp, class_id])
    send_to_slcm(name, timestamp, class_id)

    return True

def get_class_id(timestamp):
    hour = int(timestamp.split(" ")[1].split(":")[0])
    if 9 <= hour < 11:
        return "Class 1"
    elif 11 <= hour < 13:
        return "Class 2"
    elif 13 <= hour < 15:
        return "Class 3"
    elif 15 <= hour < 17:
        return "Class 4"
    elif 17 <= hour < 19:
        return "Class 5"
    else:
        return "Class 6"

# def save_attendance(name, timestamp):
#     file_path = 'attendance.csv'

#     # Create file if not exists and add headers
#     if not os.path.exists(file_path):
#         with open(file_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(["Name", "Timestamp"])

#     # Load CSV and check headers
#     df = pd.read_csv(file_path)

#     # Ensure columns exist
#     if "Name" not in df.columns or "Timestamp" not in df.columns:
#         df = pd.DataFrame(columns=["Name", "Timestamp"])
#         df.to_csv(file_path, index=False)

#     # Avoid duplicate for same day
#     today = timestamp.split(" ")[0]
#     if ((df["Name"] == name) & (df["Timestamp"].str.startswith(today))).any():
#         return False  # Already marked

#     with open(file_path, 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([name, timestamp])

#     return True

# https://webhook.site/b68018db-2c2f-4a52-9e07-931363d39dda


import requests

def send_to_slcm(name, timestamp, class_id):
    """
    Simulated API call to SLCM backend to mark attendance.
    Replace the URL and payload format as per actual SLCM API.
    """
    try:
        url = "https://webhook.site/b68018db-2c2f-4a52-9e07-931363d39dda"  # Replace with real SLCM URL
        payload = {
            "student_name": name,
            "attendance_time": timestamp,
            "class": class_id
        }

        response = requests.post(url, json=payload, timeout=5)

        if response.status_code == 200:
            return f"✅ Sent to SLCM for {name}"
        else:
            return f"⚠️ Failed to send to SLCM for {name}: {response.status_code}"
    except Exception as e:
        return f"❌ SLCM error: {str(e)}"

# utils.py

def login(username, password):
    """
    Simple login function.
    Replace with your actual authentication logic (e.g., database or external API).
    """
    if username == "admin" and password == "pass123":
        return True
    else:
        return False

