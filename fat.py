from math import ceil
def read(string):
    f = open(string,"r")
    byte = {}
    for line in f.readlines():
        line = line.replace("\n","")
        line = line.strip(" ")
        lista= line.split(" ")
        if lista[0] == "*": continue
        
        pos = int(lista[0],16)
        # ['0000000', 'eb', '58', '90', '42', '53', '44', '20', '20', '34', '2e', '34', '00', '02', '08', '20', '00'
   
        for i in range(0,len(lista)-1):
            byte[pos]=lista[i+1]
            pos+=1

    return byte

def info(byte):

    fatType = ""

    #JmpBoot
    jmpBoot = ""
    if (byte[0] == "eb" or byte[0]=="EB") and byte[2]=="90":
        jmpBoot = ("jmpBoot[0] = 0xEB, jmpBoot[1] = 0x"+ (byte[1]).upper()+ ", jmpBoot[2] = 0x90")
        print(jmpBoot)
    elif byte[0] == "e9" or byte[0]=="E9":
        jmpBoot = "jmpBoot[0] = 0xE9, jmpBoot[1] = 0x"+ byte[1].upper() +", jmpBoot[2] = 0x" + byte[2].upper()
        print(jmpBoot)
    else:
        jmpBoot = "ERROR: JmpBoot does not match"
        print(jmpBoot)
        return 1
    
    #OEMName
    oemName = ""
    for i in range(3,11):
        oemName += byte[i]
    oemName = bytes.fromhex(oemName).decode('utf-8')
    print("OEMName",oemName)

    #BytesPerSec
    msb = byte[12] 
    lsb = byte[11]
    bytesPerSec = msb + lsb
    bytesPerSec = int(bytesPerSec,16)
    print("BytesPerSec",bytesPerSec)
    if (bytesPerSec not in [512,1024,2048,4096]):
        print("ERROR: bytesPerSec is not 512 or 1024 or 2048 or 4096")
        return 1

    #SecPerClus
    SecPerClus = int(byte[13],16)
    print("SecPerClus",SecPerClus)
    if SecPerClus not in [1, 2, 4, 8, 16, 32, 64, 128]:
        print("ERROR: SecPerClus is not 1 or 2 or 4 or 8 or 16 or 64 or 128")
        return 1
    
    '''
    PREGUNTAR
    if BytesPerCluster * bytesPerSec > (32 * 1024):
        print("ERROR: BytesPerCluster is greater than 32 K")
        return 1
    '''

    #RsvdSecCnt 
    msbr = byte[15]
    lsbr = byte[14]
    rsvdSecCnt = int(msbr+lsbr, 16)
    if rsvdSecCnt == 0: 
        print("ERROR: reserved sector count does not match")
        return 1
    print("RsvdSecCnt", rsvdSecCnt)

    #NumFAT
    numFAT = int(byte[16],16)
    print("numFAT", numFAT)
    if numFAT < 1:
        print("ERROR: numFAT is less than 1")
        return 1
    elif numFAT != 2:
        print("WARNING: numFAT is different than 2, some software programs and operating system may not work properly")
    
    #RootEntCnt
    rootEntCnt = int(byte[18]+byte[17],16)
    print("RootEntCnt",rootEntCnt)
    if rootEntCnt == 0:
        fatType = "FAT32"
    elif bytesPerSec % (rootEntCnt* 32) != 0:
         print("ERROR: RootEntCnt does not match")
         return 1

    #TotalSec16
    totalSec16 = int(byte[20]+byte[19]) 
    print("totalSec16", totalSec16)

    #media
    media = byte[21]
    print("media",media)
    if media not in ["f0", "F0","f8","F8","f9","F9","fa","FA","fb","FB","fc","FC","fd","FD","fe","FE"]:
        print("media does not match")
        return 1
    
    #fatSz16
    fatSz16 = int(byte[23]+byte[22],16)
    print("fatSz16",fatSz16)
    if fatType=="FAT32" and fatSz16 != 0:
        print("ERROR: this is a FAT32 and fatSz16 is different than 0")
        return 1
    
    #SecPerTrk
    secPerTrk = int(byte[25]+byte[24],16)
    print("secPerTrk",secPerTrk)

    #NumHeads
    numHeads = int(byte[27]+byte[26], 16)
    print("NumHeads", numHeads)

    #HiddSec
    hiddSec = int(byte[31]+byte[30]+byte[29]+byte[28],16)
    print("HiddSec", hiddSec)

    #totSec32
    totSec32 = int((byte[35]+byte[34]+byte[33]+byte[32]),16)
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
        for i in range(39,35,-1):
            fatSz32 += byte[i]

        fatSz32 = int(fatSz32,16)
        print("FatSz32", fatSz32)
        if (fatSz32 != 0 and fatSz16!=0):
            print("ERROR: both fatSz32 and fatSz16 are not zero")
            return 1
    
    return jmpBoot, oemName, bytesPerSec , SecPerClus, rsvdSecCnt, numFAT, rootEntCnt, totalSec16, media, fatSz16, secPerTrk, numHeads, hiddSec, totSec32, fatSz32

