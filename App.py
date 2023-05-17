import time
import sys

from objects.Node import Node

def getArgs(args):
    try:
        id = int(args[1])
    except:
        print('Invalid process ID, try again.')
        exit(-1)

    try:
        duration = int(args[2])
    except:
        print('Invalid duration length, try again.')
        exit(-1)

    try:
        destination = int(args[3])
    except:
        print('Invalid destination ID, try again.')
        exit(-1)

    try:
        message = args[4]
    except:
        print('Invalid message, try again.')
        exit(-1)

    try:
        starttime = int(args[5])
    except:
        print('Invalid start time, try again.')
        exit(-1)

    try:
        neighbors = []
        for i in range(6,len(args)):
            neighbors.append(int(args[i]))
    except:
        print('Invalid neighbor IDs, try again.')
        exit(-1)

    return id, duration, destination, message, starttime, neighbors

def getArgsRecv(args):
    try:
        id = int(args[1])
    except:
        print('Invalid process ID, try again.')
        exit(-1)

    try:
        duration = int(args[2])
    except:
        print('Invalid duration length, try again.')
        exit(-1)

    try:
        destination = int(args[3])
    except:
        print('Invalid destination ID, try again.')
        exit(-1)
    
    try:
        neighbors = []
        for i in range(4,len(args)):
            neighbors.append(int(args[i]))
    except:
        print('Invalid neighbor IDs, try again.')
        exit(-1)
    
    return id, duration, destination, neighbors


args = sys.argv
print(args)

if int(args[1]) != int(args[3]):
    id, duration, destination, message, starttime, neighbors = getArgs(args)
else:
    id, duration, destination, neighbors = getArgsRecv(args)
    message, starttime = "", None

print('id: ' + str(id))
print('duration: ' + str(duration))
print('dest: ' + str(destination))
print('message: ' + message)
print('starttime: ' + str(starttime))
print('neighbors: ' + str(neighbors))
print("------")

# reset output files
for i in range(10):
    with open(f'./output/node{i}received.txt', 'w') as outputFile:
        outputFile.write("")
    outputFile.close()


n = Node(id, destination, message, starttime, neighbors)


currenttime = 0
while currenttime < duration:
    try:
        # insert application code here
        print(f'node {id}: ' + str(currenttime))

        if currenttime % 5 == 0:
            n.n.generate_link_state_packet()
            n.n.link_state_routing()
            print(n.n.nodeneighbors)
            print(n.n.routes)

        if starttime == currenttime and id != destination and message != "":
            print(f'node {id} sending message: {message}')
            n.send_message()
        
        n.get_messages()


        time.sleep(1)
        currenttime += 1
    except KeyboardInterrupt:
        print('\nKeyboard interrupt detected, exiting program.')
        currenttime = duration
        for x in range(10):
            with open(f'./channels/from{id}to{x}.txt', 'w') as channelFile:
                channelFile.write("")
            channelFile.close()
n.output_messages()
