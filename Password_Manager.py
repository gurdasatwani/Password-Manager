import os, sqlite3, json, random
from datetime import date, datetime


lst = [
    "LOGIN",
    "SIGN UP",
    "EXIT",
    "ONE",
    "MANY",
    "BACK",
    "SHOW",
    "ADD",
    "UPDATE",
    "DELETE",
    "ALL",
    "ACCOUNT",
    "WEBSITE",
    "USERNAME",
    "PASSWORD",
    "ACTIVITY",
    "BACKUP CODES",
    "FORGET PASSWORD",
]


class App:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS maindata (first_name TEXT,last_name TEXT,username TEXT,password TEXT,activity TEXT,backup_codes TEXT)"
        )
        self.conn.commit()
        self.first_name = None
        self.last_name = None
        self.main_username = None
        self.main_password = None
        self.main_activity = []
        self.backup_codes = []
        self.main_title = "PASSWORD MANAGER"
        self.choice = None
        self.date = date.today().strftime("%b-%d-%Y")
        self.input = lambda: input("\nEnter Number : ")

    def check_usernames(self):
        get_usernames = self.cur.execute(f"SELECT username FROM maindata")
        all_usernames = []
        for username in get_usernames:
            all_usernames.append(username[0])
        return all_usernames

    def adapt_list_to_JSON(self, lst):
        return json.dumps(lst)

    def convert_JSON_to_list(self, data):
        return json.loads(data)

    def get_time(self):
        time = datetime.now().strftime("%H:%M:%S")
        return time

    def get_user_info(self):
        self.cur.execute(
            f"SELECT * FROM maindata WHERE username = '{self.main_username}'"
        )
        return self.cur.fetchall()[0]

    def add_to_activity(self, text):
        if len(self.main_activity) > 15:
            del self.main_activity[14:]

        self.main_activity.insert(0, (self.date, text, self.get_time()))
        self.cur.execute(
            f"UPDATE maindata SET activity = '{self.adapt_list_to_JSON(self.main_activity)}' WHERE username = '{self.main_username}'"
        )
        self.conn.commit()

    def print_title(self, main_title, title):
        print(f"\t\t{'* '*5}{main_title}{' *'*5}\n")
        print(f"\t\t     {'* '*5}{title}{' *'*5}")

    def print_menu(self, lst):
        for n, i in enumerate(lst):
            print(f"\t\t\t  {'-'*16}")
            print("\t", end=f"\t\t  {n+1} ")
            print(f"| {i}")

    def clear(self):
        os.system("cls")

    def generate_backup_codes(self):
        for i in range(5):
            self.backup_codes.append(random.randint(10000, 99999))
        self.cur.execute(
            f"UPDATE maindata SET backup_codes = '{self.adapt_list_to_JSON(self.backup_codes)}' WHERE username = '{self.main_username}'"
        )
        self.conn.commit()

    def msg(self):
        for i in self.backup_codes:
            print(f"\t\t     {i}")
        print(
            "THE ABOVE ARE THE BACKUP CODES IF YOU EVER FORGOT YOUR PASSWORD\nUSE THEM TO RESTORE YOUR ACCOUNT.\nAND REMEMBER EACH CODE CAN ONLY BE USED ONCE.\nSO PLEASE TAKE A SCREENSHOT OR WRITE IT DOWN SOMEWHERE SAFE."
        )

    def login(self):
        self.clear()
        self.print_title(self.main_title, lst[0])
        print("\n\t\t\t     USERNAME:\n")
        self.main_username = input("\t\t\t ● ")
        print("\n\t\t\t     PASSWORD:\n")
        self.main_password = input("\t\t\t ● ")
        try:
            user_info = self.get_user_info()
            if self.main_password == user_info[3]:
                (
                    self.first_name,
                    self.last_name,
                    self.main_activity,
                    self.backup_codes,
                ) = (
                    user_info[:2] + user_info[4:]
                )
                self.main_activity = self.convert_JSON_to_list(self.main_activity)
                self.backup_codes = self.convert_JSON_to_list(self.backup_codes)
                if len(self.backup_codes) == 0:
                    self.clear()
                    self.generate_backup_codes()
                    self.msg()
                    input("\nPRESS ENTER TO CONTINUE")
                Account(
                    self.first_name,
                    self.last_name,
                    self.main_username,
                    self.main_password,
                    self.main_activity,
                    self.backup_codes,
                )
            else:
                print("\n\t\t\t  Wrong password")
        except IndexError:
            print("\n\t\t\t     No Member.")

    def forget_password(self):
        self.clear()
        self.print_title(self.main_title, lst[17])
        print("\n\t\t\t     USERNAME:\n")
        self.main_username = input("\t\t\t ● ")
        print("\n\t\t\t     BACKUP CODE:\n")
        try:
            backup_code = int(input("\t\t\t ● "))
            try:
                user_info = self.get_user_info()
                self.backup_codes = user_info[5]
                self.backup_codes = self.convert_JSON_to_list(self.backup_codes)
                if backup_code in self.backup_codes:
                    (
                        self.first_name,
                        self.last_name,
                        self.main_password,
                        self.main_activity,
                    ) = (
                        user_info[:2] + user_info[3:4] + user_info[4:5]
                    )
                    self.main_activity = self.convert_JSON_to_list(self.main_activity)
                    self.backup_codes.remove(backup_code)
                    if len(self.backup_codes) == 0:
                        self.clear()
                        self.generate_backup_codes()
                        self.msg()
                        input("\nPRESS ENTER TO CONTINUE")
                    Account(
                        self.first_name,
                        self.last_name,
                        self.main_username,
                        self.main_password,
                        self.main_activity,
                        self.backup_codes,
                    )
                else:
                    print("\n\t\t\t  Wrong Backup Code")
            except IndexError:
                print("\n\t\t\t     No Member.")
        except ValueError:
            print("\n\t\t\t     Only Numbers.")

    def sign_up(self):
        self.clear()
        self.print_title(self.main_title, lst[1])
        print("\n\t\t\t     FIRST NAME:\n")
        self.first_name = input("\t\t\t ● ").title()
        print("\n\t\t\t     LAST NAME:\n")
        self.last_name = input("\t\t\t ● ").title()
        while True:
            print("\n\t\t\t     USERNAME:\n")
            self.main_username = input("\t\t\t ● ")
            if (
                self.main_username not in self.check_usernames()
                and not self.main_username.isdigit()
            ):
                while True:
                    print("\n\t\t\t     PASSWORD:\n")
                    self.main_password = input("\t\t\t ● ")
                    print("\n\t\t\t     CONFIRM PW:\n")
                    confirm_pw = input("\t\t\t ● ")
                    if self.main_password == confirm_pw:
                        self.cur.execute(
                            "INSERT INTO maindata VALUES ((?),(?),(?),(?),(?),(?))",
                            (
                                self.first_name,
                                self.last_name,
                                self.main_username,
                                self.main_password,
                                self.adapt_list_to_JSON(self.main_activity),
                                self.adapt_list_to_JSON(self.backup_codes),
                            ),
                        )
                        self.conn.commit()
                        self.cur.execute(
                            f"CREATE TABLE IF NOT EXISTS {self.main_username} (website TEXT,username TEXT,password TEXT)"
                        )
                        self.conn.commit()
                        if len(self.backup_codes) == 0:
                            self.clear()
                            self.generate_backup_codes()
                            self.msg()
                            input("\nPRESS ENTER TO CONTINUE")
                        Account(
                            self.first_name,
                            self.last_name,
                            self.main_username,
                            self.main_password,
                            self.main_activity,
                            self.backup_codes,
                        )
                        break
                    print("\n\t\t\tPassword Not Match\n\t\t\tEnter Again..")
                break
            else:
                print("\n\t\t\tUsername Not Available or Cannot A Digit..")

    def exit(self):
        self.clear()
        self.conn.close()
        print("GoodBye...")
        exit()

    def main(self):
        self.clear()
        print(f"\t\t{'* '*5}PASSWORD MANAGER{' *'*5}")
        self.print_menu(lst[:2] + lst[17:] + lst[2:3])
        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3", "4"]:
                if self.choice == "1":
                    self.login()
                elif self.choice == "2":
                    self.sign_up()
                elif self.choice == "3":
                    self.forget_password()
                elif self.choice == "4":
                    self.exit()
                break
            else:
                print("\n1 TO 3 ONLY..")


