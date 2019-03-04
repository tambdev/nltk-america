#Progetto in python di linguistica computazionale di Stefano Tambellini anno 2016/2017
#Programma numero 2

#######################
#IMPORTAZIONE LIBRERIE#
#######################

import sys
import os
import nltk
import math

######################
#DEFINIZIONE FUNZIONI#
######################


def cls():  #Funzione per pulire la console all'avvio
    os.system('cls' if os.name=='nt' else 'clear')


def init(nomiFile): #Funzione iniziale del programma
    testoIniziale = """+--------------------------------------------------------------------------+
   Progetto di Linguistica Computazionale 2016/2017 Stefano Tambellini
   Programma numero 2
   Corpora di input: """+nomiFile[0]+ " " +nomiFile[1]+"""
+--------------------------------------------------------------------------+

Scegli un compito o un operazione da eseguire:

1) estraete ed ordinate in ordine di frequenza decrescente, indicando anche la relativa
frequenza:
◦ le 10 PoS (Part-of-Speech) più frequenti;
◦ i 20 token più frequenti escludendo la punteggiatura;
◦ i 20 bigrammi di token più frequenti che non contengono punteggiatura, articoli e
congiunzioni;
◦ i 20 trigrammi di token più frequenti che non contengono punteggiatura, articoli e
congiunzioni;

2) estraete ed ordinate i 20 bigrammi composti da Aggettivo e Sostantivo (dove ogni token
deve avere una frequenza maggiore di 2):
◦ con probabilità congiunta massima, indicando anche la relativa probabilità;
◦ con probabilità condizionata massima, indicando anche la relativa probabilità;
◦ con forza associativa (calcolata in termini di Local Mutual Information) massima,
indicando anche la relativa forza associativa;

3) le due frasi con probabilità più alta. Dove la probabilità della prima frase deve essere
calcolata attraverso un modello di Markov di ordine 0 mentre la seconda con un modello di
Markov di ordine 1, i due modelli devono usare le statistiche estratte dal corpus che contienele frasi; Le frasi devono essere lunghe almeno 10 token e ogni token deve avere una
frequenza maggiore di 2;

4) dopo aver individuato e classificato le Entità Nominate (NE) presenti nel testo, estraete:
◦ i 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza;
◦ i 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza.

h) Mostrare istruzioni;
q) Chiudere il programma;"""

    print(testoIniziale)

def sceltaOperazione(): #prompt scelta operazione
    s = input("\nScegli l'operazione: ")
    return s

def controlloInput(t):  #controllo correttezza file di input
    try:
        f = open(t, "r").read()
    except:
        print("\nErrore nell'apertura del file!\n")
        sys.exit()

def modelloMarkov0(l, distr, frase):    #calcolo del modello markoviano di ordine zero
    prob = 1.0
    for tok in frase:
        probTok = (distr[tok]*1.0/l*1.0)
        prob *= probTok #moltiplicazione di probabilità di ogni token della frase
    return prob

def freqTokMaggiore2(fraseTok):
    for tok in fraseTok:
        if nltk.FreqDist(testo1Tokenizzato)[tok] <= 2:
            return False
    return True

def probCondizionata(p1,p2,testoTok): #calcolo probabilità condizionata (uso p* per indicare PAROLA e prob* per indicare PROBABILITA')
    n = 0
    for p1,p2 in nltk.bigrams(testoTok):
        n+=1
    return n/len(testoTok)

def probCongiunta(p1,p2,testoTok):  #calcolo probabilità congiunta
    prob1=nltk.FreqDist(testoTok)[p1]*1.0/len(testoTok)*1.0
    return prob1*probCondizionata(p2,p1,testoTok)

def modelloMarkov1(testoTok, distr, frase): #calcolo modello markoviano di secondo ordine
    p = 1.0
    p *= distr[frase[0]]*1.0/len(testoTok)*1.0 #probabilità prima parola

    for tok1,tok2 in nltk.bigrams(frase[1:]):
        pTok = probCondizionata(tok2,tok1,testoTok)
        p *= pTok
    return p

