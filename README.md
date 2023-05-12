# CS4390 Programming Project

This project is a python-based program which simulates communication between different nodes in
a network. The entire project is done through native python (no external packages needed) and
is designed to send and receive messages through channels in the form of a text file. Throughout
the development of this project, I utilized the cs1.utdallas.edu server to manage my project and 
test my output. 


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



