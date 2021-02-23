class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    #funzione che istanzia l'oggetto sul nome 
    def __init__(self,name):
        self.name=name

    #funzione che permette di prendere i dati del file
    def get_data(self):
        #creo una super lista vuota che conterrà le liste annidate
        data_list= []

        #controllo che esista veramente un file che si possa aprire
        try:
            my_file=open(self.name,'r')
        #se non posso farlo
        except:
            #alzo un'eccezione
            raise ExamException('Error: No such file was found (hint: try using .csv type file)')

        #ciclo su tutto il file
        for i, line in enumerate(my_file):

            #separo gli elementi del fie sulla virgola (separo gli epoch dalle temperature)
            elements = line.split(',')

            #escludo la prima riga(escludo i titoli delle colonne)
            if elements[0] != 'epoch':
                #controllo che l'input di epoch sia convertibile in interi
                try: 
                    #converto gli epoch in interi arrotondando (gestisco anche il caso in cui la stringa sia un numero float)
                    elements[0]=round(float(elements[0]))
                #se non è possibile farlo
                except:
                    #salto la riga
                    continue 

                #controllo che l'input di temperature sia convertibile in float
                try:
                    #converto le temperature in floating point
                    elements[1]=float(elements[1])
                #se non è possibile farlo
                except:
                    #salto la riga
                    continue
               
                #appendo le epoch e le temperature in un lista che a sua volta verra appesa alla super lista ("data_list")
                data_list.append([elements[0], elements[1]])

        #prima di ritornare la data_list ciclo su tutta la lista per confermare che le epoch siano ordinate
        for i, line in enumerate(data_list):
            #se sono al primo elemento
            if i==0:
                #passo al successivo
                continue

            #se non sono al primo elemento
            if i>0:
                #se un epoch e minore o uguale del suo precedente
                #(gestisco sia epoch non ordinati che duplicati)
                if data_list[i][0]<=data_list[i-1][0]:
                    #alzo l'eccezzione 
                    #(utilizzo "i" e "i+1" invece che "i-1" e "i" per segnare la posizione perche l'utente vede solo il file data e non la lista data_list, cosi facendo salto i titoli delle colonne e l'utente puo trovare l'eccezione piu facilmente)
                    raise ExamException('Error: all epochs must be ordered cronologically, epoch',data_list[i][0],' in position',i,' is greater then or equal to epoch',data_list[i][0],' in position',i+1,'please try again with a file with cronoligcally ordered epochs')

        #chiudo il file per risparmiare spazio in memoria
        my_file.close()

        #ritorno la super lista
        return data_list

