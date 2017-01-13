def BeeLib():
    return True
def BeeLib_loaded():
    print('beelib loaded')
def dat2byte(data):##asci values of txt string out
    temp = []
    for x in range(len(data)):
        temp.append(ord(data[x]))
    return temp

def space2csv(strng):##replaces spaces with , char for 'csvising them'
    temp = ''
    for x in range(len(strng)):
        if strng[x] == ' ':
            temp += ','
        else:
            temp += strng[x]
    return temp
def csv2space(strng):
    temp = ''
    for x in range(len(strng)):
        if strng[x] == ',':
            temp += ' '
        else:
            temp += strng[x]
    return temp
def dot2space(strng):
    temp = ''
    for x in range(len(strng)):
        if strng[x] == '.':
            temp += ' '
        else:
            temp += strng[x]
    return temp
def csv2dot(strng):##replaces , with . char for  sub 'csvising them'
    temp = ''
    for x in range(len(strng)):
        if strng[x] == ',':
            temp += '.'
        else:
            temp += strng[x]
    return temp

def dot2csv(strng):##replaces . with , char for  sub 'uncsvising them'
    temp = ''
    for x in range(len(strng)):
        if strng[x] == '.':
            temp += ','
        else:
            temp += strng[x]
    return temp

def csv2array(csvstr):##may need os.isfile() or whatever it is to check file is in dir before declaring eofsame for array2csv
    arrayreturn = []
    temp = ''
    flag = False
    for x in csvstr:#range(len(csvnames)):
        if flag and (x==','):## ,, delimiter
            break
        if x ==',':
            arrayreturn.append(temp)
            temp = ''
            flag = True
        else:
            temp+=x
            flag = False
    return arrayreturn


def array2csv(array):
    temp = ''
    for fl in array:
        print(fl)
        temp += str(fl)+','
    temp+=','
    return temp

def loadfile(file,newlinestrip = True):
    out = []
    datfile = open(file,'r')
    for x in datfile:
        if newlinestrip:
            out.append(x.strip('\n'))
        else:
            out.append(x)
    datfile.close()
    return out

def loadfile2(file,nls = True):##process stripping after loadingaka.strip no worky currenlty yhis way
    datfile = open(file,'r')
    if nls:
        dat = datfile.readlines().strip('\n')
    else:
        dat = datfile.readlines()
    datfile.close()
    return dat

def readfile(self,fname):##file io
    try:
        f = open(fname,'r')
        data = f.readlines()
        f.close()
    except:
        try:
            f.close()
        except:
            print('error/file already closed!')
    return data

def writefile(self,fname,dat,ARRAY = True):##file io
    try:
        f = open(fname,'w')
        if ARRAY == True:
            for x in dat:
                f.write(str(x)+'\n')
                print('ln=',x)
        else:
            f.write(dat)
        f.close()
    except:
        try:
            f.close()
        except:
            print('error/file already closed!')
