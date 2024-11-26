import cv2
import numpy as np
from roboflow import Roboflow
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Label mapping for shot type prediction
label_mapping = {
    'straight': 0,
    'cover': 1,
    'defense': 2,
    'flick': 3,
    'late_cut': 4,
    'hook': 5,
    'lofted': 6,
    'pull': 7,
    'square_cut': 8,
    'sweep': 9
}

# Reverse mapping for predictions
reverse_label_mapping = {idx: label for label, idx in label_mapping.items()}

import torch
import random
from transformers import VideoMAEForVideoClassification

# Load the trained VideoMAE model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
video_mae_model = VideoMAEForVideoClassification.from_pretrained("MCG-NJU/videomae-base")
video_mae_model.classifier = torch.nn.Sequential(
    torch.nn.Linear(video_mae_model.classifier.in_features, 512),
    torch.nn.ReLU(),
    torch.nn.Linear(512, len(label_mapping))  # Match the number of classes
)
video_mae_model.load_state_dict(torch.load('C:/Users/pahwa/Python_Projects/sports_analysis/cricket_coach/CC_App_Backend/CC_App_Backend/cricket_coach_app/best_model.pth', map_location=device))
#video_mae_model.load_state_dict(torch.load('path_to_model', map_location=device))
video_mae_model.to(device)
video_mae_model.eval()

