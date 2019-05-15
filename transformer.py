import ffmpeg
import numpy as np
import os

class transformer:
    crop_arr = np.zeros(10)
    trim_arr = np.zeros(10)
    
    def score(self):
        return 0
    def crop(self, file, x, y, width, height):
        (
            ffmpeg.input(file)
            .crop(x, y, width, height)
            .output('output.mp4')
            .run(overwrite_output=True)
        )
    def trim(self, file, start_frame, end_frame):
        (
            ffmpeg.input(file)
            .trim(start=start_frame, end=end_frame)
            .setpts('PTS-STARTPTS')
            .output('output.mp4')
            .run(overwrite_output=True)
        )
    def fps(self, file, fps):
        (
            ffmpeg.input(file)
            .filter('fps', fps=fps, round='up')
            .output('output.mp4')
            .run(overwrite_output=True)
        )
    def scale(self, file, scale):
        cmd = 'ffmpeg -i %s -vf "scale=iw*%1lf:ih*%1lf" -c:v libx265 -y output.mp4' %(file, scale, scale)
        os.system(cmd)
    def bitrate(self, file, bitrate):
        (
            ffmpeg.input(file) 
            .output('output.mp4', video_bitrate=bitrate)
            .run(overwrite_output=True)
        )
