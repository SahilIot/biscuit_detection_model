from ultralytics import YOLO
import cv2
from config import MODEL_PATH,VIDEO_PATH

CONFIDENCE=0.30
LINE_Y=100

model=YOLO(MODEL_PATH)
print("Model Loaded Successfully")
cap=cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: Could not open video")
    exit()
print("Video Loaded Successfully")

total_biscuits=0
count_ids=set()
prev_pos={}

while True:
    ret,frame =cap.read()
    if not ret:
        break

    results=model.track(frame,conf=CONFIDENCE
                        , persist=True,
                        tracker="bytetrack.yaml",
                        verbose=False)
    result=results[0]
    annotated_frame=result.plot()
    if result.boxes is not None and result.boxes.id is not None:
        boxes=result.boxes.xyxy.cpu().numpy()
        track_ids = result.boxes.id.cpu().numpy().astype(int)

        for box , track_id in zip(boxes,track_ids):
            x1,y1,x2,y2=box

            center_x=int((x1+x2)/2)
            center_y=int((y1+y2)/2)

            prev_y=prev_pos.get(track_id)

            if prev_y is not None:

                if prev_y > LINE_Y >= center_y:
                    if track_id not in count_ids:
                        total_biscuits+=1
                        count_ids.add(track_id)
                        print(f"Biscuit counted ! ID:{track_id} total: {total_biscuits}")

            prev_pos[track_id]=center_y
            cv2.putText(annotated_frame,
                        f"ID: {track_id}",
                        (int(x1),int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255,0,0),
                        2)

    cv2.line(annotated_frame,
             (0,LINE_Y),
             (frame.shape[1],LINE_Y),
             (0,0,255),
             3)
    cv2.putText(annotated_frame,
                "Counting Line",
                (20,LINE_Y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,0,255),
                2)
    cv2.putText(annotated_frame,
                f"Total Biscuits: {total_biscuits}",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0,255,0),
                3)
    cv2.imshow("Biscuits Counting",
               annotated_frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
           break

cap.release()
cv2.destroyAllWindows()
print("*",*50)
print(f"TOTAL BISCUITS : {total_biscuits}")
print("*",*50)