def preprocess_video(video_path, num_frames=16, frame_size=(224, 224)):
    """
    Preprocess video for the VideoMAE model.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, frame_size)  # Resize each frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        frames.append(frame)
    cap.release()

    # Normalize pixel values and prepare the tensor
    frames = np.array(frames).astype(np.float32) / 255.0
    frames = torch.Tensor(frames).permute(0, 3, 1, 2)  # (T, H, W, C) -> (T, C, H, W)

    num_video_frames = frames.shape[0]
    if num_video_frames > num_frames:
        indices = sorted(random.sample(range(num_video_frames), num_frames))
        frames = frames[indices, :, :, :]
    elif num_video_frames < num_frames:
        padding = torch.zeros((num_frames - num_video_frames, 3, 224, 224))
        frames = torch.cat((frames, padding), dim=0)

    frames = frames.unsqueeze(0)  # Add batch dimension
    return {"pixel_values": frames.to(device)}


# def analyze_video(video_path):
#     # Initialize the analysis results dictionary
#     analysis_results = {
#         "batsman_position": {},
#         "shot_type": {},
#         "stance": {},
#         "footwork": {}
#     }

#     # Initialize Roboflow
#     rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)
#     project = rf.workspace().project("cricket-shots-wviff")
#     model = project.version(1).model

#     # Open the video file
#     cap = cv2.VideoCapture(video_path)
    
#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_count += 1
#         if frame_count % 5 != 0:  # Process every 5th frame to reduce computation
#             continue

#         # Predict on the frame
#         try:
#             predictions = model.predict(frame, confidence=40, overlap=30).json()
#             process_frame(predictions, frame, analysis_results, video_path)
#         except Exception as e:
#             logger.error(f"Error processing frame {frame_count}: {str(e)}")

#     cap.release()

#     # Process the results
#     results = {
#         "batsman_position": get_max_occurrence(analysis_results["batsman_position"]),
#         "shot_type": get_max_occurrence(analysis_results["shot_type"]),
#         "stance_analysis": analyze_stance(analysis_results["stance"]),
#         "footwork": get_max_occurrence(analysis_results["footwork"])
#     }

#     return results

def analyze_video(video_path):
    """
    Analyze video for batsman position, shot type, stance, and footwork.
    """
    # Initialize the analysis results dictionary
    analysis_results = {
        "batsman_position": {},
        "shot_type": {},
        "stance": {},
        "footwork": {}
    }

    # Initialize Roboflow
    rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)
    project = rf.workspace().project("cricket-shots-wviff")
    rf_model = project.version(1).model

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 5 != 0:  # Process every 5th frame for Roboflow
            continue

        # Predict on the frame using Roboflow
        try:
            predictions = rf_model.predict(frame, confidence=40, overlap=30).json()
            process_frame(predictions, frame, analysis_results)
        except Exception as e:
            logger.error(f"Error processing frame {frame_count}: {str(e)}")

    cap.release()

    # Add the new shot type prediction using VideoMAE
    shot_type_prediction = predict_shot_type(video_path)
    analysis_results["shot_type"]["predicted"] = shot_type_prediction

    # Process the results
    results = {
        "batsman_position": get_max_occurrence(analysis_results["batsman_position"]),
        "shot_type": shot_type_prediction,  # Use VideoMAE prediction
        "stance_analysis": analyze_stance(analysis_results["stance"]),
        "footwork": get_max_occurrence(analysis_results["footwork"])
    }

    return results


# def process_frame(predictions, frame, analysis_results):
#     if not predictions or 'predictions' not in predictions:
#         return

#     for prediction in predictions['predictions']:
#         bbox = prediction
        
#         # Analyze the frame
#         batsman_pos = batsman_position(bbox, frame.shape)
#         shot_type = shot_type_estimation(bbox)
#         stance = stance_analysis(bbox)
#         footwork = footwork_analysis(bbox, frame.shape)

#         # Update analysis results
#         update_analysis_results(analysis_results, batsman_pos, shot_type, stance, footwork)

def process_frame(predictions, frame, analysis_results):
    if not predictions or 'predictions' not in predictions:
        return

    for prediction in predictions['predictions']:
        bbox = prediction
        batsman_pos = batsman_position(bbox, frame.shape)
        stance = stance_analysis(bbox)
        footwork = footwork_analysis(bbox, frame.shape)

        # Update analysis results
        update_analysis_results(analysis_results, batsman_pos, None, stance, footwork)  # No shot type here



def batsman_position(bbox, frame_shape):
    x_center = bbox["x"] + bbox["width"] / 2
    if x_center < frame_shape[1] / 3:
        return "leg side"
    elif x_center > 2 * frame_shape[1] / 3:
        return "off side"
    else:
        return "middle"

# def shot_type_estimation(bbox):
#     bat_angle = bbox["width"] / bbox["height"]
#     return "horizontal shot (e.g., pull or sweep)" if bat_angle > 1.2 else "vertical shot (e.g., drive or push)"

def predict_shot_type(video_path):
    """
    Predict shot type for the entire video using VideoMAE.
    """
    try:
        # Preprocess the entire video
        inputs = preprocess_video(video_path)

        # Perform inference
        with torch.no_grad():
            outputs = video_mae_model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()

        # Map predicted class index to label
        predicted_label = reverse_label_mapping[predicted_class]
        return predicted_label.capitalize()
    except Exception as e:
        logger.error(f"Error predicting shot type: {str(e)}")
        return "Unknown"


def stance_analysis(bbox):
    return "unbalanced" if bbox["width"] > bbox["height"] else "balanced"

def footwork_analysis(bbox, frame_shape):
    y_center = bbox["y"] + bbox["height"] / 2
    return "aggressive" if y_center < frame_shape[0] / 2 else "defensive"

def update_analysis_results(analysis_results, batsman_pos, shot_type, stance, footwork):
    for key, value in zip(analysis_results.keys(), [batsman_pos, shot_type, stance, footwork]):
        if value in analysis_results[key]:
            analysis_results[key][value] += 1
        else:
            analysis_results[key][value] = 1

def get_max_occurrence(data_dict):
    return max(data_dict, key=data_dict.get) if data_dict else None

def analyze_stance(stance_dict):
    total_stances = sum(stance_dict.values())
    unbalanced_count = stance_dict.get("unbalanced", 0)
    
    if unbalanced_count == 0:
        return "completely balanced"
    
    unbalanced_percentage = (unbalanced_count / total_stances) * 100
    if unbalanced_percentage < 20:
        return "slightly unbalanced"
    elif 20 <= unbalanced_percentage <= 50:
        return "moderately unbalanced"
    else:
        return "unbalanced"

