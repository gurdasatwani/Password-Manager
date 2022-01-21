import os, sqlite3, hashlib, uuid
from cryptography.fernet import Fernet
# os for clearing python screen
# sqlite3 for database
# Fernet & hashlib for hashing password
# uuid for hashing id

# all the titles we needed
lst = ["LOGIN", "SIGN UP", "EXIT","ONE", "MANY", "BACK","SHOW", "ADD", "UPDATE", "DELETE","ALL", "ACCOUNT",
"WEBSITE", "USERNAME", "PASSWORD"]

class App:
   def __init__(self):
      # this constructor will make connection to the database
      self.conn = sqlite3.connect("database.db") #database name
      self.cur = self.conn.cursor() #cursor to execute commands
      # creating a database if not exist as maindata & their values
      self.cur.execute("CREATE TABLE IF NOT EXISTS maindata (first_name text,last_name text,username text,password text)")
      # this will commit to the database
      self.conn.commit()
      self.input = lambda: input("\nEnter Number : ")
      self.fnam = None
      self.usn = None
      self.psw = None

   def pmenu(self,lst):
      # this method is for printing menu
      c=0
      for i in lst:
         c+=1
         print(f"\t\t\t  {'-'*16}")
         print("\t", end=f"\t\t  {c} ")
         print(f"| {i}")

   def pt(self, name):
      # this method is for printing title
      print(f"\t\t{'* '*5}PASSWORD MANAGER{' *'*5}\n")
      print(f"\t\t     {'* '*5}{name}{' *'*5}")
   
   def clear(self):
      # this method for clearing screen
      os.system('cls')
   
   def login(self):
      self.clear()
      self.pt(lst[0])
      # taking the username & password of existing user
      print("\n\t\t\t     USERNAME:\n")
      self.usn = input("\t\t\t ● ")
      print("\n\t\t\t     PASSWORD:\n")
      self.psw = input("\t\t\t ● ")
      # try & except for handling indexerror
      try:
         # the below command will check if username exist in maindata or not
         self.cur.execute(f"SELECT * FROM maindata WHERE username = '{self.usn}'")
         data = self.cur.fetchall()[0] #store all the info of the user in the tuple
         if self.MHT(data[3], self.psw):
            self.fnam = data[0]
            Account(data[0], self.usn)
         else:
            print("\n\t\t\t  Wrong password")
      except IndexError:
         print("\n\t\t\t     No Member.")

   def sign_up(self):
      self.clear()
      self.pt(lst[1])
      # taking the first & last name, username, password for the new user
      print("\n\t\t\t     FIRST NAME:\n")
      self.fnam = input("\t\t\t ● ").title()
      print("\n\t\t\t     LAST NAME:\n")
      last_name = input("\t\t\t ● ").title()
      data = self.cur.execute(f"SELECT username FROM maindata")# this command will fetchall the username from maindata
      data2 = []# empty list for adding all usernames in the list
      for i in data:
         data2.append(i[0])# for removing brackets from each username & appending intp data2 list
      while True:# this loop will keep going until there is no same username in the list
         print("\n\t\t\t     USERNAME:\n")
         username = input("\t\t\t ● ")
         if username not in data2 and not username.isdigit():
            self.usn = username
            while True:# this loop will keep going until pw==c_pw
               print("\n\t\t\t     PASSWORD:\n")
               password = input("\t\t\t ● ")
               print("\n\t\t\t     CONFIRM PW:\n")
               confirm_pw = input("\t\t\t ● ")
               if password == confirm_pw:#the below command will add the user into maindata
                  self.psw = password
                  self.cur.execute("INSERT INTO maindata VALUES ((?),(?),(?),(?))",(self.fnam, last_name, self.usn, self.HS(self.psw)))
                  self.conn.commit()#the below command will create a table for the user as their username & their values
                  self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.usn} (website TEXT,username TEXT,password BLOB,key TEXT)")
                  self.conn.commit()
                  Account(self.fnam, self.usn)
                  break
               print("\n\t\t\tPassword Not Match\n\t\t\tEnter Again..")
         else:
            print('\n\t\t\tUsername Not Available or Cannot A Digit..')
   
   def HS(self, P):
      # this method will hash the password with salt & uuid
      salt = uuid.uuid4().hex
      return hashlib.sha256(salt.encode() + P.encode()).hexdigest() + ":" + salt

   def MHT(self, HP, PP):
      # this method will try to match the given password with database hashed password
      HP, salt = HP.split(":")
      return HP == hashlib.sha256(salt.encode() + PP.encode()).hexdigest()
   
   def main(self):
      # the main on which the choices are made
      self.clear()
      print(f"\t\t{'* '*5}PASSWORD MANAGER{' *'*5}")
      self.pmenu(lst[0:3])
      while True:
         choice = self.input()
         if choice in ['1','2','3']:
            if choice == "1":
               self.login()
            elif choice == "2":
               self.sign_up()
            elif choice == "3":
               self.exit()
            break
         else:
            print("\n1 TO 3 ONLY..")

   def exit(self):
      self.clear()
      self.conn.close()
      print("GoodBye...")
      exit()

