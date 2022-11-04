import cv2
from datetime import datetime


def frame_to_video(renders):
    height, width, layers = renders[0].shape
    unique_id = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    video_name = unique_id + ".avi"
    video = cv2.VideoWriter(video_name, 0, fps=20, frameSize=(width, height))
    for frame in renders:
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()
