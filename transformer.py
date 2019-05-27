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
            .output('output.mp4')
            .run(overwrite_output=True)
        )
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        self.monitor.insert('temporal', fps, execute_time, ratio)
        return (execute_time, ratio)
    def spatial(self, file, scale):
        if scale < 0.25:
            raise Exception("Invalid scale ration, should be larger than 0.25")
        size = os.path.getsize(file)
        start_time = time.time()
        cmd = 'ffmpeg -i %s -vf "scale=iw*%1f:ih*%1f" -c:v libx264 -y output.mp4' %(file, scale, scale)
        os.system(cmd)
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        self.monitor.insert('spatial', scale, execute_time, ratio)
        return (execute_time, ratio)
    def bitrate(self, file, bitrate):
        start_time = time.time()
        size = os.path.getsize(file)
        (
            ffmpeg.input(file) 
            .output('output.mp4', video_bitrate=bitrate)
            .run(overwrite_output=True)
        )
        execute_time = time.time() - start_time
        ratio = os.path.getsize('output.mp4') / size
        self.monitor.insert('bitrate', bitrate, execute_time, ratio)
        return (execute_time, ratio)