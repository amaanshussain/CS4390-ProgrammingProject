
from objects.DataLink import DataLink
from objects.Network import Network
from objects.Transport import Transport


class Node:
    def __init__(self, id, dest, message, starttime, neighbors) -> None:
        self.id = id
        self.dest = dest
        self.message = message
        self.starttime = starttime
        self.neighbors = neighbors

        # intialize layers
        self.d = DataLink(id)
        self.n = Network(id, neighbors)
        self.t = Transport(message, id, dest)

        self.t.network = self.n

        self.n.datalink = self.d
        self.n.transport = self.t

        self.d.n = self.n


    def send_message(self):
        self.t.transport_send()

    
    def get_messages(self):

        self.d.datalink_receive_from_channel()
    

    def output_messages(self):
        self.t.transport_output_all_received()