#--------------------------------------------------------------------------------------------------------------
import hashlib
from datetime import datetime
import cv2
import numpy as np

import numpy as np
def myBin(data, l = 8):
    if l == 0:
        l = 1
    s = "0{}b".format(l)
    return format(data, s)

def to_bin(data, l = 8):
    #Convert `data` to binary format as string
    if isinstance(data, str):
        return ''.join([ myBin(ord(i),l) for i in data ])
    
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ myBin(i,l) for i in data ]
    elif isinstance(data, int):
        if l == "":
            l = np.ceil(np.log2(max(data)))
        return myBin(data,l)
    elif isinstance(data, np.uint8):
        return  myBin(data,8)
    elif type(data) == list:
        if l == "":
            l = np.ceil(np.log2(max(data)))
        return ''.join([ myBin(i,l) for i in data ])
    
    else:
        raise TypeError("Type not supported.")

def getPos(start, num, pixelNumber):
    return list(range(start,start + num))

def calcHash(data):
    return hashlib.sha1(data.encode()).hexdigest()

def getDateAsStr():
    return str(datetime.now())

def getPosFrom(strr,pos):
    print("\n")
    tmp = ''
    for p in pos:
        tmp += str(strr[p])
    return tmp

def getPosFor(parts,deb):
    alll = []
    j =1
    for i in range(len(parts)):
        if i ==0 :
            tmp = list(range(0,sum(parts[0:1])))
            alll.append(tmp)
        else:
            tmp = list(range(sum(parts[0:j]),sum(parts[0:j+1])))
            alll.append(tmp)
            j = j + 1
        if deb:
            #print(tmp)
            pass
    return alll
def flatImage(coverImage):
    image = []
    for row in coverImage:
        #print(row)
        for pixel in row:
            image.extend(pixel)
    return image

lenn = {
"data": 15,
"hash": 10,
"date": 10
}
lennList = list(lenn.values())

def evaluate(coverImage, imgOrg):
    #difference_array = np.subtract(coverImage, imgOrg)
    #squared_array = np.square(difference_array)
    #mse = squared_array.mean()
    mse = np.mean((np.array(coverImage) - np.array(imgOrg))**2)
    if mse == 0:
        psnr = 100
    else:
        maxPixel = 255.0
        psnr = 10*np.log10(maxPixel**2/mse)
        return mse, psnr

def hideLSB(msg2Hide,coverImage,HK):
    ##
    global AllData_Bin
    r,c,w = coverImage.shape
    coverImage = flatImage(coverImage)
    imgOrg = coverImage.copy()
    imgPixelNum = r * c * w
    h = calcHash(msg2Hide)
    bin_data = to_bin(msg2Hide,8)
    bin_date = to_bin(getDateAsStr(),7)
    bin_hash = to_bin(int(h,16))[2:]
    headerBin = to_bin(len(bin_data),lenn["data"]) + to_bin(len(bin_hash),lenn["hash"]) + to_bin(len(bin_date),lenn["date"])

    dataPart = bin_data + bin_hash + bin_date 
    AllData_Bin = headerBin + dataPart
    AllData_len = len(AllData_Bin)
    
    if AllData_len > imgPixelNum:
        status = (0,"[!] Insufficient bytes, need bigger image or less data.")
    else:
        pos = getPosFor([AllData_len],1)
        for i in pos[0]:
            coverImage[i] = (coverImage[i] & 254) | int(AllData_Bin[i])
    
    mse,psnr = evaluate(coverImage, imgOrg)
    #difference_array = np.subtract(coverImage, imgOrg)
    #squared_array = np.square(difference_array)
    #mse = squared_array.mean()
    finImg = np.array(coverImage).reshape(r, c, w)

    return (finImg,round(mse,5),round(10*np.log10((255^2)/mse),5))
    
    ##
def extractLSB(coverImage, HK):
    global ss
    bin_date = ''
    bin_h = ''
    bin_data = ''
    h1 = ''
    h2 = ''
    h3 = ''
    coverImage = flatImage(coverImage)
    a,b,c = getPosFor(lennList,1)
    for i in a:
        h1 += str(coverImage[i] & 1)
    for i in b:
        h2 += str(coverImage[i] & 1)
    for i in c:
        h3 += str(coverImage[i] & 1) 

    lennD = [int(h1,2),int(h2,2),int(h3,2)]
    a,b,c = getPosFor(lennD,1)
    for i in a:
        bin_data += str(coverImage[i+sum(lennList)] & 1)
    for i in b:
        bin_h += str(coverImage[i+sum(lennList)] & 1)
    for i in c:
        bin_date += str(coverImage[i+sum(lennList)] & 1)
    ss = h1+h2+h3+bin_data+bin_h+bin_date
    
    dataGroupsBin = [ bin_data[i: i+8] for i in range(0, len(bin_data), 8) ]
    data = ""
    for byte in dataGroupsBin:
        data += chr(int(byte, 2))

    h = hex(int(bin_h, 2))
    
    dateGroupBin = [ bin_date[i: i+7] for i in range(0, len(bin_date), 7) ]
    date = ""
    for byte in dateGroupBin:
        date += chr(int(byte, 2))

    print(data)
    print(h)
    print(date)    
    return (data, h, date)

if __name__ == "__main__":
    global AllData_Bin, ss
    
    input_image = "image.PNG"
    output_image = "encoded_image.PNG"
    secret_data = "mohAMMED GO TOndnkccidvjdvjdjvidivdhvdvhsismlcscidvjdvdvnvinsivndclcnzbcdyscsi"

    (coverImage,mse,psnr) = hideLSB(secret_data,cv2.imread(input_image),0);
    cv2.imwrite(output_image, coverImage)
    coverImage = cv2.imread(output_image)
    extractLSB(coverImage, 0)
    print(AllData_Bin,"\n")
    print(AllData_Bin==ss)
    print(mse,psnr)
