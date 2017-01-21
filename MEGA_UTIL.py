from MEGA import *
import os
import BeeLibv3 as Blib

################
##    tools   ##
################
def util_packpath(newmeganame,datapath = '',MEGAINDIR = True):##packs folder to mega
    if MEGAINDIR == False:
        xmega = mega3(newmeganame)
    cwd = os.getcwd()
    packer = []
    if datapath == '':
        pass#cwd pack
    else:
        os.chdir(datapath)
    if MEGAINDIR == True:
        xmega = mega3(newmeganame)
    packer = os.listdir()
    #print(packer)
    #print(len(packer))
    if newmeganame in packer:
        packer.remove(newmeganame)##remove mega from file so dont attempt to pack itself

    if len(packer) == 0:
        print('no files to pack!')
    else:
        for x in packer:
            xmega.addfile(x)
        xmega.save()
        #xmega.close()
        os.chdir(cwd)

def util_unpacktopath(meganame,destpath = ''):#unpacks megafile to a folder
    xmega = mega3(meganame,NEWIFNOTFOUND = False)
    cwd = os.getcwd()
    if destpath == '':
        pass#cwd pack
    else:
        os.chdir(destpath)
    unpacker = xmega.peek()
    for x in unpacker:
            xmega.unpackfile(x)
    #xmega.save()
    xmega.close()
    os.chdir(cwd)

def util_packfile( mega,file):##packs a file into mega
    pass
def util_unpackfile( fileinmega,topath = 'None'):#unpacks file in mega to a specified path if left blank expands to current path
    pass
def util_compress( tmega):#compresses data in target mega if uncompressed
    pass
def util_decompress( tmega):#decompresses data in target mega if compressed
    pass
def util_mega2to3( tmega):##converts to mega3 form
    pass
def util_megapeek(tmega):##peeks fileheaders and files on mega without loading it fully
    datx = []
    f = open(tmega,'rb')
    datx.append(f.read(8).decode(DECODER))#header-txt
    datx.append(f.read(8))#switches (txt atm)-bin

    datx.append(Blib.csv2array(f.readline()))#filelist-txt
    f.close()
    return datx

def util_is_mega(self,fname):##checks if megafile formatted file exists@path
        if os.path.isfile(fname):
            f = open(fname,'rb')
            lnx = f.read(8).decode('utf-8')
            f.close()
            if 'MEGA3' in lnx:##change to explicit after mega built
                return True
            else:
                return False
        else:
            print('file does not exist!')




################
##    END     ##
################