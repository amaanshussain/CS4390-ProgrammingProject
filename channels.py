import os


os.chdir('./channels')
print(os.getcwd())

for i in range(10):
    for j in range(10):
        command = "rm from{1}to{2}.txt".format('', i, j)
        print(command)
        os.system(command)

for i in range(10):
    for j in range(10):
        command = "touch from{1}to{2}.txt".format('', i, j)
        print(command)
        os.system(command)