def analisiAlberoChunk(testoPOS, label, tipo): #si parsa l'albero e si estrae il tipo di nodi selezionati con le variabili label e tipo
    l = []
    testoChunk = nltk.ne_chunk(testoPOS)
    for nodo in testoChunk:
        if hasattr(nodo, "label"):
            if(nodo.label() == label):
                if(tipo == "nome"):
                    if(nodo[0][1][:2] == "NN"):
                        l.append(nodo[0])

                elif(tipo == "aggettivo"):
                    if(nodo[0][1][:2] == "JJ"):
                        l.append(nodo[0])
    return l

def informazioneMutua(p1,p2,testoTok):  #calcolo mutua informazione
    prob1 = nltk.FreqDist(testoTok)[p1]*1.0/len(testoTok)*1.0
    prob2 = nltk.FreqDist(testoTok)[p2]*1.0/len(testoTok)*1.0
    return math.log2(probCongiunta(p1,p2,testoTok)/(prob1*prob2))

####################
#PROGRAMMA CENTRALE#
####################

try: #Controllo che l'utente abbia inserito correttamente il nome dei due file di input
    nomiFile = [sys.argv[1], sys.argv[2]]
except:
    print("\nIl programma deve avere due testi di input!\n")
    sys.exit()

controlloInput(nomiFile[0]) #controllo input dei nomi
controlloInput(nomiFile[1])

testo1Raw = open(nomiFile[0], "r").read()   #inizializzo tutti i testi che mi servono all'avvio del programma per non appesantire l'elaborazione
testo1Frasato = nltk.sent_tokenize(testo1Raw)
testo1Tokenizzato = nltk.word_tokenize(testo1Raw)
testo1POSTaggato = nltk.pos_tag(testo1Tokenizzato)

testo2Raw = open(nomiFile[1], "r").read()
testo2Frasato = nltk.sent_tokenize(testo2Raw)
testo2Tokenizzato = nltk.word_tokenize(testo2Raw)
testo2POSTaggato = nltk.pos_tag(testo2Tokenizzato)

cls()   #Pulisce lo schermo
init(nomiFile)  #Scrive testo iniziale
cond = True #Condizione del ciclo di scelta

