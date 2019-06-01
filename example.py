import resource_monitor
import transformer

monitor = resource_monitor.resource_monitor(10)
transformer = transformer.transformer(monitor)

transformer.bootstrap('LiteOn_P8_2019-05-29_12:09:54.mp4')
monitor.predict(adaption_type='spatial', data='size')
monitor.plot(adaption_type='spatial', data='size')
monitor.predict(adaption_type='spatial', data='time')
monitor.plot(adaption_type='spatial', data='time')
monitor.predict(adaption_type='temporal', data='time')
monitor.plot(adaption_type='temporal', data='time')
monitor.predict(adaption_type='temporal', data='size')
monitor.plot(adaption_type='temporal', data='size')
monitor.predict(adaption_type='bitrate', data='time')
monitor.plot(adaption_type='bitrate', data='time')
monitor.predict(adaption_type='bitrate', data='size')
monitor.plot(adaption_type='bitrate', data='size')

return 0