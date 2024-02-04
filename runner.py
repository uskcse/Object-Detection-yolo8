import streamlit as st
from helper import *
import json
import sys
import os
sys.path.append(".")
# classes = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

def main():
    st.title("Object Tracking Dashboard")
    st.sidebar.title("Setting")

    st.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:300px;}
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{width:300; margin-left:-300px}
        <style>""", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    confidence = st.sidebar.slider("confidence",min_value=0.0,max_value=1.0,value=0.4)
    st.sidebar.markdown("---")

    save_vid = st.sidebar.checkbox("Save video")
    # enable_gpu = st.sidebar.checkbox("Enable GPU")
    # custom_classes = st.sidebar.checkbox("Use custom classes")
    # assigned_class_id = []
    # obj_names = [classes[i] for i in range(len(classes.keys( )))]
    # if custom_classes:
    #     assigned_class = st.sidebar.multiselect("Select the custom classes",obj_names,default='person')
    #     for each in assigned_class:
    #         assigned_class_id.append(obj_names.index(each))

    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "avi"])
    demo_video_path = "data/1.mp4"
    
    if not video_file_buffer:
        video_file_buffer = open(demo_video_path,"rb").read()
    else:
        video_file_buffer = video_file_buffer.read()
    st.sidebar.text("Input Video")
    st.sidebar.video(video_file_buffer)

    st_frame = st.empty()
    # video_bytes = video_file_buffer.read()
    video_file_path = os.path.join("temp","input.mp4")
    save_video(video_file_path,video_file_buffer)
    result = None
    if st.button("deduct objects",key="dedect"):
        with st.spinner('processing a video frame by frame...'):
            result = generate_bounding_box(video_file_path,confidence=confidence,save=save_vid)
    if save_vid and os.path.exists("temp/output/input.avi"):
        result_video = open("temp/output/input.avi","rb").read()
        # st_frame.video(result_video)
        st.download_button('Download video report',result_video,file_name="result.mp4",key="vid")
    results = json.load(open(os.path.join("temp","final_json.json"),"r")) if result is not None else result
    st.download_button('Download JSON report',json.dumps(result),file_name="objects.json",key='json')
        # if st.sidebar.button("Clear Experiment"):
        #     if os.path.exists("temp"):
        #         shutil.rm("temp")

    # while (vid_cap.isOpened()):
    #     success, image = vid_cap.read()
    #     if success:
    #         # Load a model 
    #         model = YOLO('yolov8n.pt')  # load an official model
    #         # model = YOLO('path/to/best.pt')  # load a custom mode/l
    #         # Predict with the model
    #         results = model.track(source=image, conf=.5)  # predict on an image
    #         # # Plot the detected objects on the video frame
    #         res_plotted = results[0].plot()
    #         stframe.image(res_plotted,
    #                     caption='Detected Video',
    #                     channels="BGR",
    #                     use_column_width=True
    #                     )
    #         st.text(results.to_json())
    #         # pickle.dump(results,open(os.path.join("temp","results.pkl"),"wb"))
    #     else:
    #         vid_cap.release()
    #         break


if __name__ =='__main__':
    main()

    