class VideoObject(object):
    def __init__(self, video_name, sample_rate):
        self.video_name = video_name 
        self.resource_cost = dict()
        self.resource_cost['time_consumption']=None
        self.resource_cost['FPS']=None

        self.info_amount=dict()
        self.info_amount['video_length'] = None
        self.info_amount['target_num'] = None 
        self.info_amount['score'] = None # fingerprints / pred_groundtruth
        self.sample_rate = sample_rate

        self.analytic_result=dict()
        self.analytic_result['object_position']=[]
        self.totalFrames = 0

        self.success_flag = False
    

