def read(string):
    f = open(string, "r")
    byte = []
    for line in f.readlines():
        line = line[8:]
        if line == "": continue  
        line = line.replace("\n","")
        line = line.strip(" ")
        lista= line.split(" ")
        byte = byte + lista

    return byte

def interpret(byte):

    fatType = ""

    #JmpBoot
    if (byte[0] == "eb" or byte[0]=="EB") and byte[2]=="90":
        print("jmpBoot[0] = 0xEB, jmpBoot[1] = 0x??, jmpBoot[2] = 0x90")
    elif byte[0] == "e9" or byte[0]=="E9":
        print("jmpBoot[0] = 0xE9, jmpBoot[1] = 0x??, jmpBoot[2] = 0x??")
    else:
        print("ERROR: JmpBoot does not match")
        return 1
    
    #OEMName
    name = "".join(byte[3:11])
    name = bytes.fromhex(name).decode('utf-8')
    print(name)

    #BytesPerSec
    msb = byte[12] 
    lsb = byte[11]
    bytesPerSec = msb + lsb
    bytesPerSec = int(bytesPerSec,16)
    print("BytesPerSec",bytesPerSec)

    #BytesPerCluster
    BytesPerCluster = int(byte[13],16)
    print("BytesPerCluster",BytesPerCluster)

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
    


    

    

def main():
    byte = read("fatSmall.txt")
    interpret(byte)


main()