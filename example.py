import resource_monitor
import transformer

monitor = resource_monitor.resource_monitor(20)
transformer = transformer.transformer(monitor)

transformer.bootstrap('/mnt/SmartPoleVideo/LiteOn_Videos/LiteOn_P1/LiteOn_P1_2019-05-27_09:45:01.mp4')
monitor.predict()
monitor.plot()