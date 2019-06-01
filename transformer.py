import ffmpeg
import numpy as np
import os
import time
class transformer:
    def __init__(self, monitor):
        self.monitor = monitor
    def score(self):
        return 0
    def temporal(self, file, fps):
        start_time = time.time()
        size = os.path.getsize(file)
        (
            ffmpeg.input(file)
            .filter('fps', fps=fps, round='up')
            .output('output.mp4', vcodec='libx265')
            .run(overwrite_output=True)
        )
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        self.monitor.insert('temporal', fps, execute_time, ratio)
        return (execute_time, ratio)
    def spatial(self, file, scale):
        size = os.path.getsize(file)
        start_time = time.time()
        iw = int((2048*scale)-1) if int((2048*scale)%2)==1 else int((2048*scale))
        ih = int((1536*scale)-1) if int((1536*scale)%2)==1 else int((1536*scale))
        print(iw, ih)
        cmd = 'ffmpeg -i %s -vf "scale=%d:%d" -c:v libx265 -y output.mp4 -pix_fmt yuvj422p' %(file, iw, ih)
        os.system(cmd)
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        if execute_time < 1:
            return 0
        self.monitor.insert('spatial', scale, execute_time, ratio)
        return (execute_time, ratio)
    def bitrate(self, file, bitrate):
        start_time = time.time()
        size = os.path.getsize(file)
        (
            ffmpeg.input(file) 
            .output('output.mp4', video_bitrate=bitrate, vcodec='libx265')
            .run(overwrite_output=True)
        )
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        self.monitor.insert('bitrate', bitrate, execute_time, ratio)
        return (execute_time, ratio)
    def bootstrap(self, file):
        for i in range(1, 20, 1):
            self.temporal(file, i)
        for i in np.arange(0.1, 0.95, 0.05):
            self.spatial(file, i)
        for i in range(1000000, 2000000, 200000):
            self.bitrate(file, i)