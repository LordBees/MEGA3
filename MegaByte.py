import BeeLibv3 as Blib
#import binascii
FOBS = 4
Fpoint = 0
DECODER = 'utf-8'
f = open('samplemanualcreatedraw.mega','rb')
datx = []
datx.append(f.read(8).decode(DECODER))#header-txt
datx.append(f.read(8))#switches (txt atm)-bin

datx.append(f.readline())#filelist-txt
datx[2] = datx[2][:-2].decode(DECODER)##strips newline
print(datx[2])
datx[2] = Blib.csv2array(datx[2])

datx.append(f.read(len(datx[2])*FOBS))#offsets(will be bytes) -txt for now
datx.append(f.readlines())##data block
f.close()

print(datx)
#f.close()
##configging datx
version = datx[0].strip('MEGA')
files = datx[2]
temp =[]
for x in range(0,len(datx[3]),4):
    temp.append(datx[3][x:x+4])
for x in range(len(temp)):
    temp[x] = bytes.hex(temp[x])#bytes(temp[x],'ASCII'))
offsets = temp
temp = []
for x in range(len(offsets)):
    temp.append(int('0x'+str(offsets[x]),0))
offsetsx = temp
temp = ''
for x in range(len(datx[4])):
    temp = temp+datx[4][x].decode(DECODER)
datx[4] = temp
##fancy print
print(datx)
print('||Version = ',version)
print('||Files = ',files)
print('||Offsets = ',offsets)
print('||Offint  = ',offsetsx)


print('\n\n\n\nofile:offset\n')
for x in range(len(files)):
    print(files[x],':',offsets[x])

