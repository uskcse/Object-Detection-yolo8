from ultralytics import YOLO
import json
import os 

def save_video(video_file_path, video_bytes):
    with open(video_file_path, "wb+") as video_file:
        video_file.write(video_bytes)

# Function to process the uploaded video
def generate_bounding_box(video_file,confidence,save):
    # Load a model
    model = YOLO('yolov8n.pt')  # load an official model
    # Predict with the model
    results = model(source=video_file, conf=confidence,save=save,exist_ok = True,project="temp",name="output")  # predict on an image
    # pickle.dump(results,open(os.path.join("temp","results.pkl"),"wb"))
    result = {}
    # res = pickle.load(open(os.path.join("temp","results.pkl"),"rb"))
    for itr,r in enumerate(results):
        result[str(itr)]=json.loads(r.tojson())
    json.dump(result,open(os.path.join("temp","final_json.json"),"w+"))
    return result