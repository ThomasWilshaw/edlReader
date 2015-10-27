#TODO:
#Clean EDL
#Recognise EDL features
#

import helper, os, sys, getopt
import edl as edlImp



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

class Shot(object):

    def __init__(self, shotData):
        self.shotData = shotData

    def getAllData(self):
        return self.shotData

    def getGlobalStart(self):
        return self.shotData[0]

    def getClipStart(self):
        return self.shotData[1]

    def getDuration(self):
        return self.shotData[2]


    def getName(self):
        return self.shotData[3]



class EDL(object):
    data = []
    lastShot = 0

    def __init__(self, data):
        self.data = data[0] #main data
        self.path = data[1]
        self.title = data[1]
        print ("\n\n\n", data, "\n\n\n")

        self.lastShot = len(self.data)

    def getTitle(self):
        return self.title

    def getShotInfo(self, number):
        if (number > self.lastShot or number < 1): #check requested shot is within bounds
            raise ValueError('Shot %s out of bounds, max = %s, min = 1' % (number, self.lastShot))
        
        return Shot(self.data[number-1])

    def createBlenderEDL(self):
        path = str(input("\nFile path of footage: "))
        paths = getPaths(path)
        clips = []
        shotPaths = {}
        for i in range(1, self.lastShot+1):
            clip = self.getShotInfo(i).getClipName().strip("\n")
            if clip not in clips:
                clips.append(clip)

        for clip in clips:
            for path in paths:
                if path.split('\\')[-1].split('.')[0] == clip.split(".")[0]:
                    shotPaths.update({clip:path})
                    continue

        edlPath = str(self.path).strip('.edl') + '_blender.edl'
        blenderEDL = open(edlPath, 'w')
        blenderEDL.write("%-150s %8s %8s %8s %8s\n" %("PathToFile", "FileIn", "FileOut", "EditIn", "Shot"))
        for i in range(1, self.lastShot+1):
            shot = self.getShotInfo(i)
            shotPath = shotPaths[shot.getClipName()]
            blenderEDL.write("%-150s %8s %8s %8s %8d\n" %(str(shotPath)+":", str(shot.getSourceIn()['Frames'])+":", str(shot.getSourceOut()['Frames'])+":", str(shot.getEditIn()['Frames'])+":", i))

        blenderEDL.close()
        return 0



def main(argv):
    try:
      opts, args = getopt.getopt(argv,"hi:",["blender"])
    except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)

    for opt, arg in opts:
        
        if opt == '-h':
            print("EDL Tool: Does useful stuff with EDL's")
            print("Author: Tom Wilshaw")
            print("Version: 0.1")
            print('\nUsage:\tpython3 edl_reader_2.py -i <input_edl> <options>\n')
            print('Options:\n\n\t -blender: Create Blender EDL')
            
        elif opt == '-i':
            input_edl = str(arg)
            a = edlImp.importEDL(input_edl)
            edl = EDL(a)
   
        elif opt == '--blender':
            edl.createBlenderEDL()


if __name__ == "__main__":
   

   
    a = edlImp.importEDL("C:/Users/Tom/Documents/EDL_reader/testEDL.edl")
    a = edlImp.createEDLData(a)
    edl = EDL(a)
    print(edl.getTitle())
    print(edl.getShotInfo(3).getAllData())
    print(edl.getShotInfo(3).getName())
    #print(edl.createBlenderEDL())
