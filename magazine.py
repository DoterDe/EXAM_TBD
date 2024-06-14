
from multiprocessing import Value
import psycopg2
import re

class Database_manager:
    def __init__(self , dbname , host , port, user  , password):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(dbname = self.dbname,host =self.host,port =self.port,user= self.user,password = self.password)

        except Exception as e:
            print(f'Connection refused {e}')
        else:
            self.cursor = self.connection.cursor()

    def insert(self, table_name , **kwargs):
        columns = ', '.join([column for column in kwargs.get('colums', [])])
        values = ', '.join([f"'{column}'" if type(column) == str else f'{column}' for column in kwargs.get('values', [])])
        
        query = f"""INSERT INTO {table_name} ({columns}) values ({values})"""
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as error:
            print(f'Something gone wronge : {error}')

    def select_all(self, table_name):
        query = f'SELECT * FROM {table_name}'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Something gone wronge : {e}')

    def select(self, table , columns, name): 
        query = f"SELECT {columns} FROM {table} Where name = '{name}'"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Something gone wronge : {e}')
    def delete(self, table_name, id):
        if id:
            query = f"DELETE FROM {table_name} WHERE name = '{id}'"
            try:
                self.cursor.execute(query)
                self.connection.commit()
            except Exception as e:
                print(f'Something gone wronge : {e}')
        else:
            print('you must say id')

    def update(self, table, column, value, id):
        query= f"update {table} set {column} = '{value}' where name = '{id}'"
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as e:
            print(f'Error: {e}')

db = Database_manager('magazine' , 'localhost', 5432, 'postgres', 'postgres')
db.connect()


while True:
    menu = int(input(f'Hello my friend , you on magazine_app cait.Choice what you want do : \n 1) Login as admin\n 2) Login as a user  \n 3) Create magazine  \n  '))
    if menu == 2:
        task = int(input(f'Choice what you want do : \n 1) Create user\n 2) Update user \n 3) Subscribe a user to the magazine newsletter \n 4) Delete user '))
        if task == 1:
            name = input('введите имя: ')
            surname = input('введите фамилию: ')
            email = input('введите email: ')
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            re.match(regex, email)
            age = int(input('введите сколько вам лет: '))
            db.insert('users', colums = ['name', 'surname', 'email','age'] , values = [f'{name}', f'{surname}', f'{email}', age])
            id = db.select('users', 'id', f'{name}' )
            print(f'user created !!! , your id = {id}')
        elif task == 2:
            name = input('введите имя акаунта для изменения: ')
            while True:
                columns = input('введите что вы хотите изменить или напишите exit: ')
                if columns == 'exit':
                    break
                values = input('введите изменения: ')
                db.update('users', column = f'{columns}', value=f'{values}',id= f'{name}')
                print('user udated !!!')
        elif task == 3:
            id= int(input('введите айди сказанный вам при создании акаунта : '))
            magazines = db.select_all('magazines')
            if magazines == []:
                print('На данный момент нет журналов ')
            else:
                print(magazines)
            magazines_id = int(input('введите ваш выбор назвав айди : '))
            db.insert('subscriptions', colums = ['id_user', 'id_magazine'] , values = [id, magazines_id])
            print('Теперь вы привязанны к этому журналу УСПЕШНО !!!')

        elif task == 4:
            name = input('введите имя акаунта для удаления: ')
            db.delete('users', id = f'{name}')
            print('Акаунт удален !!!')
    if menu == 1:
        admin = db.select_all('users')
        print(admin)
    if menu ==3:
        title = input('введите название : ')
        description = input('введите описание : ')
        date_created = input('введите дату в форме **-**-****: ')
        db.insert('magazines', colums= ['title', 'description', 'date_created'], values=[f'{title}', f'{description}', f'{date_created}'])
        print('Созданно кайф !!!')
                



