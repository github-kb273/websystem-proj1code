from flask import Flask
from flask import redirect,url_for,render_template,jsonify
from flask import request
import requests
#
gdictGlobal=dict()
gdictGlobal["nGuessCount"]=int(0)  #init guess count
gdictGlobal["strHeader"]="Header<BR>"
gdictGlobal["strFooter"]="Footer<BR>"
gdictGlobal["strContent"]="Content<BR>"
gdictGlobal["strPOSTURL"]="http://127.0.0.1:5000/formpost"
listGuess=[]
gdictGlobal["listGuess"]=listGuess
listCheck=[]
gdictGlobal["listCheck"]=listCheck
listWords=[]
gdictGlobal["listWords"]=listWords
gdictGlobal["nWordCount"]=int(0)
gdictGlobal["strCount"]="Count<BR>"
gdictGlobal["strCategory"]="Category<BR>"
gdictGlobal["bDebug"]=bool(False)
#
app=Flask(__name__,
          template_folder="templates",
          static_folder="static")
#
#----------------------------------------------------------------------------#
#Function:  funcCheckGuess()
#----------------------------------------------------------------------------#
def funcCheckGuess(strInGuess,strInWord):
    strInGuess=strInGuess.upper()
    strInWord=strInWord.upper()
    nLenGuess=len(strInGuess)
    nLenWord=len(strInWord)
    nScore=0
    strScore=""
    for nLoop in range(0,nLenWord):
        if(nLoop<nLenGuess):
            if(strInWord[nLoop]==strInGuess[nLoop]):
                strScore=strScore+str("O")
                nScore=nScore+1
            else:
                strScore=strScore+str("X")
        else:
            strScore=strScore+str("?")
        if(gdictGlobal["bDebug"]!=False):
            print(f"funcCheckGuess()::{nLoop}:{strScore}:nS{nScore}:lenG{nLenGuess}:lenW{nLenGuess}")
#    nTemp=nScore+1
    if((nScore==nLenWord) and (nScore==nLenGuess)):
        if(gdictGlobal["bDebug"]!=False):
            print(f"win {nScore}:{nLenWord}:{nLenGuess}")
        strScore="*"
    else:
        if(gdictGlobal["bDebug"]!=False):
            print(f"lose {nScore}:{nLenWord}:{nLenGuess}")
    return strScore
#
#----------------------------------------------------------------------------#
#Function:  getguess()
#****make single render_template()****
#----------------------------------------------------------------------------#
@app.route("/getguess")
def getguess():
    print("getguess():Enter")
    strGuess=request.args.get("wordguess")  #Obtain user word guess
 #
    #increment guess count
    nGuessCount=int(gdictGlobal["nGuessCount"])
    nGuessCount=nGuessCount+1  #increment guess count
    gdictGlobal["nGuessCount"]=int(nGuessCount)    
#
    strCount=str(nGuessCount)  #Guess count string
    listGuess=gdictGlobal["listGuess"]
    listCheck=gdictGlobal["listCheck"]
#
    listWords=gdictGlobal["listWords"]
    nSelect=gdictGlobal["nWordSelect"]
    listSep=listWords[nSelect].split(',')
    print(f"Comma: {listSep[0]},{listSep[1]},{listSep[2]}")
    strCategory=listSep[1]
    strLength=len(listSep[2])
    strWinWord=listSep[2]
    gdictGlobal["strWinWord"]=strWinWord
#
    strCheck=funcCheckGuess(strGuess,strWinWord)
    if(strCheck != "*"):
#        print(f"Check:{strCheck}-G{strGuess}-W{strWinWord}")
#        print("Get guess.")
#
#    strTemp=strGuess+"["+strCheck+"]"
#    strTemp=strGuess
        listGuess.append(strGuess)
        listCheck.append(strCheck)
#
        strContent="<TABLE>"
        nLines=len(listGuess)
        for nLoop in range(0,nLines):
            strGuess0=str(listGuess[nLoop])
            strCheck0=str(listCheck[nLoop])
            strContent=strContent+"<FONT SIZE=4><TR><TD>"+strGuess0+"</TD><TD>["+strCheck0+"]"+"</TD></TR></FONT>"
#            print(f"getguess()::strG{strGuess0}:strC{strCheck0}")
        strContent=strContent+"</TABLE>"
        #
        strTemp=f"getguess():WinWord={strWinWord} Guess={strGuess} Count={strCount}"
        print(f"getguess():{strTemp}")
        strTemp=strGuess.upper()
        strHeader=f"<FONT SIZE=5>Guess my word.  <BR>Guess: {strGuess} --- Guess number: {strCount}</FONT><BR>"
        strFooter=f"<FONT SIZE=5>Guess my word.</FONT><BR>"
