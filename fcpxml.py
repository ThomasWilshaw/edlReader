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
    formatDict = {}
    for child in resources.getchildren():
        if(child.tag == 'asset'):
            data = []
            ID = child.attrib['id']
            data.append(child.attrib['name'])
            data.append(child.attrib['src'])
            data.append(child.attrib['duration'])
            resourceDict[ID] = data
        if child.tag == 'format':
            data = []
            ID = child.attrib['id']
            data.append(child.attrib['width'])
            data.append(child.attrib['height'])
            data.append(child.attrib['frameDuration'])
            data.append(child.attrib['name'])
            formatDict[ID] = data

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

    ###get format and duration###
    timelineFormat = formatDict[sequence.attrib['format']]
    timelineDuration = helper.getSecond(sequence.attrib['duration'])

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
            start = helper.getSecond(child.attrib['start'])

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

            elif child.find('clip') is not None:
                for intChild in child:
                    temp2 = []
                    trackNum = 0
                    if intChild.tag == 'clip' and intChild.attrib['name'].split('.')[-1] in ('mov'):
                        intGlobalStart = (helper.getSecond(child.attrib['offset']))
                        clipStart = helper.getSecond(intChild.attrib['start']) - helper.getSecond(intChild.find('video').attrib['start'])
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
    return projectName, timeline, timelineFormat, timelineDuration

def createFCPXMLData(data):
    #Sets up data to be read by EDL class form .fcpxml file
    #srolls through time and always picks top shot
    ###WATCH OUT FOR FLOAT WEIRDNESS!!!####
    fps = helper.getSecond(data[2][2])
    totalTime = data[3]
    time = 0 #global time
    out = [] #datat to be returned
    running = [] #active clips
    currentClip = []
    previousClip = []
    timeline = data[1]
    lines = len(timeline)
    


    #print(data[1])
    #print(compare, top)
    while time < totalTime:
        for line in range(lines):
            for clip in timeline[line]:
                if time-0.0001 <= clip[0] <= time+0.0001: ###dodgy could do all in frames?
                    running.append([clip, line])

        #flush active clips
        for clip in running:
            if clip[0][2] + clip[0][0] <= time:
                running.remove(clip)

        #find highest current clip
        highest = 0
        for clip in running:
            if clip[1] > highest:
                highest = clip[1]

        #append clip if differnet to previous frame
        for clip in running:
            if clip[1] == highest:
                currentClip = clip   
            if currentClip != previousClip:
                previousClip = currentClip
                #print(out)
                #pass
                out.append(currentClip)     
                                
        #print(highest)
        time = time+fps

    edl = []
    edl.append(out[0][0])
    for i in range(1, len(out)):
        if out[i][0][0] == edl[i-1][0]:
            out[i][0][0] = out[i][0][0] + edl[i-1][2]
            out[i][0][2] = out[i][0][2] - edl[i-1][2] 
        
        if out[i][0][0] < edl[i-1][2] + edl[i-1][0]:
            edl[i-1][2] = out[i][0][0] - edl[i-1][0]

        edl.append(out[i][0])
            
            
    return edl

if __name__ == '__main__':
    data = importFCPXML('C:/Users/Tom/Documents/EDL_reader/DavinciTests/Afrobeats_davinci_owain.fcpxml')
    data = createFCPXMLData(data)
    for i in data:
        print('\n', i)

