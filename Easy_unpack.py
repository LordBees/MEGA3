##easy unpack(standalone unpacker for megav3)
import MEGA_UTIL,os,sys
def main(args):
    cwd = os.getcwd()
    #print(args)
    #print('beep')
    #with open('debuglog.txt','w') as a:
    #    for x in args:
    #        a.write(x)
        #a.write(args)

    #input()
    '''drag a = megafile onto the exe or use the commmand line to easy unpack megas to the directory MEGAEXT'''
    if '\\' in args[0]:
        s = args[0].split('\\')
        args[0] = s[len(s)-1]
    if len(args) > 1:
        MEGA_UTIL.util_unpacktopath(args[0],args[1])
    else:
        if os.path.isdir('MEGA_EX'):
            pass
        else:
            os.mkdir('MEGA_EX')
        os.chdir('MEGA_EX')
        if '.mega' not in args[0].lower():
            args[0]=args[0]+'.mega'##quick workaround

        if os.path.isdir(args[0][:-5]):
            pass
        else:
            os.mkdir(args[0][:-5])
        os.chdir(cwd)

        MEGA_UTIL.util_unpacktopath(args[0],destpath = 'MEGA_EX\\'+args[0][:-5])

if __name__ == "__main__":
    main(sys.argv[1:])##chops off file name