#        strFooter="<FONT SIZE=5>Guess my word.</FONT><BR>"
        gdictGlobal["strHeader"]=strHeader
        gdictGlobal["strFooter"]=strFooter
        gdictGlobal["strContent"]=strContent
        strPOSTURL=gdictGlobal["strPOSTURL"]
#    if(strCheck!="*"):
        strCategory=f"My word is {strLength} letters long and a {strCategory}.<BR>"
#        strGuessCount=str(gdictGlobal["nGuessCount"])
        strCount="<FONT SIZE=4>There has been "+strCount+f" guesses.</FONT><BR>"
#        print("getguess()::strCount:{strCount}")
        gdictGlobal["strCategory"]=strCategory
        gdictGlobal["strCount"]=strCount
#        strReturn = render_template("wordfun.html",
#                                    htmlHeader0=strHeader,
#                                    htmlFooter0=strFooter,
#                                    htmlContentList0=strContent,
#                                    htmlPOSTURL=strPOSTURL,
#                                    htmlCount=strCount,
#                                    htmlCategory=strCategory)
#        strReturn = redirect(url_for("getguess",
#                                    htmlHeader0=strHeader,
#                                    htmlFooter0=strFooter,
#                                    htmlContentList0=strContent,
#                                    htmlPOSTURL=strPOSTURL))
#        strReturn=redirect("/",code=302)
#        print(f"{strReturn}")
    else:
        #Player guessed word.
        print(f"Check:{strCheck}")
        print("Player guessed word.")
        strWord0=strWinWord.upper()
        #increment word selection
        nSelect=gdictGlobal["nWordSelect"]
        listWords=gdictGlobal["listWords"]
        nWordLen=len(listWords)
        nSelect=nSelect+1
        if(nSelect>=nWordLen):
            nSelect=0
        gdictGlobal["nWordSelect"]=int(nSelect)
        #
        strTemp=listWords[nSelect]
        listSep=strTemp.split(",")
        strWinWord=listSep[2]
        strLength=str(len(listSep[2]))
        strCategory=listSep[1]
#        print(f"getguess()::strNew{strWinWord} and select {nSelect}:{strLength}:{strCategory}")
#        
        gdictGlobal["strLength"]=strLength
        gdictGlobal["strCategory"]=strCategory
        strCount="<FONT SIZE=4>I have selected a new word.  Guess my word.</FONT><BR>"
        strCategory=f"My word is {strLength} letters long and a {strCategory}.<BR>"
        gdictGlobal["strCount"]=strCount
        strGuessCount=str(gdictGlobal["nGuessCount"])
        strHeader=f"<FONT size=5>You guessed my word in {strGuessCount} tries.  My word is {strWord0}</FONT><BR>"
        strFooter=f"<FONT size=5>Guess My Word.</FONT><BR>"
        print(f"getguess()::strF{strFooter}")
        listGuess.append(strGuess)
        listCheck.append(strCheck)
        strContent="<TABLE>"
        nLines=len(listGuess)
        for nLoop in range(0,nLines):
            strGuess0=str(listGuess[nLoop])
            strCheck0=str(listCheck[nLoop])
            strContent=strContent+"<FONT SIZE=4><TR><TD>"+strGuess0+"</TD><TD>["+strCheck0+"]"+"</TD></TR></FONT>"
        strContent=strContent+"</TABLE>"
#        strContent="strContent<BR>"
        strTemp=strGuess.upper()
#        strHeader=f"<FONT SIZE=5>Guess my word.  <BR>Guess: {strTemp} --- Guess number: {strGuessCount}</FONT><BR>"
#        strFooter=f"<FONT SIZE=5>Guess my word {strWinWord}.</FONT><BR>"
        gdictGlobal["strCategory"]=strCategory
        gdictGlobal["strHeader"]=strHeader
        gdictGlobal["strFooter"]=strFooter
        gdictGlobal["strContent"]=strContent
        strPOSTURL=gdictGlobal["strPOSTURL"]
        gdictGlobal["nGuessCount"]=0
        listGuess=gdictGlobal["listGuess"]
        listGuess.clear()
        listGuess=[]
        gdictGlobal["listGuess"]=listGuess
        listCheck=gdictGlobal["listCheck"]
        listCheck.clear()
        listCheck=[]
        gdictGlobal["listCheck"]=listCheck
#        strReturn=redirect("/",code=302)
    strReturn = render_template("wordfun.html",
                                htmlHeader0=strHeader,
                                htmlFooter0=strFooter,
                                htmlContentList0=strContent,
                                htmlPOSTURL=strPOSTURL,
                                htmlCount=strCount,
                                htmlCategory=strCategory)
