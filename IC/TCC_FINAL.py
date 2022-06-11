import spacy
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) #######Essa linha, juntamente com a biblioteca warnings, foi utilizada para ocultar os avisos da biblioteca gensim, de que o método que está sendo chamado irá ser descontinuado em próximas atualizações.
from nltk.corpus import stopwords
from gensim.models.word2vec import Word2Vec
nlp = spacy.load('en_core_web_sm') # Download da análise gramatical de textos, da biblioteca Spacy
num_doc = 0
stop_words = (stopwords.words('english')) #Lista de stopwords


D = open('A2.txt', 'r')
Doc = D.readlines()


A = [0]*len(Doc) #Uma lista irá receber as frases como TOKEN da biblioteca spacy
B = [0]*len(Doc) #Já a outra, irá receber as frases como string.


Delet = ["METHODS","RESULTS","OBJECTIVE","CONCLUSIONS", "BACKGROUND"] # Palavras a serem excluídas, polindo o documento A1 analisado

for i in range(len(Doc)): #Contabilização do número de artigos no documento A1
    for j in range(len(Doc[i])):
        if Doc[i][j] == "#":
            if j+1 < len(Doc[i]) and Doc[i][j+1] == "#":
                if j+2 < len(Doc[i]) and Doc[i][j+2] == "#":
                    num_doc = num_doc+1

for i in range(len(Doc)): #Mais uma última polida no documento
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


for i in range(len(A)): #Por fim, nessa seção, ocorre a Tokenização das palavras, atribuindo assim, a função gramatical de cada palavra
    A[i] = nlp(A[i])


Frases_ret = [] #Linhas de
index = [] #Número da linha, no documento, para a localização da linha retirada
Sconj_position = [] #Localização, na linha retirada, da palavra com função de conjunção subordinativa
cont = 0
Sconj_list = [] #Lista de palavras com a função de conjunção subordinativa


for i in range(len(A)): #Nessa seção, são selecionadas todas as linhas que possuem uma palavra com a função de conjunção subordinativa
    for j in range(len(A[i])):
        if A[i][j].pos_ == "SCONJ":
            if A[i][j].text != "than" and A[i][j].text != "that":
                Frases_ret.append([" "])
                if A[i][j].text not in Sconj_list:
                    Sconj_list.append(A[i][j].text)
                for h in range(len(B[i])):
                    Frases_ret[cont].append(B[i][h])
                index.append(str(i))
                Sconj_position.append(str(j))
                cont = cont + 1
                break

Frases_final = "" #Variável string contendo todas as linhas retiradas em Frases_ret, que irá ser analisada pelo método Word2Vec

for i in range(len(Frases_ret)):
    Frases_ret[i] = " ".join(Frases_ret[i])

for i in range(len(Frases_ret)):
    Frases_final += Frases_ret[i]

noun_list = [] #Lista de pronomes que irão ser excluídos da análise

for i in range(len(Frases_ret)):
    Frases_ret[i] = nlp(Frases_ret[i])


    for j in range(len(Frases_ret[i])):
        if Frases_ret[i][j].pos_ == "NOUN" and Frases_ret[i][j].text not in noun_list:
            noun_list.append(str(Frases_ret[i][j]))



pontos = [".", ",", "(", ")", ";", "{", "}","'", ":", "[", "]", "!"]

Frases_final_copia = Frases_final


cond = False


similar_words = [] #Palavras similares àquelas que conseguem
similar_words_count = [] #Número de vezes que as palavras similares apareceram


for i in range(len(Sconj_list)): #Para cada palavra con função de conjunção subordinativa, ele irá aplicar os seguintes procedimentos:

    if Sconj_list[i] in stop_words: #Caso a palavra SCONJ estiver na lista de palavras stopwords, ela será retirada da lista de stopwords, temporariamente, para que a análise dela seja feita.
        stop_words.remove(Sconj_list[i])
        cond = True

    Frases_final = ' '.join([word for word in Frases_final_copia.split() if word not in (pontos) and word not in stop_words]) #O texto passa por um filtro, e desconsidera todas as pontuações e stopwords.

    if cond == True: #Depois de feita a análise, caso a palavra estivesse na lista de stopwords, ela é adicionada novamente.
        stop_words.append(Sconj_list[i])
        cond = False


    Frases_final =Frases_final.split()


    w2v_model = Word2Vec(sentences= [Frases_final], window= 10, size = 200, min_count = 1, workers = 4, sg=1) #Aqui ocorre o treinamento e abálise do modelo, através do Word2Vec, onde ele coleta uma janela de 10 palavras próximas, atribui uma lista de 200 elementos pra cada palavra, através do método skip-gram.


    for j in range(10): #Através do conceito de cosine similarity, as 10 palavras que possuírem os vetores mais similares à palavra SCONJ a ser analisada, serão selecionadas

        Palavra = str(w2v_model.most_similar(Sconj_list[i])[j][0]) #Palavra com cosseno similar
        Valor = float(w2v_model.most_similar(Sconj_list[i])[j][1]) #Valor em cosine distance do quão similar ela é

        try: #Esse try irá evidenciar "palavras" que sejam apenas números, para que elas possam ser desconsideradas
            float(Palavra)
        except:
            if Palavra != "%" and Palavra not in noun_list: #Caso a palavra não seja um número, não seja um pronome, e tenha uma similaridade maior que 0.80; ela será considerada para futuras análises.
                if (Palavra not in similar_words) and (Valor > 0.80):
                    similar_words.append(Palavra)
                    similar_words_count.append(0)
                if Valor > 0.80:
                    similar_words_count[similar_words.index(Palavra)] += 1

