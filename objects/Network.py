from objects.Message import DataMessage, NetworkDataMessage, RoutingMessage
from collections import deque

class Network:

    def __init__(self, id, neighbors) -> None:
        self.id = id

        self.neighbors: list[int] = neighbors
        self.routingseqno = 0
        self.nodeneighbors = {}
        self.routes = {}

        self.datalink = None
        self.transport = None


    def shortest_paths(self, graph, start):
        shortest_paths_dict = {}

        # Queue for BFS traversal
        queue = deque()
        queue.append((start, [start]))  # (node, path)

        while queue:
            node, path = queue.popleft()

            if node not in shortest_paths_dict:
                shortest_paths_dict[node] = path

                if node in graph:
                    neighbors = graph[node]
                    for neighbor in neighbors:
                        queue.append((neighbor, path + [neighbor]))

        return shortest_paths_dict
    
    def link_state_routing(self):
        paths = self.shortest_paths(self.nodeneighbors, self.id)
        if self.routes != paths:
            print(f'new routing discovered for node {self.id}: ' + str(paths))
        self.routes = paths

    # packages message and sends to datalink
    def network_receive_from_transport(self, message, dest):

        dm = NetworkDataMessage(dest, message)
        datalinkmessage = ''.join(' ' for _ in range(15 - len(dm.get_message())))
        datalinkmessage += dm.get_message()

        sendto = self.routes[dest][1]

        print(f'sending to {dest} via {sendto}')
        self.datalink.datalink_receive_from_network(datalinkmessage, sendto)

    
    # reads message from datalink and sends to transport
    def network_receive_from_datalink(self, message: str, neighbor):
        parsedmessage = message[2:-2].strip()

        # if data message
        if parsedmessage[0] == 'D':
            src = int(parsedmessage[5])
            dest = int(parsedmessage[1])
            length = int(parsedmessage[2:4])
            data = parsedmessage[4:4+length]

            if dest == self.id:
                print(f'received data from {src}: {data}')
                self.transport.transport_receive_from_network(data, src)
            else:
                # find next node to send to
                sendto = self.routes[dest][1]

                print(f'sending to {dest} via {sendto}')
                self.datalink.datalink_receive_from_network(message[2:-2], sendto)
        
        # if negative acknowledgement
        if parsedmessage[0] == 'N':
            print(parsedmessage)
            self.transport.transport_receive_from_network(parsedmessage, neighbor)

        # if link state message
        if parsedmessage[0] == 'L':
            src = int(parsedmessage[1])
            seqno = int(parsedmessage[2:4])
            neighborsString = parsedmessage[4:]
            try:
                neighbors = [int(neighbor) for neighbor in neighborsString]
            except:
                neighbors = []
            self.nodeneighbors[src] = neighbors

            # send to all neighbors except self
            for neighbor in self.neighbors:
                if neighbor == self.id:
                    continue
                self.datalink.datalink_receive_from_network(message[2:-2], neighbor)

    def generate_link_state_packet(self):
        liveneighbors = self.neighbors.copy()

        for neighbor in self.neighbors:
            with open(f"./channels/from{neighbor}to{self.id}.txt", 'r') as channelFile:
                if channelFile.read() == "":
                    liveneighbors.remove(neighbor)
                    continue
            channelFile.close()
        
        
        for neighbor in self.neighbors:

            rm = RoutingMessage(self.id, self.routingseqno, liveneighbors)
            packet = ''.join(' ' for _ in range(15 - len(rm.get_packet())))
            packet += rm.get_packet()
            self.datalink.datalink_receive_from_network(packet, neighbor)
        
        self.routingseqno += 1
        self.routingseqno = self.routingseqno % 100
            