#    strReturn=redirect("/",code=302)
    print("getguess():Exit")
    return strReturn
#
#----------------------------------------------------------------------------#
#Function:  home()
#----------------------------------------------------------------------------#
@app.route("/")
def home():
    print("home():Enter")
#
#    listWords=gdictGlobal["listWords"]
#
#    nSelect=gdictGlobal["nWordSelect"]
#    nC=len(listWords)
#    print(f"select: {nSelect} {nC}")
#    strTemp=listWords[nSelect]
#    print(f"split: {strTemp}")
#    listSep=strTemp.split(",")
#    strTemp=listSep[0]
#    print(f"Comma0: {strTemp}")
#    strTemp=listSep[1]
#    print(f"Comma1: {strTemp}")
#    strTemp=listSep[2]
#    print(f"Comma2: {strTemp}")
#    gdictGlobal["strCategory"]=listSep[1]
#    gdictGlobal["strLength"]=len(listSep[2])
#    gdictGlobal["strWinWord"]=listSep[2]
    strCategory=gdictGlobal["strCategory"]
    strHeader=gdictGlobal["strHeader"]
    strFooter=gdictGlobal["strFooter"]
    strContent=gdictGlobal["strContent"]
    strPOSTURL=gdictGlobal["strPOSTURL"]
    strCount=gdictGlobal["strCount"]
    strCategory=gdictGlobal["strCategory"]
#    strGuessCount=str(gdictGlobal["nGuessCount"])
#    strLength=gdictGlobal["strLength"]
#    strCategory=f"<FONT SIZE=4>My word is {strLength} letters long and a {strCategory}.</FONT><BR>"
#    strCount="<FONT SIZE=4>There has been "+strGuessCount+" guesses.</FONT><BR>"
    strReturn = render_template("wordfun.html",
                                htmlHeader0=strHeader,
                                htmlFooter0=strFooter,
                                htmlContentList0=strContent,
                                htmlPOSTURL=strPOSTURL,
                                htmlCount=strCount,
                                htmlCategory=strCategory)
    print("home():Exit")
    return strReturn
#
#----------------------------------------------------------------------------#
#Function:  formpost()
#----------------------------------------------------------------------------#
@app.route("/formpost",methods=["POST","GET"])
def formpost():
    print("formpost():Enter")
    if(request.method=="POST"):
        strGuess=request.form["wordguess"]
    else:
        strGuess=request.args.get("wordguess")
#    nGuessCount=int(gdictGlobal["nGuessCount"])
#    nGuessCount=nGuessCount+1
#    gdictGlobal["nGuessCount"]=int(nGuessCount)    
    dictParams=dict()
    dictParams["wordguess"]=strGuess
    requests.get(url="http://127.0.0.1:5000/getguess",params=dictParams)
#    strReturn="FORMPOST<BR>"
#    strReturn=redirect(())
    print("formpost():Exit")
    strReturn=redirect("/")
    return strReturn
#
#
#----------------------------------------------------------------------------#
#Function:  app.run()
#----------------------------------------------------------------------------#
if(__name__=="__main__"):
    print("app.run()")
#  Load word set from file
    fileWords=open("wordlist.txt","r")
    strFile=fileWords.read()
    lineFile=strFile.split()
    fileWords.close()
#
    listWords=gdictGlobal["listWords"]
    for strLine in lineFile:
        listWords.append(strLine)
#        print(f"Word:{strLine}")
#
    nSelect=1
    nCheck=len(listWords)
    if(nSelect<nCheck):
        gdictGlobal["nWordSelect"]=nSelect
    else:
        gdictGlobal["nWordSelect"]=0
#
    listWords=gdictGlobal["listWords"]
#
    nSelect=gdictGlobal["nWordSelect"]
    strTemp=listWords[nSelect]
    listSep=strTemp.split(",")
    strCategory=listSep[1]
    gdictGlobal["strCategory"]=listSep[1]  #Word category
    gdictGlobal["strLength"]=str(len(listSep[2]))  #Get length of guess word
    gdictGlobal["strWinWord"]=listSep[2]  #Word to guess
#    gdictGlobal["nGuessCount"]=int(0)
    strCount=str(gdictGlobal["nGuessCount"])  #guess count string
    strLength=gdictGlobal["strLength"]
#    strCategory=gdictGlobal["strCategory"]
    strCategory=f"<FONT SIZE=4>My word is {strLength} letters long and a {strCategory}.</FONT><BR>"
    strCount="<FONT SIZE=4>There has been "+strCount+" guesses.</FONT><BR>"
    gdictGlobal["strCount"]=strCount  #String message for guess count
    gdictGlobal["strCategory"]=strCategory  #String message for category output
#
    app.run(debug=True)
