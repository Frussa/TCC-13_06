import spacy
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from nltk.corpus import stopwords
from gensim.models.word2vec import Word2Vec
nlp = spacy.load('en_core_web_sm')
num_doc = 0

stop_words = (stopwords.words('english'))


D = open('Train_red.txt', 'r')
Doc = D.readlines()


A = [0]*len(Doc)
B = [0]*len(Doc)


Delet = ["METHODS","RESULTS","OBJECTIVE","CONCLUSIONS", "BACKGROUND"]

for i in range(len(Doc)):
    for j in range(len(Doc[i])):
        if Doc[i][j] == "#":
            if j+1 < len(Doc[i]) and Doc[i][j+1] == "#":
                if j+2 < len(Doc[i]) and Doc[i][j+2] == "#":
                    num_doc = num_doc+1

for i in range(len(Doc)):
    Doc[i] = Doc[i].replace("\t", " ")
    Doc[i] = Doc[i].replace("\n", " ")
    A[i] = Doc[i].split(" ")
    B[i] = Doc[i].split(" ")

D.close()

for i in range(len(A)):
    cont = 0
    while cont<(len(A[i])):
        if A[i][cont] in Delet:
            del(A[i][cont])
            cont = cont+1
        cont = cont+1

for i in range(len(B)):
    cont = 0
    while cont<(len(B[i])):
        if B[i][cont] in Delet:
            del(B[i][cont])
            cont = cont+1
        cont = cont+1



for i in range(len(A)):
    for j in range(len(A[i])):
        A[i][j] = A[i][j].lower()
        B[i][j] = B[i][j].lower()



for i in range(len(A)):
    A[i] = " ".join(A[i])


for i in range(len(A)):
    A[i] = nlp(A[i])


Frases_ret = []
index = []
Sconj_position = []
cont = 0
Sconj_list = []


for i in range(len(A)):
    for j in range(len(A[i])):
        if A[i][j].pos_ == "SCONJ":

            print(" ")
            print(A[i])
            for ç in range(len(A[i])):
                print(" ", A[i][ç].pos_, end=' ')
            print(" ")


            if A[i][j].text != "than" and A[i][j].text != "that":
                Frases_ret.append([" "])
                if A[i][j].text not in Sconj_list:
                    Sconj_list.append(A[i][j].text)
                for h in range(len(B[i])):
                    Frases_ret[cont].append(B[i][h])
                index.append(str(i))
                Sconj_position.append(str(j))
                cont = cont + 1 ####### NÃO ESQUECE DE TIRAR, PELO AMOR DE DEUS
                break

Frases_final = ""

for i in range(len(Frases_ret)):
    Frases_ret[i] = " ".join(Frases_ret[i])

for i in range(len(Frases_ret)):
    Frases_final += Frases_ret[i]


noun_list = []

for i in range(len(Frases_ret)):
    Frases_ret[i] = nlp(Frases_ret[i])


    for j in range(len(Frases_ret[i])):
        if Frases_ret[i][j].pos_ == "NOUN" and Frases_ret[i][j].text not in noun_list:
            noun_list.append(str(Frases_ret[i][j]))



pontos = [".", ",", "(", ")", ";", "{", "}","'", ":", "[", "]", "!"]

Frases_final_copia = Frases_final


cond = False


similar_words = []
similar_words_count = []


for i in range(len(Sconj_list)):

    if Sconj_list[i] in stop_words:
        stop_words.remove(Sconj_list[i])
        cond = True

    Frases_final = ' '.join([word for word in Frases_final_copia.split() if word not in (pontos) and word not in stop_words])

    if cond == True:
        stop_words.append(Sconj_list[i])
        cond = False


    Frases_final =Frases_final.split()


    w2v_model = Word2Vec(sentences= [Frases_final], window= 10, size = 200, min_count = 1, workers = 4, sg=1)


    for j in range(10):

        Palavra = str(w2v_model.most_similar(Sconj_list[i])[j][0])
        Valor = float(w2v_model.most_similar(Sconj_list[i])[j][1])

        try:
            float(Palavra)
        except:
            if Palavra != "%" and Palavra not in noun_list:
                if (Palavra not in similar_words) and (Valor > 0.80):
                    similar_words.append(Palavra)
                    similar_words_count.append(0)
                if Valor > 0.80:
                    similar_words_count[similar_words.index(Palavra)] += 1

