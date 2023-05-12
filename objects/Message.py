

class DataMessage:
    def __init__(self, src = None, dest = None, seqno = None, data = None) -> None:
        self.src = src
        self.dest = dest
        self.seqno = seqno
        self.data = data
    
    def get_message(self):
        return 'D' + str(self.src) + str(self.dest) + str(self.seqno).zfill(2) + self.data
    
    def parse_message(self, message):
        # XX D110D0100i can50

        index = 0
        while message[index] != 'D' and message[index] != 'R':
            index += 1
        
        networkdatamessage = message[index:-2]
        len = int(networkdatamessage[2:4])
        transportdatamessage = networkdatamessage[4:4+len]

        transportsrc = int(transportdatamessage[1])
        transportdest = int(transportdatamessage[2])
        seqno = int(transportdatamessage[3:5])
        transportmessage = transportdatamessage[5:10]

        self.src = transportsrc
        self.dest = transportdest
        self.seqno = seqno
        self.data = transportmessage
    
dm = DataMessage()
dm.parse_message("XX D110D0100i can50")
print(dm.data)



class NegativeAcknowledgement:
    def __init__(self, src, dest, seqno) -> None:
        self.src = src
        self.dest = dest
        self.seqno = seqno
    
    def get_message(self):
        return 'N' + str(self.src) + str(self.dest) + str(self.seqno).zfill(2)

class NetworkDataMessage:
    def __init__(self, dest, message) -> None:
        self.dest = dest
        self.bytes = len(message)
        self.message = message
    
    def get_message(self):
        return 'D' + str(self.dest) + str(self.bytes).zfill(2) + self.message

class RoutingMessage:
    def __init__(self, id, seqno, neighbors) -> None:
        self.id = id
        self.seqno = seqno
        self.neighbors = neighbors

    def get_packet(self):
        return 'L' + str(self.id) + str(self.seqno).zfill(2) + ''.join(str(nid) for nid in self.neighbors)