def structureFAT32(byte):

    #ExtFlags
    extFlags = ""
    for i in range(40,42):
        extFlags += byte[i]
    print("ExtFlags",extFlags)

    #FSVer
    fsVer = ""
    for i in range(42,44):
        fsVer += byte[i]
    print("FSVer",fsVer)

    #RootClus
    rootClus = ""
    for i in range(47,43,-1):
        rootClus += byte[i]
    rootClus = int(rootClus,16)
    print("RootClus",rootClus)

    #file *dmg

    #FSInfo
    fsInfo = ""
    for i in range(49,47,-1):
         fsInfo += byte[i]

    fsInfo = int(fsInfo,16)
    print("fsInfo",fsInfo)

    #BkBootSec
    bkBootSec = ""
    for i in range(51,49,-1):
         bkBootSec += byte[i]

    bkBootSec = int(bkBootSec,16)
    print("BkBootSec",bkBootSec)

    #Reserved
    reserved = ""
    for i in range(63,51,-1):
        reserved += byte[i]
    reserved = int(reserved,16)
    print("Reserved",reserved)

    #DrvNum
    drvNum= byte[64]
    print("drvNum",drvNum)

    #Reserved1
    reserved1 = int(byte[65],16)
    print("Reserved1",reserved1)

    #BootSig
    bootSig = byte[66]
    print("BootSig",bootSig)

    #VolID
    volID = ""
    for i in range(67,71):
        volID += byte[i]
    print("VolID", volID)

    #volLab
    #volLab = "".join(byte[71:82])
    volLab = ""
    for i in range(71,82):
        volLab += byte[i]
    print("VolLab", volLab)

    #FilSysType
    fileSysType = ""
    for i in range(82,90):
        fileSysType += byte[i]
    fileSysType = bytes.fromhex(fileSysType).decode('utf-8')
    print("fileSysType", fileSysType)

    return extFlags, fsVer, rootClus, fsInfo, bkBootSec, reserved, drvNum, reserved1, bootSig, volID, volLab, fileSysType

def structureFAT16(byte):
    #drvNum
    drvNum = byte[36]
    print("drvNum", drvNum)

    #reserved1
    reserved1 = int(byte[37],16)
    print("reserved1",reserved1)
    if reserved1 != 0:
        print("WARNING: reserved1 is different than 0")
    
    #bootSig
    bootSig = byte[38]
    print("bootSig",bootSig)

    #volID
    volID = "".join(byte[39:43])
    print("VolID", volID)

    #volLab
    volLab = "".join(byte[43:54])
    print("VolLab", volLab)

    #FilSysType
    fileSysType = "".join(byte[54:62])
    fileSysType = bytes.fromhex(fileSysType).decode('utf-8')
    print("fileSysType", fileSysType)

    return drvNum, reserved1, bootSig, volID, volLab, fileSysType

def root(rootEntCnt, bytesPerSec,fatSz16,fatSz32,rsvdSecCnt, numFAT,totalSec16, totSec32,secPerClus,byte):
    rootDirSectors = ceil(((rootEntCnt * 32 ) + (bytesPerSec - 1))/bytesPerSec)
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
    dataSec = totSec - (rsvdSecCnt + (numFAT * fatSz ) + rootDirSectors)
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
    print("len",len(byte))
    print("Computation", byte[rsvdSecCnt * bytesPerSec + (numFAT * fatSz32 * bytesPerSec)])
    print("Computation", rsvdSecCnt * bytesPerSec + (numFAT * fatSz32 * bytesPerSec))
    
def main():
    byte = read("fat32.txt")
    print(byte)

    jmpBoot, oemName, bytesPerSec , SecPerClus, rsvdSecCnt, numFAT, rootEntCnt, totalSec16, media, fatSz16, secPerTrk, numHeads, hiddSec, totSec32, fatSz32 = info(byte)
    
    if fatSz32 != 0:
       extFlags, fsVer, rootClus, fsInfo, bkBootSec, reserved, drvNum, reserved1, bootSig, volID, volLab, fileSysType = structureFAT32(byte)
    else:
        drvNum, reserved1, bootSig, volID, volLab, fileSysType = structureFAT16(byte)

    root(rootEntCnt, bytesPerSec,fatSz16, fatSz32,rsvdSecCnt, numFAT,totalSec16,totSec32,SecPerClus,byte)



main()