som = 0
for i in range(len(similar_words_count)):
    som += similar_words_count[i]
Palavras_escolhidas = []


df = [0] * len(similar_words)

for w in range(len(similar_words)):
    cont = 0
    for i in range(len(B)):
        for j in range(len(B[i])):
            if B[i][j] == similar_words[w]:
                cont +=1
                break
    df[w] = cont


idf = [0]*len(df)

for i in range(len(df)):
    idf[i] = math.log(len(B)/df[i], 10)



tf_idf = [0]*len(idf)

som_tf_idf = 0

maior = (similar_words_count[0]/som) * idf[0]
menor = (similar_words_count[0]/som) * idf[0]

for i in range(len(idf)):
    tf_idf[i] = (similar_words_count[i]/som) * idf[i]
    if tf_idf[i] > maior:
        maior = tf_idf[i]
    if tf_idf[i] < menor:
        menor = tf_idf[i]
    som_tf_idf += tf_idf[i]

media = ((som_tf_idf - menor - maior)/(len(tf_idf) - 2)) + (math.log(len(A))) * 0.01

for i in range(len(tf_idf)):
    if tf_idf[i] >= media:
        Palavras_escolhidas.append(similar_words[i])

print(num_doc)








############################################################################

############################################################################

############################################################################








D = open('Train_red_2.txt', 'r')
Doc = D.readlines()


A = [0]*len(Doc)
B = [0]*len(Doc)


Delet = ["METHODS","RESULTS","OBJECTIVE","CONCLUSIONS", "BACKGROUND"]

for i in range(len(Doc)):
    for j in range(len(Doc[i])):
        if Doc[i][j] == "#":
            if j+1 < len(Doc[i]) and Doc[i][j+1] == "#":
                if j+2 < len(Doc[i]) and Doc[i][j+2] == "#":
                    num_doc = num_doc+1

for i in range(len(Doc)):
    Doc[i] = Doc[i].replace("\t", " ")
    Doc[i] = Doc[i].replace("\n", " ")
    A[i] = Doc[i].split(" ")
    B[i] = Doc[i].split(" ")

D.close()

for i in range(len(A)):
    cont = 0
    while cont<(len(A[i])):
        if A[i][cont] in Delet:
            del(A[i][cont])
            cont = cont+1
        cont = cont+1

for i in range(len(B)):
    cont = 0
    while cont<(len(B[i])):
        if B[i][cont] in Delet:
            del(B[i][cont])
            cont = cont+1
        cont = cont+1



for i in range(len(A)):
    for j in range(len(A[i])):
        A[i][j] = A[i][j].lower()
        B[i][j] = B[i][j].lower()



for i in range(len(A)):
    A[i] = " ".join(A[i])


index_respostas = []
palavras_respostas = []
cagadas_cometidas = [0]*len(Palavras_escolhidas)

for i in range(len(A)):
    A[i] = nlp(A[i])

for i in range(len(B)):
    for j in range(len(B[i])):
        if B[i][j] in Palavras_escolhidas:
            index_respostas.append(i)
            palavras_respostas.append(B[i][j])
            break

cont = 0

for i in range(len(index_respostas)):
    for j in range(len(A[index_respostas[i]])):
        if A[index_respostas[i]][j].pos_ == "SCONJ":
            cont +=1
            break
    cagadas_cometidas[Palavras_escolhidas.index(palavras_respostas[i])] += 1

'''
for i in range(len(index_respostas)):
    print(" ")
    print("Exemplo {:d}:".format(i))
    print(A[index_respostas[i]])
    for j in range(len(A[index_respostas[i]])):
        print(" ",A[index_respostas[i]][j].pos_, end=' ')
    print(" ")
'''

print("Linhas corretas:",cont)
print("Palavras escolhidas:")
for i in range(len(Palavras_escolhidas)):
    print(Palavras_escolhidas[i]," ", end="")
print("")
print("Total de linhas:",len(index_respostas))
print("Taxa de sucesso:",cont/len(index_respostas))