import helper

def importEDL(path):
    #returns each line and the path to the origional edl
    #Sets up data to be read by EDL class form .edl file
    file = open(path, 'r')
    data = []
    for line in file.readlines():
        if line != '\n':
            data.append(line)

    file.close()
    return data, path

def createEDLData(data):
    timeline = data[0]
    title = data[0][0].split(':')[1][1:]
    edit = []

    for i in range(int(len(data[0])/2)):
        temp = []
        clip = timeline[i*2+1].split()
        
        globalStart = helper.TimeCodeToFrames(clip[6])
        clipStart = helper.TimeCodeToFrames(clip[4])
        duration = helper.TimeCodeToFrames(clip[5]) - helper.TimeCodeToFrames(clip[4])
        name = timeline[i*2+2].split(':')[1].lstrip()

        temp.append(globalStart)
        temp.append(clipStart)
        temp.append(duration)
        temp.append(name)

        edit.append(temp)
    
    return edit, title


if __name__ == '__main__':
    data = importEDL("C:/Users/Tom/Documents/EDL_reader/testEDL.edl")
    createEDLData(data)
