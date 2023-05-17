from objects.Message import NegativeAcknowledgement

class DataLink:

    def __init__(self, id):
        self.NODECOUNT = 10

        self.id = id
        self.channel_data = {} # {id: [message]}

        self.n = None

    def get_id(self):
        return self.id
    
    # generate checksum for message
    def check_sum(self, message):
        # calculate message checksum
        sum = 0
        for i in range(len(message)):
            sum += ord(message[i])
        checksum = sum.__mod__(100)
        return checksum
    
    # verify message matches checksum
    def verify_message(self, message):

        # check if message start is valid
        if message[0] != "X" or message[1] != "X":
            print('invalid message')
            print(message)
            return False

        # get data from message
        data = ""
        for index, character in enumerate(message):
            if index < 2:
                continue
            data += character
                
        datamessage = data[:-2]

        # get checksum of message
        try:
            datachecksum = int(data[len(data) - 2 : len(data)])
        except:
            return False
        
        # calculate message checksum
        sum = 0
        for i in range(len(datamessage)):
            sum += ord(datamessage[i])

        checksum = sum.__mod__(100)

        # if datachecksum equals checksum, valid response
        if datachecksum == checksum:
            return message
        else:
            return False
    
    # send message to channel
    def datalink_receive_from_network(self, message, hop):

        file = './channels/from{0}to{1}.txt'.format(self.id, hop)
        with open(file, 'r+') as channel:
            datalinkmessage = 'XX' + message + str(self.check_sum(message)).zfill(2)
            data = channel.read()
            if datalinkmessage in data:
                channel.close()
                return
            
            channel.write(datalinkmessage)
        channel.close()

    # pull messages from channel
    def datalink_receive_from_channel(self):
        messages = {}
        for x in range(self.NODECOUNT):
            messages[x] = []
        
        for i in range(self.NODECOUNT):
            file = './channels/from{0}to{1}.txt'.format(i, self.id)
            with open(file, 'r') as channel:
                data = channel.read()
                if data == "":
                    channel.close()
                    continue

                # insert read counter here
                try:
                    data = data[self.channel_data[i]:]
                except:
                    data = data[0:]                

                message = ""

                for x in range(len(data)):

                    char = data[x]
                    message += char
                    if message[0] != "X":
                        message = ""
                        continue
                    if len(message) < 19:
                        continue
                    parsed = self.verify_message(message)

                    if not parsed:
                        datamessage = message[2:-2].strip()[4:]
                        nack = NegativeAcknowledgement(int(datamessage[2]), int(datamessage[1]), int(datamessage[3:5]))
                        print('corrupted message')
                        print(nack.get_message())
                        nackmessage = ''.join(' ' for _ in range(15 - len(nack.get_message()))) + nack.get_message()
                        self.datalink_receive_from_network(nackmessage, int(datamessage[1]))
                        if len(message) >= 19:
                            message = ""
                        continue
                    self.n.network_receive_from_datalink(parsed, i)

                    message = ""
                try:
                    self.channel_data[i] += len(data)
                except:
                    self.channel_data[i] = len(data)
                
            channel.close()
        return True