class Account(App):
    def __init__(
        self,
        first_name,
        last_name,
        main_username,
        main_password,
        main_activity,
        backup_codes,
    ):
        super().__init__()
        self.user_data = None
        self.first_name = first_name
        self.last_name = last_name
        self.main_username = main_username
        self.main_password = main_password
        self.main_activity = main_activity
        self.backup_codes = backup_codes
        self.main_title = f"{self.first_name.upper()}'s ACCOUNT"
        self.website = None
        self.username = None
        self.password = None
        self.List = []
        self.web = lambda: input("\nEnter Website Name : ").title()
        self.user = lambda: input("\nEnter Username : ")
        self.psw = lambda: input("\nEnter PassWord : ")
        self.add_to_activity("LOGGED IN")
        self.main()

    def get_user_data(self):
        self.cur.execute(f"SELECT rowid,* FROM {self.main_username}")
        self.user_data = self.cur.fetchall()
        return self.user_data

    def show_password(self):
        self.clear()
        for data in self.get_user_data():
            print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")

        print(f"\n\t\t\t  {'-'*16}")
        print("\t", end="\t\t  1 ")
        print("| BACK")
        while True:
            self.choice = self.input()
            if self.choice == "1":
                self.show()
                break
            else:
                print("\n1 ONLY..")

    def show_backup_codes(self):
        self.clear()
        for data in self.backup_codes:
            print(f"\t\t     {data}")

        print(f"\n\t\t\t  {'-'*16}")
        print("\t", end="\t\t  1 ")
        print("| BACK")
        while True:
            self.choice = self.input()
            if self.choice == "1":
                self.show()
                break
            else:
                print("\n1 ONLY..")

    def show(self):
        self.clear()
        self.print_title(self.main_title, lst[6])
        self.print_menu(lst[14:15] + lst[16:17] + lst[5:6])

        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3"]:
                if self.choice == "1":
                    self.show_password()
                elif self.choice == "2":
                    self.show_backup_codes()
                elif self.choice == "3":
                    self.main()
                break
            else:
                print("\n1 TO 3 ONLY..")

    def addone(self):
        self.clear()
        self.website = self.web()
        self.username = self.user()
        self.password = self.psw()
        self.cur.execute(
            f"INSERT INTO {self.main_username} VALUES ((?),(?),(?))",
            (self.website, self.username, self.password),
        )
        self.conn.commit()
        self.add_to_activity("ONE RECORD WAS ADDED")
        self.add()

    def addmany(self):
        self.clear()
        self.List.clear()
        while True:
            try:
                self.choice = int(input("\nHow Many Records : "))
                self.clear()
                c = self.choice + 1
                for i in range(self.choice):
                    c -= 1
                    print(f"{c} More Record To Fill.. ")
                    self.website = self.web()
                    self.username = self.user()
                    self.password = self.psw()
                    self.clear()
                    data = self.website, self.username, self.password
                    self.List.append(data)
                self.cur.executemany(
                    f"INSERT INTO {self.main_username} VALUES ((?),(?),(?))", self.List
                )
                self.conn.commit()
                self.add_to_activity(f"{self.choice} RECORDS WAS ADDED")
                self.add()
            except ValueError:
                print("\nONLY INTERGERS..")

    def add(self):
        self.clear()
        self.print_title(self.main_title, lst[7])
        self.print_menu(lst[3:6])

        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3"]:
                if self.choice == "1":
                    self.addone()
                elif self.choice == "2":
                    self.addmany()
                elif self.choice == "3":
                    self.main()
                break
            else:
                print("\n1 TO 3 ONLY..")

    def update_web_usn_psw(self):
        self.clear()
        self.List.clear()
        for data in self.get_user_data():
            print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")
            self.List.append(data[0])
        while True:
            try:
                rowid = int(input("\nEnter Row Id : "))
                if rowid in self.List:
                    self.clear()
                    print(
                        "\nweb For (WEBSITE)\nusn For (USERNAME)\npsw For (PASSWORD)\n"
                    )
                    self.choice = input("What Do You Want To Update: ").lower()
                    if self.choice in ["web", "usn", "psw"]:
                        while True:
                            if self.choice == "web":
                                self.website = self.web()
                                self.cur.execute(
                                    f"UPDATE {self.main_username} SET website = '{self.website}' WHERE rowid = {rowid}"
                                )
                                self.add_to_activity(
                                    f"ROW ID {rowid} WEBSITE NAME WAS UPDATED"
                                )
                                break
                            elif self.choice == "usn":
                                self.username = self.user()
                                self.cur.execute(
                                    f"UPDATE {self.main_username} SET username = '{self.username}' WHERE rowid = {rowid}"
                                )
                                self.add_to_activity(
                                    f"ROW ID {rowid} USERNAME WAS UPDATED"
                                )
                                break
                            elif self.choice == "psw":
                                self.password = self.psw()
                                self.cur.execute(
                                    f"UPDATE {self.main_username} SET password = '{self.password}' WHERE rowid = {rowid}"
                                )
                                self.add_to_activity(
                                    f"ROW ID {rowid} PASSWORD WAS UPDATED"
                                )
                                break
                            else:
                                print("\nOnly web, usn, psw")
                    self.conn.commit()
                    self.update()
                    break
                else:
                    print("\nNot In The List..")
            except ValueError:
                print("\nNot In The List..")

    def upone(self):
        self.clear()
        self.List.clear()
        for data in self.get_user_data():
            print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")
            self.List.append(data[0])
        while True:
            try:
                rowid = int(input("\nEnter Row Id : "))
                if rowid in self.List:
                    self.clear()
                    self.website = self.web()
                    self.username = self.user()
                    self.password = self.psw()
                    self.cur.execute(
                        f"UPDATE {self.main_username} SET website = '{self.website}',username = '{self.username}',password = '{self.password}' WHERE rowid = {rowid}"
                    )
                    self.conn.commit()
                    self.add_to_activity(f"ROW ID {rowid} WHOLE RECORD WAS UPDATED")
                    self.update()
                    break
                else:
                    print("\nNot In The List..")
            except ValueError:
                print("/nOnly Numbers..")

    def upmany(self):
        self.clear()
        self.List.clear()
        for data in self.get_user_data():
            print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")
            self.List.append(data[0])
        while True:
            try:
                self.choice = int(input("How Many Records To Update: "))
                c = self.choice + 1
                for i in range(self.choice):
                    c -= 1
                    print(f"\n{c} More Records To Update\n")
                    try:
                        rowid = int(input("\nEnter Row Id : "))
                        if rowid in self.List:
                            self.clear()
                            self.website = self.web()
                            self.username = self.user()
                            self.password = self.psw()
                            self.cur.execute(
                                f"UPDATE {self.main_username} SET website = '{self.website}',username = '{self.username}',password = '{self.password}' WHERE rowid = {rowid}"
                            )
                            self.add_to_activity(
                                f"ROW ID {rowid} WHOLE RECORD WAS UPDATED"
                            )
                            self.conn.commit()
                        else:
                            print("\nNot In The List..")
                    except ValueError:
                        print("\nOnly Numbers..")
                self.update()
                break
            except ValueError:
                print("Only numbers..")

    def update_fn_ln_pw(self):
        self.clear()
        password = self.psw()
        if password == self.main_password:
            print(
                f"{self.first_name} | {self.last_name} | {self.main_username} | {self.main_password}"
            )
            while True:
                print(
                    "\nfnam For (FIRST NAME)\nlnam For (LAST NAME)\npsw For (PASSWORD)\n"
                )
                self.choice = input("What Do You Want To Update: ").lower()
                if self.choice == "fnam":
                    self.first_name = input("Enter First Name: ").title()
                    self.main_title = f"{self.first_name.upper()}'s ACCOUNT"
                    self.cur.execute(
                        f"UPDATE maindata SET first_name = '{self.first_name}'"
                    )
                    self.add_to_activity("FIRST NAME WAS UPDATED")
                    break
                elif self.choice == "lnam":
                    self.last_name = input("Enter Last Name: ").title()
                    self.cur.execute(
                        f"UPDATE maindata SET last_name = '{self.last_name}'"
                    )
                    self.add_to_activity("LAST NAME WAS UPDATED")
                    break
                elif self.choice == "psw":
                    while True:
                        self.main_password = input("Enter Password: ")
                        confirm_pw = input("Enter Password to Confirm: ")
                        if self.main_password == confirm_pw:
                            self.cur.execute(
                                f"UPDATE maindata SET password = '{self.main_password}'"
                            )
                            self.add_to_activity("MAIN PASSWORD WAS UPDATED")
                            break
                        print("The Password Does Not Match Enter Again..")
                    break
                else:
                    print("Only fnam, lnam, psw")
            self.conn.commit()
            self.update()
        else:
            print("\n\t\t\t  Wrong password")

    def update(self):
        self.clear()
        self.print_title(self.main_title, lst[8])
        self.print_menu(
            ["WEB OR USN OR PSW"] + lst[3:5] + ["Main: NAME or PASSWORD"] + [lst[5]]
        )
        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3", "4", "5"]:
                if self.choice == "1":
                    self.update_web_usn_psw()
                elif self.choice == "2":
                    self.upone()
                elif self.choice == "3":
                    self.upmany()
                elif self.choice == "4":
                    self.update_fn_ln_pw()
                elif self.choice == "5":
                    self.main()
                break
            else:
                print("\n1 TO 3 ONLY..")

    def activity_(self):

        self.clear()
        self.print_title(self.main_title, lst[15])

        for data in self.main_activity:
            print(f"\t\t     {data[0]} | {data[1]} | {data[2]}")

        print(f"\n\t\t\t  {'-'*16}")
        print("\t", end="\t\t  1 ")
        print("| BACK")
        while True:
            self.choice = self.input()
            if self.choice == "1":
                self.main()
                break
            else:
                print("\n1 ONLY..")

    def delone(self):
        self.clear()
        self.List.clear()
        for data in self.get_user_data():
            print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")
            self.List.append(data[0])
        while True:
            try:
                rowid = int(input("\nEnter Row Id : "))
                if rowid in self.List:
                    self.clear()
                    self.cur.execute(
                        f"DELETE from {self.main_username} WHERE rowid = {rowid}"
                    )
                    self.add_to_activity(f"ROW ID {rowid} WAS DELETED")
                    self.conn.commit()
                    self.delete()
                else:
                    print("\nNot In The List..")
            except ValueError:
                print("\nOnly Numbers..")

    def delmany(self):
        self.clear()
        while True:
            try:
                self.choice = int(input("\nHow Many Records : "))
                self.clear()
                for i in range(self.choice):
                    self.List.clear()
                    for data in self.get_user_data():
                        print(f"\t\t     {data[0]} : {data[1]} {data[2]} {data[3]}")
                        self.List.append(data[0])
                    try:
                        rowid = int(input("\nEnter Row Id : "))
                        self.clear()
                        if rowid in self.List:
                            self.add_to_activity(f"ROW ID {rowid} WAS DELETED")
                            self.cur.execute(
                                f"DELETE from {self.main_username} WHERE rowid = {rowid}"
                            )
                            self.conn.commit()
                        else:
                            print("\nNot In The List..")
                    except ValueError:
                        print("\nOnly Numbers..")
                self.delete()
            except ValueError:
                print("\nONLY INTERGERS..")

    def delall(self):
        self.clear()
        self.List.clear()
        for data in self.get_user_data():
            self.List.append((data[0],))
        while True:
            ask = input("\nEnter PassWord To Confirm : ")
            if ask == self.main_password:
                self.clear()
                self.cur.executemany(
                    f"DELETE from {self.main_username} WHERE rowid = (?)", self.List
                )
                self.conn.commit()
                self.add_to_activity("ALL THE RECORDS WAS DELETED")
                self.delete()
                break
            else:
                self.delete()

    def delacc(self):
        self.clear()
        while True:
            ask = input("\nEnter PassWord To Confirm : ")
            if ask == self.main_password:
                while True:
                    ask2 = input("Are You Sure Type YES To Confirm: ")
                    if ask2 == "YES":
                        self.clear()
                        self.cur.execute(f"DROP TABLE {self.main_username}")
                        self.cur.execute(
                            f"DELETE from maindata WHERE username = '{self.main_username}'"
                        )
                        self.conn.commit()
                        self.exit()
                    elif ask2 == "NO":
                        self.delete()
                    else:
                        print("Only YES or NO..")
            else:
                print("The Password Was Wrong..")

    def delete(self):
        self.clear()
        self.print_title(self.main_title, lst[9])
        self.print_menu(lst[3:5] + lst[10:12] + [lst[5]])

        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3", "4", "5"]:
                if self.choice == "1":
                    self.delone()
                elif self.choice == "2":
                    self.delmany()
                elif self.choice == "3":
                    self.delall()
                elif self.choice == "4":
                    self.delacc()
                elif self.choice == "5":
                    self.main()
                break
            else:
                print("\n1 TO 5 ONLY...")

    def main(self):
        self.clear()
        print(f"\t\t{'* '*5}{self.main_title}{' *'*5}")
        self.print_menu(lst[6:10] + [lst[15]] + [lst[2]])
        while True:
            self.choice = self.input()
            if self.choice in ["1", "2", "3", "4", "5", "6"]:
                if self.choice == "1":
                    self.show()
                elif self.choice == "2":
                    self.add()
                elif self.choice == "3":
                    self.update()
                elif self.choice == "4":
                    self.delete()
                elif self.choice == "5":
                    self.activity_()
                elif self.choice == "6":
                    self.add_to_activity("LOGGED OUT")
                    self.exit()
                break
            else:
                print("\n1 TO 5 ONLY...")


App().main()