class Account(App):
   # this class is inherited from the app class
   def __init__(self, name, table):
      super().__init__() #by this we can easily use app class attributes
      self.name = name.upper() #user first name
      self.table = table #username table from maindata
      self.web = lambda: input("\nEnter Website Name : ").title()
      self.user = lambda: input("Enter Username : ")
      self.psw2 = lambda: input("Enter PassWord : ")
      self.main() # calling the main method from app class
   
   def pt(self, name):
      # this method is for printing user's name & title
      print(f"\t\t{'* '*5}{self.name}'s ACCOUNT{' *'*5}\n")
      print(f"\t\t      {'* '*5}{name}{' *'*5}\n")
   
   def encrypt(self,key,text):
      # this method is for encrypting the password with an indivisual key
      fernet = Fernet(key)
      enctext = fernet.encrypt(text.encode())
      return enctext
   
   def decrypt(self,key,Htext):
       # this method is for decrypting the password with an indivisual key
      fernet = Fernet(key)
      dectext = fernet.decrypt(Htext).decode()
      return dectext
   
   def show(self):
      # this method will show all data from username table
      self.clear()
      self.pt(lst[6])#the below command will get all the data of the user
      self.cur.execute(f"SELECT * FROM {self.table}")
      pdata = self.cur.fetchall()
      for i in pdata:# this loop will decrypt all the password from the database
         print(f"\t\t     {i[0]} : {i[1]} {self.decrypt(i[3],i[2])}")

      print(f"\n\t\t\t  {'-'*16}")
      print("\t", end="\t\t  1 ")
      print("| BACK")
      while True:
         choice = self.input()
         if choice == "1":
            self.main()
            break
         else:
            print("\n1 ONLY..")
   
   def addone(self):
      # this method will add the one data at a time
      self.clear()
      website = self.web()
      username = self.user()
      password = self.psw2() #the below command will add data in username table
      key = Fernet.generate_key()
      self.cur.execute(f"INSERT INTO {self.table} VALUES ((?),(?),(?),(?))",(website, username, self.encrypt(key,password),key))
      self.conn.commit()
      self.add()
   
   def addmany(self):
      # this method will add multiple data at a time
      self.clear()
      while True: #this loop will keep going until the user give a correct int input
         try: #try & except for handiling valueerror
            choice = int(input("\nHow Many Records : "))
            self.clear()
            List = [] #empty list for entering the data
            c = choice + 1
            for i in range(choice):
               c -=1
               print(f"{c} More Record To Fill.. ")
               website = self.web()
               username = self.user()
               password = self.psw2()
               key = Fernet.generate_key()
               self.clear()
               data = website, username, self.encrypt(key,password), key
               List.append(data)#entering the data into a list
            self.cur.executemany(f"INSERT INTO {self.table} VALUES ((?),(?),(?),(?))", List)
            # the above command will add multiple data into username table
            self.conn.commit()
            self.add()
         except ValueError:
            print("\nONLY INTERGERS..")
   
   def add(self):
      # main method for adding data
      self.clear()
      self.pt(lst[7])
      self.pmenu(lst[3:6])

      while True:
         choice = self.input()
         if choice in ['1','2','3']:
            if choice == "1":
               self.addone()
            elif choice == "2":
               self.addmany()
            elif choice == "3":
               self.main()
            break
         else:
            print("\n1 TO 3 ONLY..")
   
   def update_web_usn_psw(self, pdata, lst):
      # this method will update the website, username, password
      self.clear()
      for i in pdata:
         print(f"{i[0]} | {i[1]} | {i[2]} | {self.decrypt(i[4],i[3])}")
      while True:# this loop will keep going until the rowid in the lst
         rowid = input("\nEnter Row Id : ")
         if rowid in lst:
            self.clear()
            print('\nweb For (WEBSITE)\nusn For (USERNAME)\n')
            choice = input('What Do You Want To Update: ').lower()
            if choice in ['web','usn']:
               while True:
                  if choice == "web":
                     website = self.web()
                     self.cur.execute(f"UPDATE {self.table} SET website = '{website}' WHERE rowid = {int(rowid)}")
                     break
                  elif choice == "usn":
                     username = self.user()
                     self.cur.execute(f"UPDATE {self.table} SET username = '{username}' WHERE rowid = {int(rowid)}")
                     break
                  # elif choice == "psw":
                  #    password = self.psw2()
                  #    self.cur.execute(f"UPDATE {self.table} SET password = x'{password} WHERE rowid = {int(rowid)}")
                  #    break
                  else:
                     print('\nOnly web, usn')
            self.conn.commit()
            self.update()
            break
         else:
            print("\nNot In The List..")
   
   # def upone(self, pdata, lst):
      # this method will update the whole record (NEED TO WORK ON THIS)
      self.clear()
      for i in pdata:
         print(f"{i[0]} : {i[1]} {i[2]} {i[3]}")
      while True:
         rowid = input("\nEnter Row Id : ")
         if rowid in lst:
            self.clear()
            website = self.web()
            username = self.user()
            password = self.psw2()#the below command will update the whole record
            self.cur.execute(f"UPDATE {self.table} SET website = '{website}',username = '{username}',password = '{password}' WHERE rowid = {int(rowid)}")
            self.conn.commit()
            self.update()
            break
         else:
            print("\nNot In The List..")
   
   # def upmany(self, pdata, lst):
      # this method will update multiple records (NEED TO WORK ON THIS)
      self.clear()
      for i in pdata:
         print(f"{i[0]} : {i[1]} {i[2]} {i[3]}")
      while True:
         try:
            choice = int(input('How Many Records To Update: '))
            c = choice + 1
            for i in range(choice):
               c-=1
               print(f'\n{c} More Records To Update\n')
               rowid = input("\nEnter Row Id : ")
               if rowid in lst:
                  self.clear()
                  website = self.web()
                  username = self.user()
                  password = self.psw2()#the below command will update the whole record
                  self.cur.execute(f"UPDATE {self.table} SET website = '{website}',username = '{username}',password = '{password}' WHERE rowid = {int(rowid)}")
                  self.conn.commit()
               else:
                  print("\nNot In The List..")
            self.update()
            break
         except ValueError:
            print('Only numbers..')
   
   def update_fn_ln_pw(self):
      # this method will update the main data of the user
      self.clear()
      self.cur.execute(f"SELECT * FROM maindata WHERE username = '{self.table}'")
      data = self.cur.fetchall()[0]
      password = self.psw2()#to confirem the user is the owner by asking password
      if self.MHT(data[3], password):
         print(f"{data[0]} | {data[1]} | {data[2]} | {password}")
         while True:
            print('\nfnam For (FIRST NAME)\nlnam For (LAST NAME)\npsw For (PASSWORD)\n')
            choice = input('What Do You Want To Update: ').lower()
            if choice == 'fnam':
               self.name = input('Enter First Name: ').upper()#the below command will update the first name
               self.cur.execute(f"UPDATE maindata SET first_name = '{self.name.title()}'")
               self.conn.commit()
               self.update()
               break
            elif choice == 'lnam':
               last_name = input('Enter Last Name: ').title()#the below command will update the last name
               self.cur.execute(f"UPDATE maindata SET last_name = '{last_name}'")
               self.conn.commit()
               self.update()
               break
            elif choice == 'psw':
               while True:
                  password = input('Enter Password: ')
                  confirm_pw = input('Enter Password to Confirm: ')
                  if password == confirm_pw:
                     self.psw = password#the below command will update the password
                     self.cur.execute(f"UPDATE maindata SET password = '{self.HS(self.psw)}'")
                     self.conn.commit()
                     self.update()
                     break
                  print('The Password Does Not Match Enter Again..')
               break
            else:
               print('Only fnam, lnam, psw')
      else:
         print("\n\t\t\t  Wrong password")

   def update(self):
      # the main method for update menu
      self.clear()
      self.pt(lst[8])
      self.pmenu(['WEB OR USN']+['Main: NAME or PASSWORD']+[lst[5]])
      self.cur.execute(f"SELECT rowid,* FROM {self.table}")
      pdata = self.cur.fetchall()
      rows = []
      for i in pdata:
         rows.append(str(i[0]))
      while True:
         choice = self.input()
         if choice in ["1", "2", "3"]:
            if choice == "1":
               self.update_web_usn_psw(pdata, rows)
            elif choice == "2":
               self.update_fn_ln_pw()
            elif choice == "3":
               self.main()
            break
         else:
            print("\n1 TO 3 ONLY..")
   
   def delone(self, pdata, lst):
      # this method will delete a single value
      self.clear()
      for i in pdata:
         print(f"{i[0]} | {i[1]} | {i[2]} | {self.decrypt(i[4],i[3])}")
      while True:
         rowid = input("\nEnter Row Id : ")
         if rowid in lst:
            self.clear()#the bellow command will delete the value
            self.cur.execute(f"DELETE from {self.table} WHERE rowid = {int(rowid)}")
            self.conn.commit()
            self.delete()
         else:
            print("\nNot In The List..")
   
   def delmany(self, pdata, lst):
      # this method will delete a multiple value
      self.clear()
      for i in pdata:
         print(f"{i[0]} | {i[1]} | {i[2]} | {self.decrypt(i[4],i[3])}")
      while True:
         try:
            choice = int(input("\nHow Many Records : "))
            self.clear()
            List = []
            for i in range(choice):
               rowid = input("\nEnter Row Id : ")
               self.clear()
               if rowid in lst:
                  data = (rowid,)
                  List.append(data)#the bellow command will multiple the value
            self.cur.executemany(f"DELETE from {self.table} WHERE rowid = ?",List)
            self.conn.commit()
            self.delete()
         except ValueError:
            print("\nONLY INTERGERS..")
   
   def delall(self, lst):
      # this method will delete all the values from the table
      self.clear()
      self.cur.execute(f"SELECT * FROM maindata WHERE username = '{self.table}'")
      pdata = self.cur.fetchall()[0]

      while True:
         ask = input("\nEnter PassWord To Confirm : ")
         if self.MHT(pdata[3], ask):
            self.clear()
            List = []
            for i in lst:
               data = (int(i),)
               List.append(data)# the bekow command will delete all the values from the table
            self.cur.executemany(f"DELETE from {self.table} WHERE rowid = ?", List)
            self.conn.commit()
            self.delete()
            break
         else:
            self.delete()
   
   def delacc(self):
      # this method will delete the table from the main database
      self.clear()
      self.cur.execute(f"SELECT * FROM maindata WHERE username = '{self.table}'")
      pdata = self.cur.fetchall()[0]

      while True:
         ask = input("\nEnter PassWord To Confirm : ")
         if self.MHT(pdata[3], ask):
            while True:
               ask2 = input('Are You Sure Type YES To Confirm: ')
               if ask2 == 'YES':
                  self.clear()
                  self.cur.execute(f"DROP TABLE {self.table}")
                  self.conn.commit()#the below command will delete the table from the database
                  self.cur.execute(f"DELETE from maindata WHERE username = '{self.table}'")
                  self.conn.commit()
                  self.exit()
               elif ask2 == 'NO':
                  self.delete()
               print('Only YES or NO..')
         else:
            print('The Password Was Wrong..')
   
   def delete(self):
      # the main method for delete menu
      self.clear()
      self.pt(lst[9])
      self.pmenu(lst[3:5]+lst[10:12]+[lst[5]])
      self.cur.execute(f"SELECT rowid,* FROM {self.table}")
      pdata = self.cur.fetchall()
      rows = []
      for i in pdata:
         rows.append(str(i[0]))

      while True:
         choice = self.input()
         if choice in ['1','2','3','4','5']:
            if choice == "1":
               self.delone(pdata, rows)
            elif choice == "2":
               self.delmany(pdata, rows)
            elif choice == "3":
               self.delall(rows)
            elif choice == "4":
               self.delacc()
            elif choice == "5":
               self.main()
            break
         else:
            print("\n1 TO 5 ONLY...")
   
   def main(self):
      # the main method for the second screen
      self.clear()
      print(f"\t\t{'* '*5}{self.name}'s ACCOUNT{' *'*5}")
      self.pmenu(lst[6:10]+[lst[2]])
      while True:
         choice = self.input()
         if choice in ['1','2','3','4','5']:
            if choice == "1":
               self.show()
            elif choice == "2":
               self.add()
            elif choice == "3":
               self.update()
            elif choice == "4":
               self.delete()
            elif choice == "5":
               self.exit()
            break
         else:
            print("\n1 TO 5 ONLY...")


a = App().main()