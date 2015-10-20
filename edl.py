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
