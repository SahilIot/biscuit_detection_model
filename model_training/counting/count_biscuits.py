import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config

MODEL_PATH = config.MODEL_PATH
VIDEO_PATH = config.VIDEO_PATH
CONFIDENCE = 0.50
# Maximum distance in pixels for matching a new tracker ID
# to an existing physical biscuit.
MAX_MATCH_DISTANCE = 80
# Maximum number of frames a biscuit can disappear before
# its permanent ID is removed.
MAX_MISSED_FRAMES = 15

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 +(y2 - y1) ** 2)

class BiscuitCounter:
    def __init__(self,max_match_distance=MAX_MATCH_DISTANCE, max_missed_frames=MAX_MISSED_FRAMES,):
        self.max_match_distance = max_match_distance
        self.max_missed_frames = max_missed_frames
        # Permanent biscuit ID counter.
        self.next_biscuit_id = 1
        # Total unique biscuits detected.
        self.total_biscuits = 0
        self.biscuit_objects = {}
        self.track_to_biscuit = {}
        # Current frame number.
        self.frame_number = 0

    def find_existing_biscuit(self,center,used_biscuit_ids,):
        best_id = None
        best_distance = self.max_match_distance
        for biscuit_id, data in self.biscuit_objects.items():

            if biscuit_id in used_biscuit_ids:
                continue

            if self.frame_number - data["last_seen"] > self.max_missed_frames:
                continue
            old_center = data["center"]
            distance = calculate_distance(old_center,center,)
            if distance < best_distance:
                best_distance = distance
                best_id = biscuit_id
        return best_id

    def update(self, detections):
        self.frame_number += 1
        used_biscuit_ids = set()
        processed_detections = []
        for detection in detections:
            track_id = detection["track_id"]
            center = detection["center"]

            if track_id in self.track_to_biscuit:
                biscuit_id = self.track_to_biscuit[track_id]
                if biscuit_id in self.biscuit_objects:
                    used_biscuit_ids.add(biscuit_id)
                    self.biscuit_objects[biscuit_id]["center"] = center
                    self.biscuit_objects[biscuit_id ]["last_seen"] = self.frame_number
                    self.biscuit_objects[biscuit_id]["track_id"] = track_id

                    processed = dict(detection)
                    processed["biscuit_id"] = biscuit_id
                    processed_detections.append(processed)
                    continue

            biscuit_id = self.find_existing_biscuit(center,used_biscuit_ids,)
            if biscuit_id is not None:

                self.track_to_biscuit[track_id] = biscuit_id
                used_biscuit_ids.add(biscuit_id)
                self.biscuit_objects[biscuit_id]["center"] = center
                self.biscuit_objects[biscuit_id]["last_seen"] = self.frame_number
                self.biscuit_objects[biscuit_id]["track_id"] = track_id
                processed = dict(detection)
                processed["biscuit_id"] = biscuit_id
                processed_detections.append(processed)

            else:
                biscuit_id = self.next_biscuit_id
                self.next_biscuit_id += 1
                self.total_biscuits += 1
                self.biscuit_objects[biscuit_id] = {"center": center,"last_seen": self.frame_number,"track_id": track_id,}

                self.track_to_biscuit[track_id] = biscuit_id
                used_biscuit_ids.add(biscuit_id)
                processed = dict(detection)
                processed["biscuit_id"] = biscuit_id
                processed_detections.append(processed)

        old_biscuit_ids = []
        for biscuit_id, data in self.biscuit_objects.items():
            if self.frame_number - data["last_seen"]> self.max_missed_frames:
                old_biscuit_ids.append(biscuit_id)
        for biscuit_id in old_biscuit_ids:
            del self.biscuit_objects[biscuit_id]
        return processed_detections

def run_video():
    import cv2
    from ultralytics import YOLO
    print("Loading YOLO model...")
    model = YOLO(MODEL_PATH)
    print("Model loaded successfully.")
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("ERROR: Could not open video.")
        return
    print("Video opened successfully.")
    counter = BiscuitCounter()
    frame_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break
        frame_number += 1
        results = model.track(frame,
            conf=CONFIDENCE,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False,)

        result = results[0]
        annotated_frame = frame.copy()
        detections = []

        if result.boxes is not None and result.boxes.id is not None:
            boxes = result.boxes
            track_ids = (boxes.id.int().cpu().tolist())
            confidences = (boxes.conf.cpu().tolist())
            xyxy = (boxes.xyxy.cpu().tolist())

            for track_id, confidence, box in zip(track_ids,confidences,xyxy,):
                x1, y1, x2, y2 = map(int, box)
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                detections.append( {"track_id": track_id,
                        "center": (center_x,center_y,),
                        "confidence": confidence,
                        "box": (
                            x1,y1,x2,y2,),})

        processed_detections = counter.update(detections)
        for detection in processed_detections:
            x1, y1, x2, y2 = detection["box"]
            center_x, center_y = detection["center"]
            biscuit_id = detection["biscuit_id"]
            confidence = detection["confidence"]

            cv2.rectangle(annotated_frame,
                (x1, y1), (x2, y2),
                (255, 0, 0),
                2,)
            cv2.circle(annotated_frame,
                (center_x, center_y),
                5,
                (0, 255, 0), -1,)
            label = f"ID:{biscuit_id} {confidence:.2f}"
            cv2.putText(annotated_frame,
                label,
                (x1,max(y1 - 5, 20),),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2,
            )
        cv2.putText(annotated_frame,
            f"Total Biscuits: {counter.total_biscuits}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.putText(annotated_frame,
            f"Frame: {frame_number}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(annotated_frame,
            f"Active IDs: {len(processed_detections)}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,0.7,
            (255, 255, 255),
            2,
        )
        cv2.imshow("Biscuit Counting",annotated_frame,)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    print()
    print("FINAL RESULT")
    print(f"Total unique biscuits: {counter.total_biscuits}")
if __name__ == "__main__":
    run_video()