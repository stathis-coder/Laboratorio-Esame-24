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

        except:
            raise ExamException('Error: No such file was found (hint: try using .csv type file)')

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

        #ritorno la super lista
        return data_list


#funzione che analizza "data_list" e ritorna minimo, massimo e media delle temperture di ogni giorno
def hourly_trend_changes(data_list):
    hour_start_list=[]
    
    #creo la lista risultato dove salvero il numero di trend changes per ogni ora
    result_list=[]

    #ciclo su tutta data_list
    for i, line in enumerate(data_list):
         #se sono all'ultimo elemento della lista
        if i==len(data_list)-1:
            #ne aggiungo un' elemento in piu per interrompere corettamente il ciclo nella riga 100
            hour_start_list.append([data_list[0][0],data_list[0][1]])

        #utilizzando l'operazione di modulo riesco a calcolare l'inizio di ogni giorno in epoch e lo salvo insieme alla temperatura corrispondente
        hour_start_list.append([(data_list[i][0]-(data_list[i][0]%3600)),data_list[i][1]])
   
    
    #creo una lista dove salvero le temperature con lo stesso epoch
    same_hour_list=[]

    #ciclo su tutta "day_start_list"
    for i, line in enumerate(hour_start_list):

        #se sono al primo elemento della lista
        if i==0:
            #appendo la temperatura alla lista delle temperature giornaliere
            same_hour_list.append(hour_start_list[i][1])
        
        #se non sono al primo o ultimo elemento della lista
        if i > 0 and i<len(hour_start_list)-1:
            
            #se l'epoch è uguale al suo precedente
            if hour_start_list[i][0]==hour_start_list[i-1][0]:
                #appendo la temperatura che corrisponde all'epoch in posizione i alla lista sam_day_list
                same_hour_list.append(hour_start_list[i][1])
                

            #se l'epoch è diverso dal suo precedente 
            if hour_start_list[i][0]!=hour_start_list[i-1][0]:

                #appendo alla lista "result" il minimo, e il massimo calcolato sulla lista di temperature giornaliere (same_day_list) e anche la media calcolata facendo: la somma di tutta la lista / la lunghezza della lista
                result_list.append([min(same_day_list),max(same_day_list),(sum(same_day_list)/len(same_day_list))])
                print(same_day_list)
                #svuoto la lista in modo da poter passare al prossimo giorno
                same_day_list=[]
                #aggiungo l'elemento nella lista same_day_list
                same_day_list.append(hour_start_list[i][1]);