while(cond): #Ciclo di scelta delle operazioni da eseguire
    scelta = sceltaOperazione()
    
    if scelta == "1":
        print("\n10 pos più frequenti in",nomiFile[0],":")
        pos = [i[1] for i in testo1POSTaggato]
        print(nltk.FreqDist(pos).most_common(10))

        print("\n20 token più frequenti senza punteggiatura in",nomiFile[0],":")
        testo1PosNoPun =[]
        for word in testo1POSTaggato: #controllo se il tag non è punteggiatura
            if word[1]!="," and word[1]!="-" and word[1]!="." and word[1]!=":" and word[1]!=""  and word[1]!="SYM":
                testo1PosNoPun.append(word[0])

        print(nltk.FreqDist(testo1PosNoPun).most_common(20))

        print("\n20 bigrammi token più frequenti che non contengono punteggiatura, articoli o congiunzioni in",nomiFile[0],":")
        testo1PosNoPunArtCong = []
        bigrammiPOS = list(nltk.bigrams(testo1POSTaggato))
        distr = nltk.FreqDist(bigrammiPOS)

        for bigramma in bigrammiPOS:
            if bigramma[0][1]!="," and bigramma[0][1]!="-" and bigramma[0][1]!="." and bigramma[0][1]!=":" and bigramma[0][1]!="" and bigramma[0][1]!="IN" and bigramma[0][1]!="CC" and bigramma[0][1]!="SYM":
                if bigramma[1][1]!="," and bigramma[1][1]!="-" and bigramma[1][1]!="." and bigramma[1][1]!=":" and bigramma[1][1]!="" and bigramma[1][1]!="IN" and bigramma[1][1]!="CC" and bigramma[1][1]!="SYM":
                    testo1PosNoPunArtCong.append(bigramma)

        for tupla in nltk.FreqDist(testo1PosNoPunArtCong).most_common(20):
            print(tupla)

        print("\n20 trigrammi token più frequenti che non contengono punteggiatura, articoli o congiunzioni in",nomiFile[0],":")
        testo1PosNoPunArtCong = []
        trigrammiPOS = list(nltk.trigrams(testo1POSTaggato))
        distr = nltk.FreqDist(trigrammiPOS)

        for trigramma in trigrammiPOS:
            if trigramma[0][1]!="," and trigramma[0][1]!="-" and trigramma[0][1]!="." and trigramma[0][1]!=":" and trigramma[0][1]!="" and trigramma[0][1]!="IN" and trigramma[0][1]!="CC" and trigramma[0][1]!="SYM":
                if trigramma[1][1]!="," and trigramma[1][1]!="-" and trigramma[1][1]!="." and trigramma[1][1]!=":" and trigramma[1][1]!="" and trigramma[1][1]!="IN" and trigramma[1][1]!="CC" and trigramma[1][1]!="SYM":
                    if trigramma[2][1]!="," and trigramma[2][1]!="-" and trigramma[2][1]!="." and trigramma[2][1]!=":" and trigramma[2][1]!="" and trigramma[2][1]!="IN" and trigramma[2][1]!="CC" and trigramma[2][1]!="SYM":
                        testo1PosNoPunArtCong.append(trigramma)

        for tupla in nltk.FreqDist(testo1PosNoPunArtCong).most_common(20):
            print(tupla)

        print("\n10 pos più frequenti in",nomiFile[1],":")
        pos = [i[1] for i in testo2POSTaggato]
        print(nltk.FreqDist(pos).most_common(10))

        print("\n20 token più frequenti senza punteggiatura in",nomiFile[1],":")
        testo2PosNoPun =[]
        for word in testo2POSTaggato: #controllo se il tag non è punteggiatura
            if word[1]!="," and word[1]!="-" and word[1]!="." and word[1]!=":" and word[1]!=""  and word[1]!="SYM":
                testo2PosNoPun.append(word[0])

        print(nltk.FreqDist(testo2PosNoPun).most_common(20))

        print("\n20 bigrammi token più frequenti che non contengono punteggiatura, articoli o congiunzioni in",nomiFile[1],":")
        testo2PosNoPunArtCong = []
        bigrammiPOS = list(nltk.bigrams(testo2POSTaggato))
        distr = nltk.FreqDist(bigrammiPOS)

        for bigramma in bigrammiPOS:
            if bigramma[0][1]!="," and bigramma[0][1]!="-" and bigramma[0][1]!="." and bigramma[0][1]!=":" and bigramma[0][1]!="" and bigramma[0][1]!="IN" and bigramma[0][1]!="CC" and bigramma[0][1]!="SYM":
                if bigramma[1][1]!="," and bigramma[1][1]!="-" and bigramma[1][1]!="." and bigramma[1][1]!=":" and bigramma[1][1]!="" and bigramma[1][1]!="IN" and bigramma[1][1]!="CC" and bigramma[1][1]!="SYM":
                    testo2PosNoPunArtCong.append(bigramma)

        for tupla in nltk.FreqDist(testo2PosNoPunArtCong).most_common(20):
            print(tupla)

        print("\n20 trigrammi token più frequenti che non contengono punteggiatura, articoli o congiunzioni in",nomiFile[1],":")
        testo2PosNoPunArtCong = []
        trigrammiPOS = list(nltk.trigrams(testo2POSTaggato))
        distr = nltk.FreqDist(trigrammiPOS)

        for trigramma in trigrammiPOS:
            if trigramma[0][1]!="," and trigramma[0][1]!="-" and trigramma[0][1]!="." and trigramma[0][1]!=":" and trigramma[0][1]!="" and trigramma[0][1]!="IN" and trigramma[0][1]!="CC" and trigramma[0][1]!="SYM":
                if trigramma[1][1]!="," and trigramma[1][1]!="-" and trigramma[1][1]!="." and trigramma[1][1]!=":" and trigramma[1][1]!="" and trigramma[1][1]!="IN" and trigramma[1][1]!="CC" and trigramma[1][1]!="SYM":
                    if trigramma[2][1]!="," and trigramma[2][1]!="-" and trigramma[2][1]!="." and trigramma[2][1]!=":" and trigramma[2][1]!="" and trigramma[2][1]!="IN" and trigramma[2][1]!="CC" and trigramma[2][1]!="SYM":
                        testo2PosNoPunArtCong.append(trigramma)

        for tupla in nltk.FreqDist(testo2PosNoPunArtCong).most_common(20):
            print(tupla)

    elif scelta == "2":
        bAggSostCong = []
        bAggSostCond = []
        bAggSostMI = []

        for tupla in nltk.bigrams(testo1POSTaggato):
            if (tupla[0][1]=="JJ" or tupla[0][1]=="JJR" or tupla[0][1]=="JJS") and (tupla[1][1]=="NN" or tupla[1][1]=="NNP" or tupla[1][1]=="NNPS" or tupla[1][1]=="NNS") and nltk.FreqDist(testo1Tokenizzato)[tupla[0][0]] > 2 and nltk.FreqDist(testo1Tokenizzato)[tupla[1][0]] > 2:
                bAggSostCong.append((probCongiunta(tupla[0][0],tupla[1][0],testo1Tokenizzato),tupla))
                bAggSostCond.append((probCondizionata(tupla[0][0],tupla[1][0],testo1Tokenizzato),tupla))
                bAggSostMI.append((informazioneMutua(tupla[0][0],tupla[1][0],testo1Tokenizzato),tupla))

        print("\n20 bigrammi composti da aggettivo/sostantivo con token di f>2 in",nomiFile[0])
        print("..di probabilità congiunta massima:")
        for bigramma in sorted(set(bAggSostCong), reverse=True)[0:20]:
            print(bigramma[1]," ----- pCong:",bigramma[0])

        print("\n..di probabilità condizionata massima:")
        for bigramma in sorted(set(bAggSostCond), reverse=True)[0:20]:
            print(bigramma[1]," ----- pCond:",bigramma[0])

        print("\n..di informazione mutua massima")
        for bigramma in sorted(set(bAggSostMI), reverse=True)[0:20]:
            print(bigramma[1]," ----- MI:",bigramma[0])

        bAggSostCong = []
        bAggSostCond = []
        bAggSostMI = []

        for tupla in nltk.bigrams(testo2POSTaggato):
            if (tupla[0][1]=="JJ" or tupla[0][1]=="JJR" or tupla[0][1]=="JJS") and (tupla[1][1]=="NN" or tupla[1][1]=="NNP" or tupla[1][1]=="NNPS" or tupla[1][1]=="NNS") and nltk.FreqDist(testo2Tokenizzato)[tupla[0][0]] > 2 and nltk.FreqDist(testo2Tokenizzato)[tupla[1][0]] > 2:
                bAggSostCong.append((probCongiunta(tupla[0][0],tupla[1][0],testo2Tokenizzato),tupla))
                bAggSostCond.append((probCondizionata(tupla[0][0],tupla[1][0],testo2Tokenizzato),tupla))
                bAggSostMI.append((informazioneMutua(tupla[0][0],tupla[1][0],testo2Tokenizzato),tupla))

        print("\n20 bigrammi composti da aggettivo/sostantivo con token di f>2 in",nomiFile[1])
        print("..di probabilità congiunta massima:")
        for bigramma in sorted(set(bAggSostCong), reverse=True)[0:20]:
            print(bigramma[1]," ----- pCong:",bigramma[0])

        print("\n..di probabilità condizionata massima:")
        for bigramma in sorted(set(bAggSostCond), reverse=True)[0:20]:
            print(bigramma[1]," ----- pCond:",bigramma[0])

        print("\n..di informazione mutua massima")
        for bigramma in sorted(set(bAggSostMI), reverse=True)[0:20]:
            print(bigramma[1]," ----- MI:",bigramma[0])

    elif scelta == "3":
        distr = nltk.FreqDist(testo1Tokenizzato)

        distrFrasi = []
        for frase in testo1Frasato:
            tokF=nltk.word_tokenize(frase)
            if len(tokF)>10 and freqTokMaggiore2(tokF):
                distrFrasi.append((modelloMarkov0(len(testo1Tokenizzato), distr,tokF),frase))
        print("\nFrase con probabilità massima calcolata con modello Markov di ordine zero in",nomiFile[0],":\n\"",max(distrFrasi)[1],"\" :",max(distrFrasi)[0])

        distrFrasi = []
        for frase in testo1Frasato:
            tokF=nltk.word_tokenize(frase)
            if len(tokF)>10 and freqTokMaggiore2(tokF):
                distrFrasi.append((modelloMarkov1(testo1Tokenizzato, distr,tokF),frase))
        print("\nFrase con probabilità massima calcolata con modello Markov di ordine uno in",nomiFile[0],":\n\"",max(distrFrasi)[1],"\" :",max(distrFrasi)[0])

        distr = nltk.FreqDist(testo2Tokenizzato)

        distrFrasi = []
        for frase in testo2Frasato:
            tokF=nltk.word_tokenize(frase)
            if len(tokF)>10 and freqTokMaggiore2(tokF):
                distrFrasi.append((modelloMarkov0(len(testo2Tokenizzato), distr,tokF),frase))
        print("\nFrase con probabilità massima calcolata con modello Markov di ordine zero in",nomiFile[1],":\n\"",max(distrFrasi)[1],"\" :",max(distrFrasi)[0])

        distrFrasi = []
        for frase in testo2Frasato:
            tokF=nltk.word_tokenize(frase)
            if len(tokF)>10 and freqTokMaggiore2(tokF):
                distrFrasi.append((modelloMarkov1(testo2Tokenizzato, distr,tokF),frase))
        print("\nFrase con probabilità massima calcolata con modello Markov di ordine uno in",nomiFile[1],":\n\"",max(distrFrasi)[1],"\" :",max(distrFrasi)[0])

    elif scelta == "4":
        print("\n20 Nomi propri di persona più frequenti in",nomiFile[0],":")
        for n in nltk.FreqDist(analisiAlberoChunk(testo1POSTaggato, "PERSON", "nome")).most_common(20):
            print(n)

        print("\n20 Nomi propri di luogo più frequenti in",nomiFile[0],":")
        for n in nltk.FreqDist(analisiAlberoChunk(testo1POSTaggato, "GPE", "nome")).most_common(20):
            print(n)

        print("\n20 Nomi propri di persona più frequenti in",nomiFile[1],":")
        for n in nltk.FreqDist(analisiAlberoChunk(testo2POSTaggato, "PERSON", "nome")).most_common(20):
            print(n)

        print("\n20 Nomi propri di luogo più frequenti in",nomiFile[1],":")
        for n in nltk.FreqDist(analisiAlberoChunk(testo2POSTaggato, "GPE", "nome")).most_common(20):
            print(n)

    elif scelta == "h":
        cls()
        init(nomiFile)

    elif scelta == "q": #Chiusura del programma
        print("Ciao!")
        cond = False
        sys.exit()

    else:
        print("\nValore non valido!")