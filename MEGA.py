import os,sys,binascii
import BeeLibv3 as Blib
class mega3:
    __xheader = 'MEGA3XXX'#'MEGA3XXXX'##blank header
    __xmeta =   '000000000'##blank switches
    __XVERSION = '3000'
    
    __LOADED = False##is loaded
    __COMPRESSED = False##is in compressed form(data only)
    __ENCRYPTED = False##added but unused
    __EKEY = ''##key
    __LOADEDVER = ''##megaver
    __MEGA_NAME = ''#mega filename
    __MEGA_qentries = ''##quick entry data
    data_META = ''##meta flags
    data_names = []##fname table
    data_offsets = []#offsets
    data_data = b''#[]##datablock ##string for now

    def __init__(self,MEGAINIT = '',FORCE = False,NEWIFNOTFOUND = True):
        #pass##do some file checking
        if MEGAINIT != '':
            if os.path.isfile(MEGAINIT):
                if FORCE == True:##if force load attempt
                    self.load(MEGAINIT)##if Param specified load the file
                else:
                    if self.is_mega(MEGAINIT) == True:
                        self.load(MEGAINIT)
                    else:
                        print('MEGA header not found, File is not considered valid.')
            elif NEWIFNOTFOUND == True:
                self.new(MEGAINIT)
            else:
                print('file does not exist')

    ################
    ## the  usual ##
    ################
    def is_mega(self,fname):##checks if megafile formatted file exists@path
        if os.path.isfile(fname):
            f = open(fname,'r')
            lnx = f.read(8)
            f.close()
            if 'MEGA3' in lnx:##change to explicit after mega built
                return True
            else:
                return False
        else:
            print('file does not exist!')



    ################
    ##  returners ##
    ################
    def is_compressed(self):#returns compression state
        return self.__COMPRESSED
    def is_loaded(self):##returns loading state
        return self.__LOADED
    def is_version(self):#gets version from loaded mega
        return self.__LOADEDVER
    def is_meganame(self):#gets meganame
        return self.__MEGA_NAME
    def is_megacode_version(self):#gets current mega version from code
        return self.__XVERSION





    ################
    ##   setters  ##
    ################
    def set_loaded(self,TorF):##set loaded as true/false
        self.__LOADED = bool(TorF)
    def set_version(self,newversion):##set version
        self.__LOADEDVER = newversion
    def set_meganame(self,newname):#set name
        self.__MEGA_NAME = newname


    
    
    ################
    ##    MEGA    ##
    ################
    def new(self,Mname,OVR = False):#creates an empty file object for use
        if not os.path.isfile(Mname):
            self.set_loaded('True')
            #self.__MEGA_NAME = Mname
            self.set_meganame(Mname)
            self.set_version(self.is_megacode_version())
            self.data_META = b'00000000'
            self.adddata('TESTENTRY.MEGATEST',b'MEGAFILE TEST ENTRY')
            self.save_reload()

        elif (os.path.isfile(Mname))and (OVR == True):
            print('overwriting existing file!')
            self.load(Mname)
            self.clear()
            
        else:
            print('file already exists, please use load and clear or specify overwrite flag in call')
            
    def load(self,mega):#loads mega data from file into memory object
        if self.is_mega(mega):
            FOBS = 4
            Fpoint = 0
            DECODER = 'utf-8'
            datx = []
  
            f = open(mega,'rb')

            datx.append(f.read(8).decode(DECODER))#header-txt
            datx.append(f.read(8))#switches (txt atm)-bin

            datx.append(f.readline())#filelist-txt
            datx[2] = datx[2][:-2].decode(DECODER)##strips newline
            print(datx[2])
            datx[2] = Blib.csv2array(datx[2])

            datx.append(f.read(len(datx[2])*FOBS))#offsets(will be bytes) -txt for now
            datx.append(f.readlines())#[0].decode(DECODER))
            f.close()
            #if is mega:
            if 'MEGA' in datx[0]:
                self.set_meganame(mega)#sets mega name
                self.set_version(datx[0].strip('MEGA'))##version set
                self.data_META = datx[1]##switches
                #self.data_names = Blib.csv2array(datx[2])##filenames
                self.data_names = datx[2]##filenames
            

                ##converts bytes to integer offset
                temp =[]
                for x in range(0,len(datx[3]),4):
                    temp.append(datx[3][x:x+4])
                for x in range(len(temp)):
                    temp[x] = bytes.hex(temp[x])#bytes(temp[x],'ASCII'))
                offsets = temp
                temp = []
                for x in range(len(offsets)):
                    temp.append(int('0x'+str(offsets[x]),0))
                #offsetsx = temp
                

                self.data_offsets = temp#datx[3]##assign offsets to object table
                temp = []
                ##end offsets bit

                ##concencating data and converting to text ##may want to leave as binary and convert whaen needed
                temp = b''
                for x in range(len(datx[4])):
                    temp = temp+datx[4][x]#.decode(DECODER)#data decoding removed
                datx[4] = temp
                self.data_data = datx[4]
                self.set_loaded('True')

                ##dbg
                if self.data_names[0] == 'TESTENTRY.MEGATEST':
                    print('testentry detected, removing...')
                    self.removefile('TESTENTRY.MEGATEST')


                print('||Version = ',self.is_version())
                print('||Files = ',self.data_names)
                print('||Offsets = ',self.data_offsets)
                print('||Data = ',self.data_data)

        else:
            print('MEGA header not found, File is not considered valid.')
        
        #self.data_offsets = Blib.csv2array(datx[1])

    def load_from_data(self,Mname,megastream,PREPROCESSED = False):#load mega form raw data (must be bin)
        FOBS = 4
        Fpoint = 0
        DECODER = 'utf-8'
        datx = []
        if preprocessed == True:
            if 'MEGA' not in megastream[0]:
                megastream.reverse()
                print('flipping')

            if 'MEGA' not in megastream[0]:##better way of doing with iteration
                print('MEGA header not found at beginning of data stream!')
            else:
                self.set_meganame(Mname)#sets mega name
                self.set_version(megastream[0].strip('MEGA'))##version set
                self.data_META = megasteream[1]##switches
                #self.data_names = Blib.csv2array(datx[2])##filenames
                self.data_names = megastream[2]##filenames
                self.data_offsets = megastream[3]##offsets
                self.data_data = megastream[4]
                self.set_loaded('True')
                ##dbg
                if self.data_names[0] == 'TESTENTRY.MEGATEST':
                    print('testentry detected, removing...')
                    self.removefile('TESTENTRY.MEGATEST')

        elif preprocessed == False:##UNFINISHED!
            #if 'megastream[0]'
            #f = open(mega,'rb')

            datx.append(megastream[0:8].decode(DECODER))#header-txt
            datx.append(megastream[8:16])#switches (txt atm)-bin

            datx.append(f.readline())#filelist-txt
            datx[2] = datx[2][:-2].decode(DECODER)##strips newline
            print(datx[2])
            datx[2] = Blib.csv2array(datx[2])

            datx.append(f.read(len(datx[2])*FOBS))#offsets(will be bytes) -txt for now
            datx.append(f.readlines())#[0].decode(DECODER))
            #f.close()
            #if is mega:
            if 'MEGA' in datx[0]:
                self.set_meganame(mega)#sets mega name
                self.set_version(datx[0].strip('MEGA'))##version set
                self.data_META = datx[1]##switches
                #self.data_names = Blib.csv2array(datx[2])##filenames
                self.data_names = datx[2]##filenames
            

                ##converts bytes to integer offset
                temp =[]
                for x in range(0,len(datx[3]),4):
                    temp.append(datx[3][x:x+4])
                for x in range(len(temp)):
                    temp[x] = bytes.hex(temp[x])#bytes(temp[x],'ASCII'))
                offsets = temp
                temp = []
                for x in range(len(offsets)):
                    temp.append(int('0x'+str(offsets[x]),0))
                #offsetsx = temp
                

                self.data_offsets = temp#datx[3]##assign offsets to object table
                temp = []
                ##end offsets bit

                ##concencating data and converting to text ##may want to leave as binary and convert whaen needed
                temp = b''
                for x in range(len(datx[4])):
                    temp = temp+datx[4][x]#.decode(DECODER)#data decoding removed
                datx[4] = temp
                self.data_data = datx[4]
                self.set_loaded('True')
                if self.data_names[0] == 'TESTENTRY.MEGATEST':
                    print('testentry detected, removing...')
                    self.removefile('TESTENTRY.MEGATEST')
        else:
            print('invalid PREPROCESS argument!')

       # ##dbg
       # if self.data_names[0] == 'TESTENTRY.MEGATEST':
       #     print('testentry detected, removing...')
       #     self.removefile('TESTENTRY.MEGATEST')

        


    def internal_saver(self,fn):##saver funct for save/saveas as code same
        if self.is_loaded() == True:
            if len(self.data_names) == 0:
                self.adddata('TESTENTRY.MEGATEST',b'MEGAFILE TEST ENTRY')
            ENCODER = 'utf-8'
            save_data = []
            save_data.append(('MEGA'+self.is_version()).encode(ENCODER))##version
            save_data.append(self.data_META)##meta
            save_data.append((Blib.array2csv(self.data_names)+'\n').encode(ENCODER))##names

            ##offset conversion
            xtemp = []
            for x in range(len(self.data_offsets)):
                curr = hex(self.data_offsets[x]).strip('0x')
                if len(curr) == 1:
                    curr = '0'+curr
                xtemp.append(bytes.fromhex(str(curr)))

            #padding v2
            for x in range(len(xtemp)):
                padbytes = 4-len(xtemp[x])##4bytes - byte len is bytes to add
                if   padbytes == 0:#no adding so pass(added for readability)
                    pass
                elif padbytes == 1:
                    xtemp[x] = bytes.fromhex('00') + xtemp[x] 
                elif padbytes == 2:
                    xtemp[x] = bytes.fromhex('0000') + xtemp[x] 
                elif padbytes == 3:
                    xtemp[x] = bytes.fromhex('000000') + xtemp[x] 
                else:
                    print('INVALID PADBYTES VALUE!')
            save_data.append(xtemp)#offsets
            xtemp = []
            ##prepoffsetsfor saving
            xtemp = b''
            for x in range(len(save_data[3])):
                xtemp = xtemp+save_data[3][x]
            save_data[3] = xtemp
            xtemp = ''
            save_data.append(self.data_data)#.encode(ENCODER))##data ## forcing all data_data to be bin/bytes format
            print(save_data)

            f = open(fn,'wb')
            for x in save_data:
                f.write(x)
                print('wr:',x)
            f.close()
            print('SAVED!')
        else:
            print('operation failed!, No file loaded.')

    def save(self):#saves current megafile stored in memory to disk
        self.internal_saver(self.is_meganame())

    def saveas(self,fname):#saves current megafile to disk as a different name
        self.internal_saver(fname)

    def reload(self):##reloads mfiledata without saving
        if self.is_loaded():
            self.load(self.is_meganame())
        else:
            print('error cannot reload if file not loaded!')

            
    def save_reload(self):#saves and reloads megafile data
        if self.is_loaded():
            self.save()
            self.load(self.is_meganame())
        else:
            print('error cannot saveas_reload if file not loaded!')

            
    def compressloaded(self):#compresses data in mega if uncompressed
        pass
    def decompressloaded(self):#decompresses data in mega if compressed
        pass

    def addfile(self,fname):#adds file from disk to mega
        f = open(fname,'rb')
        xdat = f.readlines()#.decode('utf-8')
        f.close()
        xtemp = b''
        for x in xdat:
            xtemp = xtemp + x#.decode('utf-8')
        self.adddata(fname,xtemp)

    def removefile(self,xname):#removes file from mega
        if self.is_loaded() == True:
            if xname in self.data_names:
                Fidx = self.data_names.index(xname)
                print('Fidx',Fidx)
                #offsetstart = 0
                #offset = int(self.data_offsets[Fidx])##finds offset data of file
                file_data = b''
                offset_data = []
                for x in self.data_names:
                    if x == xname:
                        pass
                    else:
                        file_data = file_data + self.fetch(x)##copy all data into file data excluding file

                for x in self.data_offsets:
                    #print(x,';;;;',Fidx)
                    if x == self.data_offsets[Fidx]:
                        pass
                    else:
                        offset_data.append(x)


                ##update values
                self.data_offsets = offset_data
                self.data_data = file_data
                self.data_names.remove(xname)
            else:
                print('file not in mega!')
        else:
            print('error cannot saveas_reload if file not loaded!')

    def replacefile(self,fname):#replaces file in mega with one from disk
        self.removefile(fname)
        self.addfile(fname)

    def renamefile(self,xname,newname):##renames file
        if self.is_loaded() == True:
            if xname in self.data_names:
                self.data_names[self.data_names.index(xname)] = newname
        else:
            print('error cannot saveas_reload if file not loaded!')
    
    def unpackfile(self,xname,destpath = ''):##unpacks file from currently loaded megafile
        if self.is_loaded() == True:
            cwd = os.getcwd()
            if destpath == '':
                pass
            else:
                os.chdir(destpath)
            xdat = self.fetch(xname)
            if os.path.isfile(xname):
                pass
            else:
                f = open(xname,'wb')
                f.write(xdat)
                f.close()
            os.chdir(cwd)
        else:
            print('operation failed!, No file loaded.')

    def adddata(self,xname,data):#adds raw data as new file
        if self.is_loaded() == True:
            self.data_names.append(xname)
            self.data_offsets.append(len(data))
            if type(data) == bytes:
                self.data_data = self.data_data + data
            else:
                self.data_data = self.data_data + data.encode('utf-8')

    def replacedata(self,xname,data):#replaces data in megafile with raw data
        self.removefile(xname)
        self.adddata(xname,data)

    def peek(self):#peeks files in mega
        if self.is_loaded() == True:
            return self.data_names
        else:
            print('error cannot saveas_reload if file not loaded!')

    def fetch(self,file,DECODE_DATA = True,DECODER = 'utf-8',NEWLINE_RETURN = False):#fetches file out of mega
        if self.is_loaded() == True:
            offsetstart = 0
            offset = int(self.data_offsets[self.data_names.index(file)])##finds offset data of file
            file_data = b''
            for x in range(0,self.data_names.index(file)):#self.file_names.index(file)):##add offsests to get starting line
                offsetstart +=int(self.data_offsets[x])
                #offset +=1
            #for x in range(offsetstart,(offsetstart+offset)):#appends data to buffer for returning
                #print(self.data_data[x])
                #file_data = file_data+self.data_data[x]
                #print(offset,'.',offsetstart)
            file_data = self.data_data[offsetstart:(offsetstart+offset)]
            if NEWLINE_RETURN == True:
                xtemp = []
                ctemp = ''
                for x in range(len(file_data)-1):##check it doesnt miss the extra 2 at the end of the file
                    if file_data[x:x+1] == '\n':
                        xtemp.append(ctemp+'\n')
                        ctemp=''
                    else:
                        ctemp = ctemp+file_data[x]
            else:
                return file_data
        else:
            print('error cannot saveas_reload if file not loaded!')
    def close(self):#cleans up file and marks as unloaded
        self.clear()
        self.set_loaded('False')
        
    def clear(self):#resets file as blank without closing file
        self.data_META = ''##meta flags
        self.data_names = []##fname table
        self.data_offsets = []#offsets
        self.data_data = ''#[]##datablock ##string for now
        self.set_meganame('')
        self.set_version('')
        ##check clearing is proper

    def modify_attributes(self,xdat):##modifies 8byte header for updating
        pass










    ################
    ##    END     ##
    ################

    def testnew(self,name):
        headermeta = []
        names = []
        offsets = []
        data_file = []
        

        
        

class mega3filestruct:
    pass
#x = mega3()##testing
#x.load('samplemanualcreatedraw.mega')
