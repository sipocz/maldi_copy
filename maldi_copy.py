import os
import shutil
import datetime as dt
import re

# path definition

_logext = ".log"
_swname = "MALDI_COPY_"



_MaldiInput="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\PRD\\"

_Logdirectory="\\log"
_Basedirectory="C:\\maldi_copy\\"
_UsedPlateFile="plates.dat"
_DebugToFile=True
_logprefix = _Basedirectory+_Logdirectory
_usedplatelist=_Basedirectory+_UsedPlateFile    # egy fájlra mutat ami csv-ként tartalmazza a plateID és fióktelep összerendeléseket

_DOR_prefix="DOR"
_DEB_prefix="DEB"
_BUD_prefix="BUD"

_DORNAME="DOROG"
_DEBNAME="DEBRECEN"
_BUDNAME="BUDAPEST"



_DOR_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Dorog_kezi\\"
_DEB_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Debrecen_kezi\\"
_BUD_Source_Path="C:\\Hungary\\dfsroot\\maldi_eredmenyek\\Budapest_kezi\\"

sites=(_DORNAME,_DEBNAME,_BUDNAME)


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
    # print(sourcefname,destfname)  # DEBUG print
    try:
        shutil.copyfile(sourcefname,destfname)
        msg("File copy: "+sourcefname+"-->"+destfname, tofile=_DebugToFile)    
    except: 
        print(destfname)  # DEBUG print
        msg("Exception return: "+" **** ERROR IN FILE COPY ****", tofile=_DebugToFile)        



def parseCSV(str):
    '''
    pontosvessző tagolt stringet elemei bont 
    :param str: a feldolgozandó string  
    :return:  list
    '''
    # print("parse:", str.strip())

    a = str.strip().split(";")
    return (a)

#e8 = u.encode('utf-8')        # encode without BOM
#e8s = u.encode('utf-8-sig')   # encode with BOM
#e16 = u.encode('utf-16')      # encode with BOM
#e16le = u.encode('utf-16le')  # encode without BOM
#e16be = u.encode('utf-16be')  # encode without BOM


def loadCSVfile(fname):
    '''
    csv fálj betöltése egy listába
    param fname: a fájl neve teljes elérési út
    :return: listában adja vissza a file tartalmát
    '''
    msg()
    msg("filename:"+fname)
    l1=[]
    csvfile = open(fname, "rt" , encoding='latin-1')
    for line in csvfile.readlines():
        l1.append(parseCSV(line))
    csvfile.close()
    return (l1)

def loadplates():
    f=loadCSVfile(_usedplatelist)
    f2=dict(f)
    return(f2) 



def checkfile(fname):
    '''
    fname ellenőrzése
        .csv?
        plateID létezik, és helyes?
    return: True, ha minden OK
    '''
    # print("*** file name:",fname)
    # .csv file érkezett?
    o=True
    if fname[-4:].upper() != ".CSV":
        return(False)
    
    # plate id korrekt?
    # megnézük hogy a file nevében szerepel-e a site és szerepel e a sitehoz rendelt plateid
    #
    foundamatch=False
    for key in plates :
        # print(fname, key,plates[key])   # DEBUG PRINT
        if (key in fname) and (plates[key] in fname ):
            foundamatch=True
            
    if not(foundamatch):
        return(False)
    
    # fenntartva egyéb pl. belső szintaktikai ellenőrzések számára
    # 
    if True:
        pass

    # ha nem léptünk ki hibával akkor kilépünk True-val
    return(True)

def copyallmanualfile():
    '''
    végrehajtja a fájlok másolását a manual könyvtárakból a Maldi input könyvtárába
    '''
    _manual_dorog=_DOR_Source_Path
    _manual_budapest=_BUD_Source_Path
    _manual_debrecen=_DEB_Source_Path
    
    dorog_list=listfiles(_manual_dorog)
    budapest_list=listfiles(_manual_budapest)
    debrecen_list=listfiles(_manual_debrecen)
    msg(tofile=_DebugToFile)


    # Dorogi manuális igények ellenőrzése és másolása
    if len(dorog_list)>0:
        for filename in dorog_list:
            if checkfile(_manual_dorog+filename):     # ellenőrizzük a fált
                msg("Dorogi manuális igény másolása: "+filename, tofile=_DebugToFile)
                dest=_MaldiInput
                copyafile(_manual_dorog,filename,dest,"")
            else:                       #nem sikeres az ellenőrzés 
                msg("Dorogi manuális igény fájl nem megfelelő: "+filename, tofile=_DebugToFile)
    else:
        msg("Nincs dorogi manuális igény:", tofile=_DebugToFile) 

    
    # Budapesti manuális igények ellenőrzése és másolása
    if len(budapest_list)>0:
        for filename in budapest_list:
            if checkfile(_manual_budapest+filename):     # ellenőrizzük a fált
                msg("Budapesti manuális igény másolása: "+filename, tofile=_DebugToFile)
                dest=_MaldiInput
                copyafile(_manual_budapest,filename,dest,"")
            else:                        #nem sikeres az ellenőrzés 
                msg("Budapesti manuális igény fájl nem megfelelő: "+filename, tofile=_DebugToFile)
    else:
        msg("Nincs budapesti manuális igény:", tofile=_DebugToFile) 


    # Debreceni manuális igények ellenőrzése és másolása
    if len(debrecen_list)>0:
        for filename in debrecen_list:
            if checkfile(_manual_debrecen+filename):     # ellenőrizzük a fált
                msg("Debreceni manuális igény másolása: "+filename, tofile=_DebugToFile)
                dest=_MaldiInput
                copyafile(_manual_debrecen,filename,dest,"")
            else:                        #nem sikeres az ellenőrzés 
                msg("Debreceni manuális igény fájl nem megfelelő: "+filename, tofile=_DebugToFile)
    else:
        msg("Nincs debreceni manuális igény:", tofile=_DebugToFile) 


# main


plates=loadplates()
    
copyallmanualfile()


