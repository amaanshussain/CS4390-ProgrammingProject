# CS4390 Programming Project

This project is a python-based program which simulates communication between different nodes in
a network. By utilizing a transport, network, and datalink layers, the nodes acheive a structure that can communicate with one another if there are paths in the network connecting them together. The entire project is done through native python (no external packages needed) and
is designed to send and receive messages through channels in the form of a text file. Throughout
the development of this project, I utilized the cs1.utdallas.edu server to manage my project and 
test my output. 

_Note: /src is root directory_


## Structure
The source code for the project is located in the src directory, which is where you will be executing 
the program from [note. make sure the working directory is /src otherwise relative pathnames will mess up].
The format to run the program is the same as the one described in the rubric, however, uses a python3 
execution mode instead of C/Java. All necessary files will be located in their respective folders, 
channels (housing for all possible channel outcomes), objects (class files for objects in the program), and
output (directory which houses all output that is received from a given node). The actual application to run is
App.py in the /src directory where you will start and run the program.


## Run the program
In order to run the program, you will follow the format as given in the rubric, example shown below:

sender node: 
python3 App.py [nodeID] [duration] [destination] [message] [starttime] [neighbors]

ex. python3 App.py 0 30 1 "this is my message from node 0 to 1" 20 1

receiver node: 
python3 App.py [nodeID] [duration] [nodeID] [neighbors]

ex. python3 App.py 1 30 1 0 2

I have also included a channels.py script (command to run: python3 channels.py, make sure you are in src directory) which will automatically reset the channels for different tests. In
regards to the output files, each file will be formatted on application start so there is no need to manually reset
the output.


## Demo

Assume a network consisting of 3 nodes, 0, 1, and 2. The networks are connected in a path, where 0 -- 1 -- 2. 


![Start Commands](https://media.discordapp.net/attachments/1103056330329169951/1108535211228135454/Screenshot_2023-05-17_at_6.15.51_PM.png?width=630&height=488)

Here we launch the network by starting multiple nodes, each with different IDs. Node 0 is a sender (denoted with different ID and destination) and Nodes 1 and 2 are receivers (denoted with same ID and destination).


![Send message](https://media.discordapp.net/attachments/1103056330329169951/1108535211500769340/Screenshot_2023-05-17_at_6.20.14_PM.png?width=537&height=488)

At the given starttime, the node will send the given message through the network by finding the shortest path to take between the source and destination. The node routes through link-state routing which sends routing packets to all nodes in the network to generate a routing table. Once the optimal route is found, the node will send the message in individual data packets to be read by the datalink layer of the receiver. Once received, the receiving node will parse the message, check whether the message it for itself or another node. If the destination is itself, it will send the message to the transport layer, otherwise will send back to datalink to send to the next best hop to reach its destination.


![01Channel](https://media.discordapp.net/attachments/1103056330329169951/1108535211794366464/Screenshot_2023-05-17_at_6.21.30_PM.png?width=955&height=94)
![12Channel](https://media.discordapp.net/attachments/1103056330329169951/1108535212121526404/Screenshot_2023-05-17_at_6.21.45_PM.png?width=955&height=91)

The channels above are the result of node 0 trying to message node 2 in our network (more channels altered, only showing important channels). As stated above, the nodes send routing packets, denoted with 'L', and data packets, denoted with 'D', to initialize a network and send data throughout the network.