som = 0
for i in range(len(similar_words_count)): #Contabilização do número de vezes que cada palavra com cossenos similares aparece.
    som += similar_words_count[i]
Palavras_escolhidas = []


df = [0] * len(similar_words) #Document frequency de cada uma das palavras selecionadas, ou seja, em quantas das linhas selecionadas por possuírem uma SCONJ, a palavra similar aparece.

for w in range(len(similar_words)):
    cont = 0
    for i in range(len(B)):
        for j in range(len(B[i])):
            if B[i][j] == similar_words[w]:
                cont +=1
                break
    df[w] = cont


idf = [0]*len(df) #Inverse document frequency

for i in range(len(df)):
    idf[i] = math.log(len(B)/df[i], 10)



tf_idf = [0]*len(idf) #Lista com os valores de tf-idf de cada uma das palavras similares

som_tf_idf = 0

#O maior e menor valor de tf-idf serão retirados do cálculo da média, para uma média mais consistente

maior = (similar_words_count[0]/som) * idf[0]
menor = (similar_words_count[0]/som) * idf[0]

for i in range(len(idf)):
    tf_idf[i] = (similar_words_count[i]/som) * idf[i] #Cálculo dos valores tf-idf para cada uma das palavras similares
    if tf_idf[i] > maior:
        maior = tf_idf[i]
    if tf_idf[i] < menor:
        menor = tf_idf[i]
    som_tf_idf += tf_idf[i]

media = ((som_tf_idf - menor - maior)/(len(tf_idf) - 2)) + (math.log(len(A))) * 0.01 #Cálculo da média, adicionando um valor de correção que escala diretamente com o tamanho do documento analisado, deixando uma métrica cada vez mais rigorosa de acordo com o quão grande o texto é

for i in range(len(tf_idf)): #Por fim, todas as palavras similares, que tiverem o valor de tf-idf acima da média, serão consideradas como palavras selecionadas; aquelas que, caso encontradas em uma linha, serão utilizadas como parâmetro de identificação de trechos com respostas à perguntas de causa
    if tf_idf[i] >= media:
        Palavras_escolhidas.append(similar_words[i])

print("O documento com", num_doc, "artigos foi analisado.")
print("Aguarde até a análise ser aplicada no segundo documento.")








############################################################################

############################################################################

############################################################################





## Os mesmos filtros aplicados para polir os documentos, serão novamente utilizados para tratar do documento B1


D = open('B2.txt', 'r')
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

#Após o fim desse tratamento, ocorre a aplicação das palavras selecionadas (palavras_escolhidas) Para detectar a presença de uma resposta de causa no texto.

index_respostas = []
palavras_respostas = []
Controle_de_erros = [0] * len(Palavras_escolhidas)




for i in range(len(B)):
    for j in range(len(B[i])): #Retira todas as linhas que possuam palavras escolhidas
        if B[i][j] in Palavras_escolhidas:
            index_respostas.append(i)
            palavras_respostas.append(B[i][j])
            break

cont = 0
for i in range(len(index_respostas)):
    cond_erro = True
    for j in range(len(A[index_respostas[i]])): #Para cada uma das linhas retiradas, caso haja uma palavra SCONJ, ela será considerada um sucesso (Cont+=1)
        if A[index_respostas[i]][j].pos_ == "SCONJ":
            cont +=1
            cond_erro = False
            break
    if cond_erro == True: #Caso a linha retirada não possua uma palavra SCONJ, esse resultado será salvo como um erro, no respectivo index da palavra escolhida que gerou o erro. (Palavras_escolhidas[0] = whether *whether causa um erro* controle de erros[0] += 1)
        Controle_de_erros[Palavras_escolhidas.index(palavras_respostas[i])] += 1



print("Linhas corretas:",cont)
print("Palavras escolhidas:")
for i in range(len(Palavras_escolhidas)):
    print(Palavras_escolhidas[i]," ", end="")
print("")
print("Total de linhas:",len(index_respostas))
print("Taxa de sucesso:",cont/len(index_respostas))
print("")