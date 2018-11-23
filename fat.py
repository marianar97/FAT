from math import ceil


def read(string):
    f = open(string, "r")
    byte = {}
    for line in f.readlines():
        line = line.replace("\n", "")
        line = line.strip(" ")
        lista = line.split(" ")
        if lista[0] == "*": continue

        pos = int(lista[0], 16)
        # ['0000000', 'eb', '58', '90', '42', '53', '44', '20', '20', '34', '2e', '34', '00', '02', '08', '20', '00'

        for i in range(0, len(lista) - 1):
            byte[pos] = lista[i + 1]
            pos += 1

    return byte


def info(byte):
    fatType = ""

    # JmpBoot
    jmpBoot = ""
    if (byte[0] == "eb" or byte[0] == "EB") and byte[2] == "90":
        jmpBoot = ("jmpBoot[0] = 0xEB, jmpBoot[1] = 0x" + (byte[1]).upper() + ", jmpBoot[2] = 0x90")
        print(jmpBoot)
    elif byte[0] == "e9" or byte[0] == "E9":
        jmpBoot = "jmpBoot[0] = 0xE9, jmpBoot[1] = 0x" + byte[1].upper() + ", jmpBoot[2] = 0x" + byte[2].upper()
        print(jmpBoot)
    else:
        jmpBoot = "ERROR: JmpBoot does not match"
        print(jmpBoot)

    # OEMName
    oemName = ""
    for i in range(3, 11):
        oemName += byte[i]
    oemName = bytes.fromhex(oemName).decode('latin-1')
    print("OEMName", oemName)

    # BytesPerSec
    msb = byte[12]
    lsb = byte[11]
    bytesPerSec = msb + lsb
    bytesPerSec = int(bytesPerSec, 16)
    print("BytesPerSec", bytesPerSec)
    if (bytesPerSec not in [512, 1024, 2048, 4096]):
        print("ERROR: bytesPerSec is not 512 or 1024 or 2048 or 4096")
        

    # SecPerClus
    SecPerClus = int(byte[13], 16)
    print("SecPerClus", SecPerClus)
    if SecPerClus not in [1, 2, 4, 8, 16, 32, 64, 128]:
        print("ERROR: SecPerClus is not 1 or 2 or 4 or 8 or 16 or 64 or 128")
        return 1

    '''
    PREGUNTAR
    if BytesPerCluster * bytesPerSec > (32 * 1024):
        print("ERROR: BytesPerCluster is greater than 32 K")
        return 1
    '''

    # RsvdSecCnt
    msbr = byte[15]
    lsbr = byte[14]
    rsvdSecCnt = int(msbr + lsbr, 16)
    if rsvdSecCnt == 0:
        print("ERROR: reserved sector count does not match")
        return 1
    print("RsvdSecCnt", rsvdSecCnt)

    # NumFAT
    numFAT = int(byte[16], 16)
    print("numFAT", numFAT)
    if numFAT < 1:
        print("ERROR: numFAT is less than 1")
        return 1
    elif numFAT != 2:
        print("WARNING: numFAT is different than 2, some software programs and operating system may not work properly")

    # RootEntCnt
    rootEntCnt = int(byte[18] + byte[17], 16)
    print("RootEntCnt", rootEntCnt)
    if rootEntCnt == 0:
        fatType = "FAT32"
    elif bytesPerSec % (rootEntCnt * 32) != 0:
        print("ERROR: RootEntCnt does not match")
        

    # TotalSec16
    totalSec16 = int(byte[20] + byte[19],16)
    print("totalSec16", totalSec16)

    # media
    media = byte[21]
    print("media", media)
    if media not in ["f0", "F0", "f8", "F8", "f9", "F9", "fa", "FA", "fb", "FB", "fc", "FC", "fd", "FD", "fe", "FE"]:
        print("media does not match")
        return 1

    # fatSz16
    fatSz16 = int(byte[23] + byte[22], 16)
    print("fatSz16", fatSz16)
    if fatType == "FAT32" and fatSz16 != 0:
        print("ERROR: this is a FAT32 and fatSz16 is different than 0")
        return 1

    # SecPerTrk
    secPerTrk = int(byte[25] + byte[24], 16)
    print("secPerTrk", secPerTrk)

    # NumHeads
    numHeads = int(byte[27] + byte[26], 16)
    print("NumHeads", numHeads)

    # HiddSec
    hiddSec = int(byte[31] + byte[30] + byte[29] + byte[28], 16)
    print("HiddSec", hiddSec)

    # totSec32
    totSec32 = int((byte[35] + byte[34] + byte[33] + byte[32]), 16)
    print("TotSec32", totSec32)
    if totSec32 == 0 and totalSec16 == 0:
        print("ERROR: totSec32 and totSec16 equal 0")
        return 1
    if fatType == "FAT32" and totSec32 == 0:
        print("ERROR: This is a FAT32 and totSec32 is 0")
        return 1

    fatSz32 = 0
    if fatType == "FAT32":
        fatSz32 = ""
        for i in range(39, 35, -1):
            fatSz32 += byte[i]

        fatSz32 = int(fatSz32, 16)
        print("FatSz32", fatSz32)
        if (fatSz32 != 0 and fatSz16 != 0):
            print("ERROR: both fatSz32 and fatSz16 are not zero")
            return 1

    return jmpBoot, oemName, bytesPerSec, SecPerClus, rsvdSecCnt, numFAT, rootEntCnt, totalSec16, media, fatSz16, secPerTrk, numHeads, hiddSec, totSec32, fatSz32


