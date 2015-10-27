import sys

def TimeCodeToFrames(tc):
    data = tc.split(":")
    hours = int(data[0]) * 3600 * 25
    minutes = int(data[1]) * 60 * 25
    seconds = int(data[2]) * 25
    frames = int(data[3])
    raw_frames = hours + minutes + seconds + frames
    return raw_frames

def secondsToFrames(s, fps):
    return s*fps

def isInt(s):
    #suppresses vlue errors
    try:
        int(s)
        return int(s)
    except ValueError:
        pass

def getPaths(path):
    #gets path to all mov's in folder
    paths = []
    extensions = tuple(['.mov', '.MOV'])
    for root, subFolder, files in os.walk(path):
        for item in files:
            if item.endswith(extensions):
                paths.append(str(os.path.join(root,item)))
    return paths

def getSecond(time):
    time = time.strip('s')
    data = time.split('/')
    time = float(data[0])/float(data[1])
    return time

def pad(number, digits):
    length = len(str(number))
    zeros = digits-length
    zero = '0'
    if zeros < 0:
        print('Error, to few digits to convert number: {}'.format(number))
        sys.exit()
    return zeros*zero + str(number)
        

if __name__ == "__main__":
    print(getSecond('3600/1s'))
    print(getSecond('91509/25s'))
    print(pad(99999, 5))
