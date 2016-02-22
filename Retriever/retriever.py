# retriever.py
#
#  Receives chat messages and acts on them.  If message is ‘GO’ it will go forward for 5 seconds.
#

import mraa
import time
import boto3
from boto3.session import Session



def sendRover (rover_message):

    print "Message: ", rover_message

    if rover_message == "GO" :

        roverGo.write(1);

    elif rover_message == "STOP" :

        roverGo.write(0)

    else:

        roverGo.write(0);





#  Rover Interface
roverGo = mraa.Gpio(13)
roverGo.dir(mraa.DIR_OUT)

sendRover('STOP')





session = Session( aws_access_key_id='AKIAI63546FLYAQUMQ3A',
                   aws_secret_access_key='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',
		   region_name='us-east-1')


print "Session is set.\n"
# Get the service resource
sqs = session.resource('sqs')

queue = sqs.get_queue_by_name(QueueName='chatqueue1')


# You can now access identifiers and attributes
print "Queue URL: ", queue.url
print "Queue Delay Seconds Attribute: ", queue.attributes.get('DelaySeconds')

receiver_name = raw_input ("Enter your Chat Id: ")

print "Poll for messages.\n";

while 1 :

    messages = queue.receive_messages( MessageAttributeNames = ['SenderName','ReceiverName']   )

    for message in messages:
        
        sender_name = ''

        if message.message_attributes is not None :

            if message.message_attributes.get('ReceiverName') is not None :

                if message.message_attributes.get('ReceiverName').get('StringValue') == receiver_name :
    
                    sender_name = message.message_attributes.get('SenderName').get('StringValue')

                    print sender_name, "said:  " , message.body
                    sendRover(message.body)
                    time.sleep (5)
                    sendRover('STOP')
                    message.delete()



print "Done with infinite while loop.\n";
