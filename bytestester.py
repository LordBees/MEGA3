import BeeLibv3 as Blib
#import binascii
FOBS = 4
Fpoint = 0
f = open('samplemanualcreatedraw.mega','r')
datx = []
datx.append(f.read(8))#header-txt
datx.append(f.read(8))#switches (txt atm)-bin
datx.append(f.readline())#quick fix appends newline into array
datx[2] = Blib.csv2array(f.readline().strip('\n'))#filelist-txt
Fpoint = f.tell()
datx.append(f.readline().strip('\n'))#offsets(will be bytes) -txt for now
datx.append(f.readlines())

f.close()

f=open('samplemanualcreatedraw.mega','rb')
f.seek(Fpoint)
#f.readline()
datx[3] = f.read(len(datx[2])*FOBS)

f.close()
##configging datx
version = datx[0].strip('MEGA')
files = datx[2]
temp =[]
for x in range(0,len(datx[3]),4):
    temp.append(datx[3][x:x+4])
for x in range(len(temp)):
    temp[x] = bytes.hex(temp[x])#bytes(temp[x],'ASCII'))
offsets = temp
##fancy print
print(datx)
print('||Version = ',version)
print('||Files = ',files)
print('||Offsets = ',offsets)

print('\n\n\n\nofile:offset\n')
for x in range(len(files)):
    print(files[x],':',offsets[x])
