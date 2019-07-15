import pulsar
from pulsar import MessageId
from pulsar.schema import *

class Frame(Record):
    timestamp = String()
    img = Bytes()

class YOLOFrame(Record):
    timestamp = String()
    processed_img = Bytes()
    detections = String()

class PulsarClient:
    def __init__(self, pulsar_url, debug=False):
        self.client = pulsar.Client(pulsar_url)
        if(debug):	print("[Info] Create Client to " + pulsar_url)

    def createReader(self, input_topic):
        self.reader = self.client.create_reader(
                                topic=input_topic,  
                                start_message_id=MessageId.latest, 
                                receiver_queue_size=5000,
                                schema=AvroSchema(Frame)
                                )

    def createProducer(self,output_topic):
        self.producer = self.client.create_producer(
                topic=output_topic,
                producer_name="ycl",
                schema=AvroSchema(YOLOFrame))