#funzione che analizza "data_list" e ritorna una lista con il numero di inversioni di trend per ogni ora
def hourly_trend_changes(data_list):
    #creo una lista in cui salvero le epoch calibrato sull'inizio di ogni ora e le temperature
    hour_start_list=[]
    
    #creo la lista risultato dove salvero il numero di trend changes per ogni ora
    result_list=[]

    #ciclo su tutta data_list
    for i, line in enumerate(data_list):
        #se sono all'ultimo elemento della lista
        if i==len(data_list)-1:
            #aggiungo ad hour_start_list l'ultimo elemento di data_list ma con l'epoch convertito in ore(col ragionamento di riga 90)
            hour_start_list.append([int(data_list[i][0]/3600),data_list[i][1]])
            #aggiungo un' elemento in piu per interrompere corettamente il ciclo nella riga 99
            hour_start_list.append([-1,-1])

        #dividendo l'epoch per 3600 e trasformando il risultato in un intero calcolo quante ore sono passate dal primo gennaio del 1970 in altre parole adesso riesco a distinguere un'ora dall'altra perche tutte le temperature della stessa ora avranno lo stesso epoch in ore
        hour_start_list.append([int(data_list[i][0]/3600),data_list[i][1]])

    #creo una lista dove salvero le temperature con lo stesso epoch in ore (quindi temperature della stessa ora)
    same_hour_list=[]

    #inzializzo questa variabile fuori dal ciclo cosi posso salvarmi il trend della lista same_hour_list prima di azzerarla 
    past_trend = None

    #ciclo su tutta "hour_start_list"
    for i, line in enumerate(hour_start_list):

        #se sono al primo elemento della lista
        if i==0:
            #appendo la temperatura alla lista delle temperature orarie
            same_hour_list.append(hour_start_list[i][1])
        
        #se non sono al primo elemento della lista
        if i > 0 :
            #se l'epoch è uguale al suo precedente
            if hour_start_list[i][0]==hour_start_list[i-1][0]:
                #appendo la temperatura che corrisponde all'epoch in posizione i alla lista same_hour_list
                same_hour_list.append(hour_start_list[i][1])
            
            #se l'epoch è diverso dal suo precedente e l'epoch è diverso da -1(cioe l'ultimo elemento di hour_start_list, quello creato per interrompere corettamente il ciclo)
            if not hour_start_list[i][0]==hour_start_list[i-1][0] and not hour_start_list[i][0]==-1:
                #setto il contatore del trend_change a zero
                trend_change_count=0

                #print(same_hour_list)#(controlli personali)
                #print('----')#(controlli personali)

                #ciclo su tutte la lista delle temperature orarie
                for j, line in enumerate(same_hour_list):
                    #se sono al primo elemento
                    if j==0:
                        #passo al prossimo
                        continue

                    #se sono al secondo elemento
                    if j==1:

                        #True = andamento crescente
                        #False = andamento decrescente

                        #se le due temperature sono uguali
                        if same_hour_list[j]==same_hour_list[j-1]:
                            #passo al prossimo elemento
                            continue
                        #se il trend è decrescente
                        elif same_hour_list[j]<same_hour_list[j-1]:
                            #setto la previsione su decrescente
                            prevision_trend=False
                        #se il trend è crescente
                        else:
                            #setto la previsione su crescente
                             prevision_trend=True

                        #se il trend della lista precedente è diverso dal trend della previsione e il trend non è vuoto(quindi non è la prima volta che analizzo same_hour_list)
                        if not past_trend==prevision_trend and not past_trend==None:
                            #aumento il numero di cambiamenti di trend
                            trend_change_count +=1
                            #setto il trend della lista precedente al trend della lista attuale
                            past_trend=prevision_trend

                    #se sono al terzo elemento in poi
                    if j>1:
                        #se le due temperature sono uguali
                        if same_hour_list[j]==same_hour_list[j-1]:
                            #imposto l'andamento attuale del trend sulla previsione del trend
                            actual_trend=prevision_trend
                        #se la temperature è maggiore della sua precedente
                        elif same_hour_list[j]>same_hour_list[j-1]:
                            #imposto il trend attuale su crescente
                            actual_trend=True
                        #se la temperature è minore della sua precedente
                        else:
                            #imposto il trend attuale su decrescente
                            actual_trend=False

                        #se il trend previsione è diverso dal trend attuale
                        if not prevision_trend==actual_trend:
                            #setto la previsione sull'attuale
                            prevision_trend=actual_trend
                            #aumento il contatore delle inversioni di trend
                            trend_change_count += 1

                        #imposto il trend(che diventera il trend dell'ora precedente) sulla previsione del trend dell'ora attuale
                        past_trend=prevision_trend
                                  
                #dopo che ho ciclato su tutta la lista appendo il numero di inversioni termiche di quell'ora alla lista risultato
                result_list.append(trend_change_count)

                #svuoto la lista delle temperature della stessa ora 
                same_hour_list=[]

                #appendo l'ultima temperature dell'ora precedente(per poter settare l'andamento del trend)
                same_hour_list.append(hour_start_list[i-1][1])
                
                #appendo la prima temperatura della nuova ora
                same_hour_list.append(hour_start_list[i][1])
                        
    #ritorno la lista risultato
    return result_list

#TEST
#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#lista=hourly_trend_changes(time_series)
#print(lista)
#print(len(lista))