def structureFAT32(byte):
    # ExtFlags
    extFlags = ""
    for i in range(40, 42):
        extFlags += byte[i]
    print("ExtFlags", extFlags)

    # FSVer
    fsVer = ""
    for i in range(42, 44):
        fsVer += byte[i]
    print("FSVer", fsVer)

    # RootClus
    rootClus = ""
    for i in range(47, 43, -1):
        rootClus += byte[i]
    rootClus = int(rootClus, 16)
    print("RootClus", rootClus)

    # file *dmg

    # FSInfo
    fsInfo = ""
    for i in range(49, 47, -1):
        fsInfo += byte[i]

    fsInfo = int(fsInfo, 16)
    print("fsInfo", fsInfo)

    # BkBootSec
    bkBootSec = ""
    for i in range(51, 49, -1):
        bkBootSec += byte[i]

    bkBootSec = int(bkBootSec, 16)
    print("BkBootSec", bkBootSec)

    # Reserved
    reserved = ""
    for i in range(63, 51, -1):
        reserved += byte[i]
    reserved = int(reserved, 16)
    print("Reserved", reserved)

    # DrvNum
    drvNum = byte[64]
    print("drvNum", drvNum)

    # Reserved1
    reserved1 = int(byte[65], 16)
    print("Reserved1", reserved1)

    # BootSig
    bootSig = byte[66]
    print("BootSig", bootSig)

    # VolID
    volID = ""
    for i in range(67, 71):
        volID += byte[i]
    print("VolID", volID)

    # volLab
    # volLab = "".join(byte[71:82])
    volLab = ""
    for i in range(71, 82):
        volLab += byte[i]
    print("VolLab", volLab)

    # FilSysType
    fileSysType = ""
    for i in range(82, 90):
        fileSysType += byte[i]
    fileSysType = bytes.fromhex(fileSysType).decode('utf-8')
    print("fileSysType", fileSysType)

    return extFlags, fsVer, rootClus, fsInfo, bkBootSec, reserved, drvNum, reserved1, bootSig, volID, volLab, fileSysType


def structureFAT16(byte):
    # drvNum
    drvNum = byte[36]
    print("drvNum", drvNum)

    # reserved1
    reserved1 = int(byte[37], 16)
    print("reserved1", reserved1)
    if reserved1 != 0:
        print("WARNING: reserved1 is different than 0")

    # bootSig
    bootSig = byte[38]
    print("bootSig", bootSig)

    # volID
    volID = ""
    for i in range(39,43):
        volID += byte[i]
    print("VolID", volID)

    # volLab
    volLab = ""
    for i in range(43,54):
        volLab += byte[i]
    print("VolLab", volLab)

    # FilSysType
    fileSysType = ""
    for i in range(54,62):
        fileSysType += byte[i]

    fileSysType = bytes.fromhex(fileSysType).decode('utf-8')
    print("fileSysType", fileSysType)

    return drvNum, reserved1, bootSig, volID, volLab, fileSysType


