#Progetto in python di linguistica computazionale di Stefano Tambellini anno 2016/2017
#Programma numero 1

#######################
#IMPORTAZIONE LIBRERIE#
#######################

import sys
import os
import nltk

######################
#DEFINIZIONE FUNZIONI#
######################

#Funzione per pulire la console all'avvio
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Funzione iniziale del programma
def init(nomiFile):
    testoIniziale = """+--------------------------------------------------------------------------+
   Progetto di Linguistica Computazionale 2016/2017 Stefano Tambellini
   Programma numero 1
   Corpora di input: """+nomiFile[0]+ " " +nomiFile[1]+"""
+--------------------------------------------------------------------------+

Scegli un valore da confrontare tra i due corpora o un operazione da eseguire:

1) Numero di token del corpus;

2) Lunghezza media delle frasi in termini di token;

3) Grandezza del vocabolario all'aumento del corpus per porzioni 
   incrementali di 1000 token (1000 token, 2000 token, 3000 token, etc.);

4) Ricchezza lessicale calcolata attraverso la Type Token Ratio 
   (TTR) all'aumento del corpus per porzioni incrementali di 1000 token;

5) Rapporto tra sostantivi e verbi (indice che caratterizza 
   variazioni di registro linguistico);

6) Densità lessicale, calcolata come il rapporto tra il numero 
   totale di occorrenze nel testo di Sostantivi, Verbi, Avverbi, Aggettivi e 
   il numero totale di parole nel testo (ad esclusione dei segni di 
   punteggiatura marcati con POS "," ".");

h) Mostrare istruzioni;
q) Chiudere il programma;"""

    print(testoIniziale)

def sceltaOperazione():
    s = input("\nScegli l'operazione: ")
    return s

#Controlla se ci sono errori durante l'apertura del file
def controlloInput(t):
    try:
        f = open(t, "r").read()
    except:
        print("\nErrore nell'apertura del file!\n")
        sys.exit()

#Media dei token nelle frasi
def avgTokFrasi(t):
    tot=0
    num=0

    for frase in t:
        tot += len(nltk.word_tokenize(frase))
        num += 1

    return tot/num

#Vocabolario al crescere del corpus ogni 1000 token
def vocCum(t):
    n = 1000
    l=[]

    while n < len(t): #Creo una lista di tuple
        l.append((n, len(set(t[:n]))))
        n+=1000

    l.append((len(t),len(set(t)))) #Valore finale della distribuzione
    return l

#TTR al crescere del corpus ogni 1000 token
def TTRCum(t):
    n = 1000
    l=[]

    while n < len(t):
        l.append((n, len(set(t[:n]))/len(t[:n])))
        n+=1000

    l.append((len(t),len(set(t))/len(t)))
    return l

#Rapporto Sostantivi/Verbi
def rappSostVerb(t):
    numSost = 0
    numVerb = 0

    for token in t: #Confronto il valore del pos tag
        if token[1]=="NN" or token[1]=="NNP" or token[1]=="NNS" or token[1]=="NNPS":
            numSost+=1
        if token[1]=="VB" or token[1]=="VBD" or token[1]=="VBG" or token[1]=="VBN" or token[1]=="VBP" or token[1]=="VBZ":
            numVerb+=1

    return numSost/numVerb

#Densità lessicale
def densLex(t):
    numPar = 0
    numTok = 0

    for token in t:
        if token[1]=="NN" or token[1]=="NNP" or token[1]=="NNS" or token[1]=="NNPS" or token[1]=="VB" or token[1]=="VBD" or token[1]=="VBG" or token[1]=="VBN" or token[1]=="VBP" or token[1]=="VBZ" or token[1]=="JJ" or token[1]=="JJR" or token[1]=="JJS" or token[1]=="RB" or token[1]=="RBR" or token[1]=="RBS" or token[1]=="WRB":
            numPar += 1
        if token[1]!="." or token[1]!=",":
            numTok += 1

    return numPar/numTok

####################
#PROGRAMMA CENTRALE#
####################

try: #Controllo che l'utente abbia inserito correttamente il nome dei due file di input
    nomiFile = [sys.argv[1], sys.argv[2]]
except:
    print("\nIl programma deve avere due testi di input!\n")
    sys.exit()

controlloInput(nomiFile[0])
controlloInput(nomiFile[1])

testo1Raw = open(nomiFile[0], "r").read()
testo1Tokenizzato = nltk.word_tokenize(testo1Raw)
testo1POSTaggato = nltk.pos_tag(testo1Tokenizzato)

testo2Raw = open(nomiFile[1], "r").read()
testo2Tokenizzato = nltk.word_tokenize(testo2Raw)
testo2POSTaggato = nltk.pos_tag(testo2Tokenizzato)

cls()   #Pulisce lo schermo
init(nomiFile)  #Scrive testo iniziale
cond = True #Condizione del ciclo di scelta

while(cond): #Ciclo di scelta delle operazioni da eseguire
    scelta = sceltaOperazione()
    
    if scelta == "1":
        print(nomiFile[0],"ha",len(testo1Tokenizzato),"token") #Per ogni scelta printo il valore calcolato su entrambi i testi

        print(nomiFile[1],"ha",len(testo2Tokenizzato),"token")

    elif scelta == "2":
        testo1Frasato = nltk.sent_tokenize(testo1Raw)
        print("La media di token per frase di",nomiFile[0],"è di",avgTokFrasi(testo1Frasato),"token")

        testo2Frasato = nltk.sent_tokenize(testo2Raw)
        print("La media di token per frase di",nomiFile[1],"è di",avgTokFrasi(testo2Frasato),"token")

    elif scelta == "3":
        distr1 = vocCum(testo1Tokenizzato)
        print("\nParole tipo ogni 1000 token in",nomiFile[0],":")
        print("Numero Token  :  Parole Tipo")
        for elem in distr1:
            print("      ",elem[0],"  :  ",elem[1])

        distr2 = vocCum(testo2Tokenizzato)
        print("\nParole tipo ogni 1000  token in",nomiFile[1],":")
        print("Numero Token  :  Parole Tipo")
        for elem in distr2:
            print("      ",elem[0],"  :  ",elem[1])

    elif scelta == "4":
        distr1 = TTRCum(testo1Tokenizzato)
        print("\nTTR ogni 1000 token in",nomiFile[0],":")
        print("Numero Token  :  Type-Token Ratio")
        for elem in distr1:
            print("      ",elem[0],"  :  ",elem[1])

        distr2 = TTRCum(testo2Tokenizzato)
        print("\nTTR ogni 1000  token in",nomiFile[1],"")
        print("Numero Token  :  Type-Token Ratio")
        for elem in distr2:
            print("      ",elem[0],"  :  ",elem[1])

    elif scelta == "5":
        print(nomiFile[0]," ha rapporto sostantivi/verbi uguale a ",rappSostVerb(testo1POSTaggato))
        
        print(nomiFile[1]," ha rapporto sostantivi/verbi uguale a ",rappSostVerb(testo2POSTaggato))

    elif scelta == "6":
        print(nomiFile[0]," ha densità lessicale uguale a",densLex(testo1POSTaggato))

        print(nomiFile[1]," ha densità lessicale uguale a",densLex(testo2POSTaggato))

    elif scelta == "h":
        cls()
        init(nomiFile)

    elif scelta == "q": #Chiusura del programma
        print("Ciao!")
        cond = False
        sys.exit()

    else:
        print("\nValore non valido!")