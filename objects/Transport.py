
from objects.Message import DataMessage, NegativeAcknowledgement

class Transport:
    def __init__(self, message: str, src: int, dest: int) -> None:
        self.message = message
        self.src = src
        self.datamessages: list[DataMessage] = []
        self.seqno = 0
        self.split_message(src, dest)

        self.received_messages = {}


        # layers
        self.network = None


    # split messages into different DataMessage packets
    def split_message(self, src, dest):
        pos = 0
        while pos < len(self.message):

            dm = DataMessage(src, dest, self.seqno, self.message[pos:pos+5])
            self.datamessages.append(dm)
            pos += 5
            self.seqno += 1
    
    # send packets to network
    def transport_send(self):
        for dm in self.datamessages:
            self.network.network_receive_from_transport(dm.get_message(), dm.dest)

    # receive packet from network
    def transport_receive_from_network(self, message, src):

        if message[0] == 'D':
            dm = DataMessage(int(message[1]), int(message[2]), int(message[3:5]), message[5:])

            try:
                for item in self.received_messages[src]:
                    if int(message[3:5]) == item.seqno:
                        return
            except:
                self.received_messages[src] = []
            
            self.received_messages[src].append(dm)
        
        if message[0] == 'N':
            print(message, src)
    
    def transport_output_all_received(self):


        keys = self.received_messages.keys()
        for key in keys:
            message = ""
            for index, object in enumerate(self.received_messages[key]):
                snippet = object.data
                if len(snippet) != 5 and index != len(self.received_messages[key]) - 1:
                    snippet += " "
                message += snippet
            
            print(f'From {key}, {self.src} received: ' + message)
            if message == "":
                continue
            file = open(f'output/node{self.src}received.txt', 'a+')
            file.write(f'From {key} received: ' + message + '\n')
            file.close()
