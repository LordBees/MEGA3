##tester#
#import MEGA_UTIL as mgu
#mgu.util_packpath('TEST','old')
#os.chdir('extraction test')
#mgu.util_unpackpath('TEST')
import MEGA,MEGA_UTIL,os
cwd = os.getcwd()


##testing mega functions




##testing mega_util functions




#testing misc data
#x = MEGA.mega3('Sample.mega')
##os.chdir('extraction test\\Res')
###x.unpack('')
##print('packing')
##y = MEGA.mega3('Packer.MEGA',FORCE = True)
##y.is_loaded()
##y.pack('')
###x.save()
##y.save()

os.chdir('extraction test')#\\ExTest')
y = MEGA.mega3('Packer.MEGA',FORCE = True)
print('packing')
y.pack('Res')

#x.unpack('')
print('expacking')

#y.is_loaded()
y.unpack('ExTest')

print('saving2disk')
y.save()
os.chdir(cwd)


