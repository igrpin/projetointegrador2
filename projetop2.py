import psycopg2
import os
from functionsP2 import *
from aulaFila import *
import datetime
import csv

connection = psycopg2.connect(dbname = 'postgres', user="postgres", password="postgres")
db = connection.cursor()
os.system('clear')
print('Título do projeto: LimpaKi')
print('Equipe: Igor')
print('Objetivo da aplicação: Agendamento de microserviços caseiros')
print('Tecnologias: Python e Postgres')
print('Estrutura de dados: Fila e Lista Encadeada')
print('Banco de dados: 9 Entidades, comandos SELECT e INSERT')
print()
input('hit ENTER to continue...')
os.system('clear')
print('### LimpaKi - Agendamento de microserviços ###')
print()
action = 0 
while True:
    mainMenu()
    action = intValidation()

    if action == 1:
        os.system('clear')
        print('CADASTRAR CLIENTE')
        clientData = getPersonalData()
        if clientData: 
            if insertClient(clientData[0], clientData[1], clientData[2], db, connection):
                os.system('clear')
                print('### Cliente inserido com sucesso ###')
                input('Press ENTER to continue...')
            else:
                os.system('clear')
                print('Ops... Algo deu errado. Tente novamente')
        else:
            print('Tente novamente')
            print()
    elif action == 2:
        os.system('clear')
        print('CADASTRAR PROFISSIONAL')
        professionalData = getPersonalData()
        if professionalData:
            if insertPro(professionalData[0], professionalData[1], professionalData[2], db, connection):
                os.system('clear')
                print('### Profissional cadastrado com sucesso ###')
                input('Press ENTER to continue...')
            else:
                print('Ops... Algo deu errado. Tente novamente')
        else: 
            print('Tente novamente')
            print()
    elif action == 3:
        os.system('clear')
        print('AGENDAR SERVIÇO')
        print()
        print('SELECIONE O CLIENTE')
        clientList = selectClient(db)
        for c in clientList:
            print('[',c[0],']',' ', c[1], sep='')
        clientID = intValidation()
        
        if clientIdValidation(clientID, db):
            os.system('clear')
            print('SELECIONE O SERVIÇO')
            serviceList = selectService(db)
            for s in serviceList:
                print('[',s[0],']',' ',s[1],' | R$ ', s[2], sep='')
            serviceID = intValidation()
            
            if serviceIdValidation(serviceID, db):
                os.system('clear')
                print('SELECIONE UM PROFISSIONAL')
                proList = selectPro(db)
                for p in proList:
                    print('[',p[0],']',' ',p[1], sep='')
                proID = intValidation()

                if proIdValidation(proID, db):
                    os.system('clear')
                    print('DATA DO SERVIÇO (DD/MM/AAAA): ')
                    day = input('DIA: ')
                    month = input('MÊS: ')
                    year = input('ANO: ')
                    date = dateAdjust(year, month, day)
                    if valiDate(date):
                        makeAppointment(clientID, proID, serviceID, date, None , db, connection)
                        os.system('clear')
                        print('### Agendamento efetivado com sucesso ###')
                        input('Hit ENTER to continue...')
                    else:
                        input('Hit ENTER to continue...')
                else:
                    print('Profissional com ID inexistente. Tente novamente')
                    print()
            else:
                print('Serviço com ID inexistente. Tente novamente')
                print()            
        else:
            print('Cliente com ID Inexistente. Tente novamente')
            print()
    elif action == 4:
        os.system('clear')
        print('SELECIONE UM PROFISSIONAL - IMPLEMENTAÇÃO DE FILA')
        subOption = 0
        professionalList = selectPro(db)
        
        for p in professionalList:
            print('[',p[0],']',' ', p[1], sep='')
        
        professionalID = intValidation()
        jobList = proJobList(professionalID, db)
        
        if proIdValidation(professionalID, db):
            while subOption != 6:
                print()
                subMenu()
                subOption = intValidation()
                if (subOption == 1):
                    os.system('clear')
                    if temGente(jobList):
                        i = 1
                        for j in jobList:
                            print('Item', i,'|', 'Profissional:',j[2],'| Cliente:', j[3],'| Serviço:', j[4],'| Data:', j[5])
                            i += 1
                    else:
                        print()
                        print('FILA VAZIA')
                        print()
                elif (subOption == 2):
                    if moveFila(jobList):
                        print()
                        print('MOVIMENTANDO...')
                        print()
                    else:
                        print('FILA VAZIA')
                elif (subOption == 3):
                    os.system('clear')
                    print('Primeiro elemento:')
                    fe = firstElement(jobList)
                    print('Profissional:',fe[2],'| Cliente:', fe[3],'| Serviço:', fe[4],'| Data:', fe[5])
                    print()
                elif (subOption == 4):
                    os.system('clear')
                    print('Quantidade de elementos na fila:')
                    print(len(jobList))
                    print()
                elif (subOption == 5):
                    if temGente(jobList):
                        os.system('clear')
                        print('Último elemento:')
                        la = lastElement(jobList)
                        print('Profissional:',la[2],'| Cliente:', la[3],'| Serviço:', la[4],'| Data:', la[5])
                        print()
                    else:
                        print()
                        print('FILA VAZIA')
                        print()
                elif (subOption == 6):
                    break
                else:
                    print('Opção inválida. Tente novamente')
        else:
            print('Opção inválida')
    elif action == 5:
        os.system('clear')
        print('VERIFICAR A AGENDA DO CLIENTE SELECIONADO')
        print('Implementação de lista encadeada')
        print()
        clientList = selectClient(db)
        for c in clientList:
            print('[',c[0],']',' ',c[1], sep='')
        clientID = intValidation()
        
        if clientIdValidation(clientID, db):
            servList = selectServiceFromClientID(clientID, db)
            clientServList = List()
            if len(servList) == 0:
                print('Cliente sem agendamentos. Tente novamente')
            else: 
                for s in servList:
                    clientServList.insertNode(s)
                otherOption = 0
                while True:
                    linkedListMenu()
                    otherOption = intValidation()
                    if (otherOption == 1):
                        os.system('clear')
                        print('Primeiro elemento (head):')
                        fel = clientServList.getElem(0)
                        print('Cliente:',fel[0],'| Profissional:', fel[1],'| Serviço:', fel[2],'| Data:', fel[3])
                        print()
                    elif (otherOption == 2):
                        os.system('clear')
                        print('Último elemento:')
                        lel = clientServList.getElem(clientServList.size-1)
                        print('Cliente:',lel[0],'| Profissional:', lel[1],'| Serviço:', lel[2],'| Data:', lel[3])
                    elif (otherOption == 3):
                        os.system('clear')
                        print('Quantidade de elementos:', clientServList.size)
                        print()
                    elif (otherOption == 4):
                        c = 1
                        os.system('clear')
                        for i in range(clientServList.size):
                            if clientServList.getElem(i):
                                wtl = clientServList.getElem(i)
                                print('Item {} | Cliente: {} | Profissinoal: {} | Serviço {} | Data: {}'.format(c,wtl[0],wtl[1],wtl[2],wtl[3]))
                                input('Tecle ENTER para continuar')
                                print()
                                c += 1
                    elif (otherOption == 5):
                        os.system('clear')
                        print('REMOVER ELEMENTO DA LISTA')
                        print()
                        if clientServList.size > 0:
                            for i in range(clientServList.size):
                                if clientServList.getElem(i):
                                    rel = clientServList.getElem(i)
                                    print('Índice {} | Cliente: {} | Profissinoal: {} | Serviço {} | Data: {}'.format(i,rel[0],rel[1],rel[2],rel[3]))
                            rem = intValidation()
                            if clientServList.remove(rem) == False:
                                os.system('clear')
                                print('Índice fora do intervalo. Tente novamente')
                                input('Tecle ENTER para continuar')
                            else:
                                os.system('clear')
                                print(' ### Item removido com sucesso. Lista reorganizada ###')
                                print()
                        else: 
                            print('Lista vazia.')
                    elif otherOption == 6:
                        break
                    else:
                        print('Opção inválida. Tente novamente.')
            input("Press Enter to continue...")
            os.system('clear')
        else:
            print('ID Inexistente. Tente novamente')
    elif action == 6:
        os.system('clear')
        print('Até logo!')
        break
    else:
        os.system('clear') 
        print('Opção inválida. Tente novamente.')
        input('Pressione ENTER para continuar...')


db.close()
connection.close()
