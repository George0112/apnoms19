from optimal_downsampling_manager.decision_type import Analytic_Decision
from analytics.analyst import Analyst
analyst = Analyst()
analyst.set_sample_rate(30)
ad = Analytic_Decision()
ad.c = './dataSet/videos/LiteOn_P1_2019-07-14_13_34_43.mp4'
ad.f = [0,100]
ad.a = 'people_counting'

ad2 = Analytic_Decision()
ad2.c = './dataSet/videos/LiteOn_P1_2019-07-14_13_34_43.mp4'
ad2.f = [101,200]
ad2.a = 'nothing'
S_decision=[]
S_decision.append(ad)

S_decision.append(ad2)

for idx in range(len(S_decision)):
    
    if idx==0:
        analyst.set_video_clip(S_decision[0].c)
        
    else:
        if S_decision[idx].c != S_decision[idx-1].c:    
            analyst.set_video_clip(S_decision[idx].c)
    
    analyst.analyze(
                    S_decision[idx].c,
                    S_decision[idx].f[0],
                    S_decision[idx].f[1],
                    S_decision[idx].a
                )
    

