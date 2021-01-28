import os
import shutil
import datetime as dt
import re

# path definition

_logext = ".log"
_swname = "MALDI_COPY"


_Basedirectory="C:/gits/maldi_copy"
_Tmpdirectory="C:/gits/maldiTMP"
_Backupdirectory="C:/gits/Maldi2/MaldiBCKP"
_Indirectory="/IN"
_Resultdirectory="/RESULT"
_Outdirectory="/OUT2"
_Logdirectory="/log"
_BackupIN=_Backupdirectory+_Indirectory
_BackupOUT=_Backupdirectory+_Outdirectory
_Backupresult=_Backupdirectory+_Resultdirectory


_DebugToFile=True
_logprefix = _Basedirectory+_Logdirectory




_DOR_prefix="DOR"
_DEB_prefix="DEB"
_BUD_prefix="BUD"




'''
_DOR_Source_Path="\\\\hungary\\dfsroot\\Maldi_eredmenyek\\Dorog kezi\\"
_DEB_Source_Path="\\\\hungary\\dfsroot\\Maldi_eredmenyek\\Dorog kezi\\"
_BUD_Source_Path="\\\\hungary\\dfsroot\\Maldi_eredmenyek\\Dorog kezi\\"
'''

def createLogFile():
    '''
    meghatározza a msg fájl nevét
    :return: a Log file neve stringként
    '''
    import datetime as dt
    from os import path as ospath
    currentdate=dt.datetime.now()
    isostr=currentdate.isoformat()
    datestr="/"+_swname+str(isostr[0:4])+str(isostr[5:7])+str(isostr[8:10])
    fname=_logprefix+datestr+_logext
    #print(fname)
    if ospath.exists(fname):
       pass
    else:
        fileLog = open(fname, "x")
        fileLog.close()
        msg(tofile=_DebugToFile)
        msg("created",tofile=_DebugToFile)
    return (fname)


def timestamp(): 
    '''
    Az aktuális időpontot adja vissza string formában YYYY-MM-DD HH-MM-SS.xxxxxx
    '''
    n = dt.datetime.now()
    n.isoformat(" ", "seconds")
    # print(n)
    return (n)


def msg(msgstr="",tofile=True):
    '''
    :param msgstr: kiírandó szöveg
    :param tofile: alapértelmezett True esetén fájba ír, átírva standard kimenet
    :return:
    '''
    import sys
    caller=sys._getframe(1).f_code.co_name
    if msgstr=="":
        
        if tofile:

            filename=createLogFile()
            fname=open(filename, "a")
            print(timestamp(),file=fname)
            print("\tDEF: ",caller,file=fname)
            fname.close()
        else:
            print(timestamp())
            print("\tDEF: ", caller)
        #print("~"*(len(caller)+4))
    else:
        if tofile:
            filename = createLogFile()
            fname=open(filename, "a")
            print("\t\t"+caller+"-"+msgstr,file=fname)
            fname.close()
        else:
            print("\t\t" +caller+"-"+msgstr)


def listfiles(directory):
    '''
    directory könyvtár elemeit listázza
    :return: listába rendezett fálnevek
    '''
    msg(tofile=_DebugToFile)
    f = []
    for (_, _, filenames) in os.walk(directory):
        f.extend(filenames)
    msg("return: "+str(f), tofile=_DebugToFile)
    return(f)

def copyafile(sourcepath,fname,destpath,prefix):
    '''
    sourcepath könyvtárból fname file-t dest könyvtárba másolja prefix-et tesz a fname elejére 
    '''
    msg(tofile=_DebugToFile)
    sourcefname=sourcepath+fname
    destfname=destpath+prefix+fname
    try:
        shutil.copyfile(sourcefname,destfname)
        msg("File copy: "+sourcefname+"-->"+destfname, tofile=_DebugToFile)    
    except: 
        print(destfname)
        msg("Exception return: "+" **** ERROR IN FILE COPY ****", tofile=_DebugToFile)        
    