def root(rootEntCnt, bytesPerSec, fatSz16, fatSz32, rsvdSecCnt, numFAT, totalSec16, totSec32, secPerClus, byte):
    rootDirSectors = ceil(((rootEntCnt * 32) + (bytesPerSec - 1)) / bytesPerSec)
    print("RootDirSectors", rootDirSectors)
    if fatSz16 != 0:
        fatSz = fatSz16
    else:
        fatSz = fatSz32

    if totalSec16 != 0:
        totSec = totalSec16
    else:
        totSec = totSec32

    firstDataSector = rsvdSecCnt + (numFAT * fatSz) + rootDirSectors
    dataSec = totSec - (rsvdSecCnt + (numFAT * fatSz) + rootDirSectors)
    countClusters = int(dataSec // secPerClus)
    typeFAT = ""

    if countClusters < 4085:
        typeFAT = "FAT12"
    elif countClusters < 65525:
        typeFAT = "FAT16"
    else:
        typeFAT = "FAT32"
    print(typeFAT)

    if typeFAT == "FAT12" or typeFAT == "FAT16":
        firstRootDirSecNum = rsvdSecCnt + (numFAT * fatSz)
    print("len", len(byte))

    if typeFAT == "FAT32":
        computation = rsvdSecCnt * bytesPerSec + (numFAT * fatSz32 * bytesPerSec)
        rootDir = byte[rsvdSecCnt * bytesPerSec + (numFAT * fatSz32 * bytesPerSec)]

        print("FILES:")
        try:
            while (byte[computation + 32] != "00"):

                # if it is a short entry
                if byte[computation + 11] != "0f":
                    shortEntry(byte,computation,0)
                    computation += 32
                else:
                    name = ""
                    while byte[computation+11] == '0f':
                        name = longEntry(byte,computation) + name
                        computation += 32
                    print("Long name",name)
                    shortEntry(byte,computation,1)
                    computation+=32
                print()
        except KeyError:
            print("All files were listed")
    elif typeFAT == "FAT16" or typeFAT == "FAT12":
        computation = rsvdSecCnt * bytesPerSec + (numFAT * fatSz16 * bytesPerSec)
        # print("rsvdSecCnt: %d numFAT: %d, fatSz: %d" %(rsvdSecCnt,numFAT,fatSz16))
        # print("computation",computation)
        # print("byte in computation",byte[computation])
        try:
            while (byte[computation + 32] != "00"):
                shortEntry(byte,computation,0)
                computation+=32
                print()
        except KeyError:
            print("All files were listed")
        

def shortEntry(byte,computation,isLong):
    
   # name
    if isLong == 0: # name
        name = ""
        # deletedFile
        deletedFile = 0
        for i in range(computation, computation + 11):
            if i == computation and byte[i] == "e5":
                print("Deleted file:", end=" ")
                deletedFile = 1
            else:
                name += byte[i]

        name = bytes.fromhex(name).decode('latin-1')

        if deletedFile and (name[7:].replace(" ", "")) not in ["", " "]:
            name = name[0:7] + "." + name[7:]
        elif deletedFile == 0 and (name[8:].replace(" ", "")) not in ["", " "]:
            name = name[0:8] + "." + name[8:]

        print(name)

    attr = byte[computation + 11]
    attrDict = {1: "readOnly", 2: "hidden", 4: "system", 8: "volumeID", 10: "Directory", 20: "Archive"}
    attrList = []
    try:
        if attr == "0f" and isLong==1:
            print("attribute: LongName")
        elif attr == "0f" and isLong==0:
            attr = "Read only, hidden, system, Volume_ID"
            print("Attribute:",attr)
        else:
            attr = int(attr)
            if attr % 20 < attr:
                attrList.append(20)
                attr = attr % 20

            if attr % 10 < attr:
                attrList.append(10)
                attr = attr % 10

            if attr % 8 < attr:
                attrList.append(8)
                attr = attr % 8

            if attr % 4 < attr:
                attrList.append(4)
                attr = attr % 4

            if attr % 2 < attr:
                attrList.append(2)
                attr = attr % 2

            if attr % 1 < attr:
                attrList.append(1)
                attr = attr % 1
            
            #cambiar con and con atributo

            print("Attributes:", end=" ")
            for i in attrList:
                attrName = attrDict[i]
                print(attrName, end=" ")
            print()

    except ValueError:
        print("WARNING: attribute unknown")

    #ntrEs
    ntrEs = byte[computation + 12]
    ntrEs = int(ntrEs)

    #crtTimeTenth
    crtTimeTenth = byte[computation + 13]
    crtTimeTenth = int(crtTimeTenth, 16)


    #crtTime
    crtTime = int(byte[computation + 15] + byte[computation + 14] ,16 )
    
    try:
        seconds = crtTime&31
        minutes = (crtTime>>5)&63
        hours = (crtTime>>11)&31

        print("Time at which it was created: %d:%d:%d " %(hours,minutes,seconds) )
    except:
        print("No information about the creation time found")

    #crtDate
    crtDate = int(byte[computation + 17] + byte[computation + 16],16 )
    try:
        day = crtDate&31
        month = (crtDate>>5)&15
        year = (crtDate>>9)&127
        year += 1980

        print("Date at which it was created: %d:%d:%d" %(year,month,day))
        
    except ValueError as e:
        print("No information about the creation date found")
    
    
    #LstAccDate
    lstAccDate = int(byte[computation + 19] + byte[computation + 18],16 )
    try:
        day = lstAccDate&31
        month = (lstAccDate>>5)&15
        year = (lstAccDate>>9)&127
        year += 1980

        print("Date at which it was last accessed: %d:%d:%d" %(year,month,day))
        
    except ValueError as e:
        print("No information about the last access date found")
    
    #wrTime
    wrTime = int(byte[computation + 23] + byte[computation + 22] ,16 )
    
    seconds = wrTime&31
    minutes = (wrTime>>5)&63
    hours = (wrTime>>11)&31
    print("Time of last write: %d:%d:%d " %(hours,minutes,seconds) )

    #wrDate
    wrDate = int(byte[computation + 25] + byte[computation + 24],16 )
    day = wrDate&31
    month = (wrDate>>5)&15
    year = (wrDate>>9)&127
    year += 1980

    print("Date of last write: %d:%d:%d" %(year,month,day))
        
    #fileSize
    fileSize = int(byte[computation+32] + byte[computation+31] + byte[computation+30] + byte[computation+29],16)
    print("File Size %d Bytes" %fileSize)
    

def longEntry(byte,computation):
    dir_Ord = byte[computation]
    name1 = ""
    for i in range(computation+1,computation+11):
        if byte[i] != "ff":
            name1 += byte[i]
    name1 = bytes.fromhex(name1).decode('latin-1')
    attr = byte[computation + 11]
    atype = byte[computation + 12]
    checksum = byte[computation + 13]
    name2 = ""

    for i in range(computation+14,computation+26):
        if byte[i] != "ff":
            name2 += byte[i]
    name2 = bytes.fromhex(name2).decode('latin-1')

    name3 = ""
    for i in range(computation+28,computation+32):
        if byte[i] != "ff":
            name3 += byte[i]
    name3 = bytes.fromhex(name3).decode('latin-1')

    name = name1 + name2 + name3
    return name
    

def main():
    byte = read("FAT16.txt")

    jmpBoot, oemName, bytesPerSec, SecPerClus, rsvdSecCnt, numFAT, rootEntCnt, totalSec16, media, fatSz16, secPerTrk, numHeads, hiddSec, totSec32, fatSz32 = info(byte)    

    
    if fatSz32 != 0:
        extFlags, fsVer, rootClus, fsInfo, bkBootSec, reserved, drvNum, reserved1, bootSig, volID, volLab, fileSysType = structureFAT32(
            byte)
    else:
        drvNum, reserved1, bootSig, volID, volLab, fileSysType = structureFAT16(byte)

    root(rootEntCnt, bytesPerSec, fatSz16, fatSz32, rsvdSecCnt, numFAT, totalSec16, totSec32, SecPerClus, byte)
    

main()

