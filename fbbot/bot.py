from fbchat import Client, log

from fbchat.models import *

class Jarvis(Client):
        def onMessage(self, author_id=None,messaege_object=None,thread_id=None, thread_type=ThreadType.USER,**kwargs):
            self.markAsRead(author_id)
            log.info("Message {} from {} in {}".format(messaege_object,thread_id,thread_type))
            msgText=messaege_object.msgText
            reply ='Hello world'
            if author_id!=self.uid:
                self.send(Message(text=reply, thread_id=thread_id,thread_type=thread_type))
            self.markAsDelivered(author_id,thread_id)

client= Jarvis("ionescugeorge492@yahoo.ro","HackTheBurgh123")
client.listen()