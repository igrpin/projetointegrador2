import datetime

# INSERT

def insertClient(thisName, thisBirth, thisGender, db, connection):
    db.execute("""INSERT INTO client(name, birth, gender) VALUES (%s, %s, %s);""", (thisName, thisBirth, thisGender))
    connection.commit()
    return True

def insertPro(thisName, thisBirth, thisGender, db, connection):
    db.execute("""INSERT INTO professional(name, birth, gender) VALUES (%s, %s, %s);""", (thisName, thisBirth, thisGender))
    connection.commit()
    return True

def makeAppointment(thisClientID, thisProID, serviceID, date, observ, db, connection):
    db.execute("""INSERT INTO agendamento(client_id, professional_id, service_id, data, observacao)
                VALUES (%s, %s, %s, %s, %s)""", (thisClientID, thisProID, serviceID, date, observ))
    connection.commit()
    return None


# SELECT 

def selectClient(db):
    db.execute('SELECT id, name FROM client')
    clientList = db.fetchall()
    return clientList

def selectPro(db):
    db.execute('SELECT id, name FROM professional')
    proList = db.fetchall()
    return proList

def selectService(db):
    db.execute('SELECT id, description, price FROM service')
    serviceList = db.fetchall()
    return serviceList

def selectServiceID(id, db):
    db.execute('SELECT description FROM service WHERE id = %s', (id,))
    service = fetchone()
    return service

def proJobList(thisProID, db):
    db.execute("""SELECT agendamento.id, professional.id, professional.name, client.name, service.description, agendamento.data 
                FROM agendamento 
                JOIN professional ON (agendamento.professional_id = professional.id)
                JOIN client ON (agendamento.client_id = client.id)
                JOIN service ON (agendamento.service_id = service.id)
                WHERE
                professional.id = %s
                ORDER BY agendamento.data ASC""", (thisProID,))
    jobList = db.fetchall()
    return jobList

def clientIdValidation(ID, db):
        db.execute('SELECT * FROM client WHERE id = %s;', (ID,))
        client = db.fetchone()

        if client:
            return True
        else:
            return False

def proIdValidation(ID, db):
        db.execute('SELECT * FROM professional WHERE id = %s;', (ID,))
        pro = db.fetchone()

        if pro:
            return True
        else:
            return False

def serviceIdValidation(ID, db):
        db.execute('SELECT * FROM service WHERE id = %s;', (ID,))
        service = db.fetchone()

        if service:
            return True
        else:
            return False

def selectServiceFromClientID(thisClientID, db):
    db.execute(('''SELECT client.name AS cliente, 
                        professional.name AS profissional, 
                        service.description AS serviço,
                        agendamento.data AS data
                FROM agendamento 
                    JOIN client 
                        ON (client.id = client_id)
                    JOIN professional
                        ON (professional.id = professional_id)
                    JOIN service
                        ON (service.id = service_id)
                WHERE 
                    client.id = %s
                ORDER BY agendamento.data ASC'''), (thisClientID,))
    serviceList = db.fetchall()
    return serviceList

# DELETE 

def delElement(jobID, db, connection):
    db.execute('DELETE FROM agendamento WHERE id = %s', (jobID,))
    connection.commit()

# LINKED LIST

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class List:
    def __init__(self):
        self.head = None
        self.size = 0

    def insertNode(self, data):
        if self.head:
            p = self.head
            while p.next:
                p = p.next
            p.next = Node(data)
        else:
            self.head = Node(data)
        self.size += 1

    def trackElem(self, index):
        p = self.head
        for i in range(index):
            if p:
                p = p.next
            else:
                return False
        return p

    def getElem(self, index):
        p = self.trackElem(index)
        if p:
            return p.data
        else:
            return None

    def updateList(self, index, data):
        temp = Node(data)
        if index == 0:
            temp.next = self.head
            self.head = temp
        else:
            p = self.trackElem(index - 1)
            temp.next = p.next
            p.next = temp
        self.size += 1
    
    def remove(self, index):
        p = self.head
        if index == 0 and self.head:
            self.head = self.head.next
            self.size -= 1
        else:
            for i in range(index):
                if p:
                    p = p.next
                else:
                    return False
            a = self.head
            for i in range(index-1):
                if a:
                    a = a.next
                else:
                    return False
            if a.next:
                a.next = p.next
                self.size -= 1
            else:
                return False

# DATE TREATMENT

def dateAdjust(thisYear, thisMonth, thisDay):
    adjustedDate = thisYear+'-'+thisMonth+'-'+thisDay
    return adjustedDate

def valiDate(dateText):
    try:
        datetime.datetime.strptime(dateText, '%Y-%m-%d')
    except:
        print()
        print(" +++ Erro: Data inválida +++ ")
        print()
    else:
        return True

# OTHER FUNCTIONS

def getGender():
    optionGender = 0
    while (optionGender != 1) or (optionGender != 2):
            try:
                optionGender = eval(input('[1] Masculino\n[2] Feminino\n'))
                if optionGender == 1:
                    return 'M'
                    break
                elif (optionGender == 2):
                    return 'F'
                    break
                else:
                    print('Digite uma opção válida')
            except: 
                print('Opção inválida tente novamente.')

def getPersonalData():
    name = input('Digite o nome: ')
    gender = getGender()
    print('Data de nascimento (DD/MM/AAAA): ')
    day = input('DIA: ')
    month = input('MÊS: ')
    year = input('ANO: ')
    birth = dateAdjust(year, month, day)
    if valiDate(birth) == None:
        return
    else:
        return name, birth, gender

def intValidation():
    while True:
            try:
                print()
                value = int(input('Digite a opção desejada\n -> '))
            except ValueError:
                print()
                print('Não entendi. Tente novamente')
                print()
                continue
            if value < 0:
                print('Digite um inteiro positivo.')
            else:
                break
    return value

def mainMenu():
    print('1 - Cadastrar cliente')
    print('2 - Cadastrar profissional')
    print('3 - Agendar serviço')
    print('4 - Selecionar profissional (Implementação de fila)')
    print('5 - Verificar agenda de cliente (Implementação de lista encadeada)')
    print('6 - Sair')

def subMenu():
    print('1 - Verificar fila')
    print('2 - Movimentar fila')
    print('3 - Primeiro elemento')
    print('4 - Quantidade de elementos')
    print('5 - Último elemento')
    print('6 - Voltar ao menu principal')

def linkedListMenu():
    print('1 - Primeiro elemento da lista')
    print('2 - Último elemento')
    print('3 - Quantidade de elementos')
    print('4 - Percorrer lista')
    print('5 - Remover elemento da lista')
    print('6 - Voltar ao menu anterior')
