import cv2
from datetime import datetime
import os


def frame_to_video(renders, path="root", video_format='mp4'):
    height, width, layers = renders[0].shape
    unique_id = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

    if video_format == 'avi':
        video_name = unique_id + ".avi"
        fourcc = 0

    if video_format == 'mp4':
        video_name = unique_id + ".mp4"
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    if path != "root":
        if not os.path.exists(path):
            os.makedirs(path)
        video_name = os.path.join(path, video_name)

    video = cv2.VideoWriter(video_name, fourcc=fourcc, fps=10, frameSize=(width, height))

    for frame in renders:
        video.write(frame)
    cv2.destroyAllWindows()
    video.release()
