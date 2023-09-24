
# 19th Sept '23
# Sachin
# Employee Management Program ( EMP )

import mysql.connector as mysql


class emp:

    __rootUser = ''
    __rootUserPass = ''
    cur = ''
    cnx = ''


    # program driven code    
    def mainEntry(self):
        self.decor()
        feed = input("Feed \'login' to root-user login while \'signup' to create new root-user = ")
        dept = []
        
        if feed == 'login': 
            self.decor()
            self.rootUserLogin(self.cnx, self.cur)
            dept = self.deptBasedTableAllocation(self.cnx, self.cur)

            self.loginOptions(dept)

        elif feed == 'signup':
            self.signupOptions()

        else: 
            print('Forgot password')

        ch = 1
        while ch == 1:
            ch = int(input("Enter \'1' to display options while \'0' to exit = "))
            if ch == 1:
                self.loginOptions(dept)

            elif ch == 0:
                self.decor()
                print('You exited program successfully!')
                self.decor()

                self.cur.close()
                self.cnx.close()
                exit(0)



    # establishes cnx to mysql database on object initialization
    def connect(self):
        login = {
            'host' : 'localhost',
            'user':'root',
            'passwd' : 'root',
            'database' : 'empdb'
        }

        self.cnx = mysql.connect(**login)
        self.cur = self.cnx.cursor() 

        return self.cnx, self.cur

    

    # to login into existing rootuser
    def loginOptions(self, dept):
        # self.decor()
        # dept = self.deptBasedTableAllocation(self.cnx, self.cur)
            
        self.options()

        ch = int(input('Enter your choice = '))
        self.decor()

        if ch == 1:
            self.connect()
            self.insertRecords(self.cnx, self.cur, dept)
            self.decor()
                
        elif ch == 2:
            self.connect()
            self.addNewColumn(self.cnx, self.cur, dept)
            self.decor()

        elif ch == 3:
            self.connect()
            self.delExistingColumns(self.cnx, self.cur, dept)
            self.decor()

        elif ch == 4:
            self.connect()
            self.delExistingRecords(self.cnx, self.cur, dept)
            self.decor()

        elif ch == 5:
            pass
            self.connect()
            self.decor()

        elif ch == 6:
            self.connect()
            self.fetchExistingRecords(self.cnx, self.cur, dept)
            self.decor()

        else:
            print('Invalid option!')
            self.decor()



    # to register for new rootuser
    def signupOptions(self):
            self.decor()
            self.createNewRootUser(self.cnx, self.cur)
            self.rootUserLogin(self.cnx, self.cur)
            dept = self.deptBasedTableAllocation(self.cnx, self.cur)
            self.insertRecords(self.cnx, self.cur, dept)



    # root user login func
    def rootUserLogin(self, cnx, cur):
        self.__rootUser = input('Enter root User-ID = ')
        self.__rootUserPass = input("Enter root User-Password = ")

        tempList = self.__rootUser, self.__rootUserPass
        self.cur.execute('select username from rootusers where username = %s and password = %s;', tempList)
        returnedUser = self.cur.fetchall()
        
        self.cur.execute('select password from rootusers where username = %s and password = %s;', tempList)
        returnedPass = self.cur.fetchall()
        
        for i in range(len(returnedUser)):
            for j in range(len(returnedUser[i])):
                if self.__rootUser == returnedUser[i][j] and self.__rootUserPass == returnedPass[i][j]:
                    self.decor()
                    print(f'Session started for {self.__rootUser}!')
                    self.decor()



    # to create new root user 
    def createNewRootUser(self, cnx, cur):
        self.__rootUser = input('Enter root User-ID = ')
        self.__rootUserPass = input("Enter root User-Password = ")

        tempList = self.__rootUser, self.__rootUserPass
        self.cur.execute('select username from rootusers where username = %s and password = %s;', tempList)
        returnedUser = self.cur.fetchall()
        
        self.cur.execute('select password from rootusers where username = %s and password = %s;', tempList)
        returnedPass = self.cur.fetchall()

        dept = input("Enter department name = ")
        tempList = self.__rootUser, self.__rootUserPass, dept
        operation = 'insert into rootusers(username, password, dept) values(%s, %s, %s); commit;'
        self.cur.execute(operation, tempList)
        self.decor()
        print("New root user successfully registered!")
        self.decor()
        cur.close()

                

    # to create dept based table if not exists
    def deptBasedTableAllocation(self, cnx, cur):
        cnx, cur = self.connect()
        operation = 'show tables;'
        cur.execute(operation)
        tableList = cur.fetchall()
        # print(tableList)

        tempList = self.__rootUser, self.__rootUserPass

        cur.execute('select dept from rootusers where username = %s and password = %s;', tempList)
        returnedDept = cur.fetchall()

        i = 0
        while i <= len(tableList):
            if returnedDept[0][0] != tableList[i][0]:
                # print(tableList[i][0])
                if i == len(tableList):
                    cur.execute(f'create table if not exists {returnedDept[0][0]} ( id int not null primary key, empname varchar(30), language varchar(15));')
                    print('Table created successfully!')

            else:
                print(f"Department table related to root-user \'{self.__rootUser}' exists!")
                break

            i += 1

        return returnedDept



    # to insert records into table
    def insertRecords(self, cnx, cur, returnedDept):
        ch = 1
        count = 0
        
        # to return the latest row number
        cur.execute(f'select max(id) from {returnedDept[0][0]};')
        tempCurrRow = cur.fetchone()
        currRow = []

        if tempCurrRow[0] == None:
            currRow.append(0)
        
        else:
            currRow = tempCurrRow 

        values = []  # empty list
        while ch != 0:
            print(f"Insert the {currRow[0] + 1 + count}th employee details for {returnedDept[0][0]} table ->")
            self.decor()
            tp = tuple(((currRow[0] + 1 + count), input('Name = '), input("Language = "))) # tuple
            values.append(tp)  # list of tuples
            count += 1
            # print(values)
            self.decor()
            ch = int(input("Enter 1 to continue and 0 to terminate insertion = "))
            self.decor()

        operation = f'insert into {returnedDept[0][0]} (id, empname, language) values(%s, %s, %s); commit;'
        self.cur.executemany(operation, values)
        
        print(f'{count} record(s) inserted successfully!')

        cur.close()
        


    # to add new column to table schema
    def addNewColumn(self, cnx, cur, dept):
        print(f'To add new column to \"{dept[0][0]}" table, enter ->')
        self.decor()
        
        a, b, c = input('Column name = '), input('Column type = '), int(input('Column size = '))
        
        if b == 'int':
            tp = (a, b)
            values = []
            values.append(tp)

            operation = f'alter table {dept[0][0]} add column {values[0][0]} {values[0][1]};'
            cur.execute(operation)
            print(f'Column {a} added successfully!')

        elif b == 'char' or b == 'varchar':
            tp = (a, b, c)
            values = []
            values.append(tp)

            operation = f'alter table {dept[0][0]} add column {values[0][0]} {values[0][1]} ({values[0][2]});'
            cur.execute(operation)
            print(f'Column {a} added successfully!')
            
        else:
            print(f'Invalid datatype for column {a}!')
        
        cur.close()



    # to delete or drop existing column from schema
    def delExistingColumns(self, cnx, cur, dept):
        print(f'To delete existing column from \"{dept[0][0]}" table, enter ->')
        self.decor()

        a = input("Column name = ")

        cur.execute(f'alter table {dept[0][0]} drop column {a};')
        columnNames = self.cur.column_names
        
        if a not in columnNames:
            self.decor()
            print(f'Column \"{a}" deleted successfully!')

        cur.close()



    # to delete existing records from table
    def delExistingRecords(self, cnx, cur, dept):
        print(f'To delete existing records from \"{dept[0][0]}" table, enter ->')
        self.decor()

        ch = input("To delete all records, enter \'0' while \'1' for specific record(s) = ")

        if ch == '0':
            cur.execute(f'delete from {dept[0][0]}; commit;')
            
            self.decor()
            print(f'Specified records deleted successfully!')   

        
        if ch == '1':
            condn = input('Enter specific conition to delete record(s) = ')
            
            cur.execute(f'select id from {dept[0][0]} where {condn};')
            condnSatisfyingRowsIdList = cur.fetchall()
            print(condnSatisfyingRowsIdList)

            cur.execute(f'select id from {dept[0][0]};')
            allRowsIdList = cur.fetchall()
            print(allRowsIdList)

            cur.execute(f'delete from {dept[0][0]} where {condn}; commit;')

            for i in range(len(allRowsIdList)):
                for j in range(len(condnSatisfyingRowsIdList)): 
                    
                    if allRowsIdList[i][0] != condnSatisfyingRowsIdList[j][0]:
                        if i == len(allRowsIdList) - 1:
                            self.decor()
                            print(f'Specified records deleted successfully!')   

        cur.close()


    # to fetch existing records from table
    def fetchExistingRecords(self, cnx, cur, dept):
        print(f'To retrieve existing records from \"{dept[0][0]}" table, enter ->')
        self.decor()

        ch = input("To retrieve all records, enter \'0' while \'1' for specific record(s) = ")
        self.decor()

        # to print column headings ( local method )
        def printfields(rfields):  
            for j in range(len(rfields)):
                print(f'{rfields[j]}', end='')

                if j < len(rfields) - 1:
                        print(end='  -  ')

                if j == len(rfields) - 1:
                        print()

        # to print rows ( local method )
        def printrecords(rrecords):
            for i in range(len(rrecords)):
                for j in range(len(rrecords[0])):
                    print(f' {rrecords[i][j]}', end='')

                    if j < len(rrecords[0]) - 1:
                        print(end='  -  ')

                    if j == len(rrecords[0]) - 1:
                        print()


        if ch == '0':
            cur.execute(f'select * from {dept[0][0]};')
            returnedRows = cur.fetchall()
            returnedFields = cur.column_names

            printfields(returnedFields)
            printrecords(returnedRows)

            self.decor()
            print(f'{cur.rowcount} record(s) returned successfully!')   

        
        if ch == '1':
            self.decor()
            ch = input("Enter \'0' to retrieve rows for specific condition while\n      \'1' for specific column = ")
            self.decor()

            if ch == '0':
                condn = input('Enter condition to retrieve all records = ')
                cur.execute(f'select * from {dept[0][0]} where {condn};')
                returnedRows = cur.fetchall()
                returnedFields = cur.column_names
                self.decor()

                printfields(returnedFields)
                printrecords(returnedRows)

                self.decor()
                print(f'{cur.rowcount} record(s) returned successfully!')   


            elif ch == '1':
                enterdColumns = input('Enter column names = ')
                condn = input('Enter condition = ')

                if condn == 'none':
                    cur.execute(f'select {enterdColumns} from {dept[0][0]};')
                    returnedRows = cur.fetchall()

                else:
                    cur.execute(f'select {enterdColumns} from {dept[0][0]} where {condn};')
                    returnedRows = cur.fetchall()
                    
                returnedFields = cur.column_names
                
                self.decor()
                printfields(returnedFields)
                printrecords(returnedRows)

                self.decor()
                print(f'{cur.rowcount} record(s) returned successfully!')  

        cur.close()



    # to print options for operations
    def options(self):
        self.decor()
        print('Enter 1 to insert records.            2 to add new column to table schema.')
        print('      3 to delete existing column.    4 to delete existing record.')
        print('      5 to update records.            6 to fetch records.')
        self.decor()



    # used for decorating print statements
    def decor(self):
        print('\n********************************************************************************************')
        print('********************************************************************************************\n')
        



if '__main__':
    
    obj = emp()
    obj.connect()
    obj.mainEntry()



