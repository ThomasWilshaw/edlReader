from lxml import etree
import helper

###TODO###
#
##########

def printXML(part):
	print(etree.tostring(part, pretty_print=True))

def importFCPXML(file):
        try:
                doc = etree.parse(file)
                print('Importing file: {}'.format(file))
                #doc = etree.parse('Afrobeats_davinci_owain.fcpxml')
                #doc = etree.parse('complex.fcpxml')
        except:
                print('Failed to load fcpxml, double check path')
                return

        ###Check fcpxml version###
        if doc.xpath('//fcpxml')[0].attrib['version'] == '1.5':
            print("At fcpxml version 1.5...")
        else:
            print("Warning, fcpxml version is  not 1.5, possible errors.")
            print("fcpxml version: {}".format(doc.xpath('//fcpxml')[0].attrib['version']))
        print('Possible errors if gaps in timeline...')
            
        ###Store files###
        #dict: id:[filename, origional_Src, duration]
        resources = doc.xpath('//resources')[0]
        resourceDict = {}
        for child in resources.getchildren():
            if(child.tag == 'asset'):
                data = []
                ID = child.attrib['id']
                data.append(child.attrib['name'])
                data.append(child.attrib['src'])
                data.append(child.attrib['duration'])
                resourceDict[ID] = data

        ###name###
        project = doc.xpath('//project')[0]
        projectName = project.attrib['name']
        print("Importing project '{}'...".format(projectName))

        ###Sequence data###
        #[format(im xml form), duration (seconds), tcStart(seconds)]
        sequence = doc.xpath('//sequence')[0]
        sequenceData = []
        for child in resources.getchildren():
            if child.tag == 'format':
                if child.attrib['id'] == sequence.attrib['format']:
                    formt = child
                    break
        sequenceData.append(formt)
        sequenceData.append(helper.getSecond(sequence.attrib['duration']))
        sequenceData.append(helper.getSecond(sequence.attrib['tcStart']))

        ###Main timeline datat collection###
        timelineData = doc.xpath('//spine')[0]
        global timeline
        #stored as: globalStart, clipStart (i.e. clip inpoint), duration, name
        #all in seconds plus timeline offset
        timeline = [[]]

            
        for child in timelineData:
            trackNum = 0
            temp1 = []
            flag = False
            if child.tag == 'clip':
                start = helper.getSecond(child.attrib['start'])
                #get IN START DURATION NAME
                globalStart = helper.getSecond(child.attrib['offset'])
                clipStart = helper.getSecond(child.attrib['start']) - helper.getSecond(child.find('video').attrib['start'])
                duration = helper.getSecond(child.attrib['duration'])
                name = child.attrib['name']
                temp1.append(globalStart)
                temp1.append(clipStart)
                temp1.append(duration)
                temp1.append(name)
                timeline[trackNum].append(temp1)#will be in first track
                flag = 'a'

            elif child.tag == 'video':
                    globalStart = helper.getSecond(child.attrib['start'])
                    clipStart = 0.0
                    duration = helper.getSecond(child.attrib['duration'])
                    name = 'Title Card'
                    temp1.append(globalStart)
                    temp1.append(clipStart)
                    temp1.append(duration)
                    temp1.append(name)
                    timeline[trackNum].append(temp1)#will be in first track
                    flag = 'b'

            elif child.tag == 'gap':
                    flag = 'b'    

            if flag == 'a':

                if child.find('clip') is not None:
                    #find clips with child clips
                    flag = False
                    for intChild in child:
                        temp2 = []
                        trackNum = 0 #have to reset trackNum each time
                        checkClip = 'BMPCC_1_2015-05-30_1130_C0003.mov'
                        if intChild.tag == 'clip':
                            if intChild.attrib['name'].split('.')[-1] in ('WAV'):
                                continue #skip WAVs
                            if(intChild.attrib['name'] == checkClip):
                                  #print(globalStart)
                                  pass

                            intGlobalStart = (helper.getSecond(intChild.attrib['offset']) - start) + globalStart
                            clipStart = helper.getSecond(intChild.attrib['start']) - helper.getSecond(intChild.find('video').attrib['start'])
                            duration = helper.getSecond(intChild.attrib['duration'])
                            name = intChild.attrib['name']
                            
                            temp2.append(intGlobalStart)
                            temp2.append(clipStart)
                            temp2.append(duration)
                            temp2.append(name)
                           
                            lane = int(intChild.attrib['lane']) #find lane number

                            trackNum = trackNum + lane
                            if(intChild.attrib['name'] == checkClip):
                                  #print(name, globalStart, start)
                                  pass
                            try: #add to correct track. Add track if doesn't exist
                                timeline[trackNum].append(temp2)
                            except:
                                n = len(timeline)-1
                                for i in range(trackNum-n):
                                    timeline.append([])
                                timeline[trackNum].append(temp2)
                                
            elif flag == 'b':
                    if child.find('title') is not None:
                            for intChild in child:
                                    temp2 = []
                                    trackNum = 0
                                    if intChild.tag == 'title':
                                            intGlobalStart = helper.getSecond(intChild.attrib['start'])
                                            clipStart = 0.0
                                            duration = helper.getSecond(intChild.attrib['duration'])
                                            name = intChild.attrib['name']
                                            temp2.append(intGlobalStart)
                                            temp2.append(clipStart)
                                            temp2.append(duration)
                                            temp2.append(name)

                                            lane = int(intChild.attrib['lane']) #find lane number

                                            trackNum = trackNum + lane

                                            try: #add to correct track. Add track if doesn't exist
                                                timeline[trackNum].append(temp2)
                                            except:
                                                n = len(timeline)-1
                                                for i in range(trackNum-n):
                                                    timeline.append([])
                                                timeline[trackNum].append(temp2)
                                            
                            
        #remove timeline offset from globalStart
        for track in timeline:
                for clip in track:
                        clip[0] = clip[0] - helper.getSecond(sequence.attrib['tcStart'])

        print('FCPXML import successful.')
        #timeline: globalStart, clipStart, duration, name
        return projectName, timeline

def createFCPXMLData():
        #Sets up data to be read by EDL class form .fcpxml file
        return

if __name__ == '__main__':
        data = importFCPXML('Afrobeats_davinci_owain.fcpxml')
