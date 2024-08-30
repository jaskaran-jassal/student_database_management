from tkinter import *
from tkinter import Toplevel, messagebox
import mysql.connector


def add_functionality():
    def submit_add():
        name_get = name.get()
        roll_no_get = roll_no.get()
        id_get = id.get()
        phone_no_get = phone_no.get()
        email_get = email.get()
        address_get = address.get()
        try:
            mycursor.execute("SELECT * FROM student1 WHERE Roll_no = %s OR id = %s", (roll_no_get, id_get))
            existing_entries = mycursor.fetchall()

            if existing_entries:
                for entry in existing_entries:
                    if entry[1] == roll_no_get:
                        messagebox.showerror('notification',
                                             'Please enter a different roll_no..... this already exists')
                        return
                    if entry[2] == id_get:
                        messagebox.showerror('notification', 'Please enter a different id..... this already exists')
                        return

            # If no duplicates, proceed with insertion
            strr = 'INSERT INTO student1 (Name, Roll_no, id, phone_no, email, address) VALUES (%s, %s, %s, %s, %s, %s)'
            mycursor.execute(strr, (name_get, roll_no_get, id_get, phone_no_get, email_get, address_get))
            con.commit()

            messagebox.showinfo("Notification", f"id {id_get} with name {name_get} added successfully.")

            # Clear the fields
            name.set('')
            roll_no.set('')
            id.set('')
            phone_no.set('')
            email.set('')
            address.set('')

        except mysql.connector.Error as err:
            messagebox.showerror('Database Error', f'Error: {err}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    name = StringVar()
    roll_no = StringVar()
    id = StringVar()
    phone_no = StringVar()
    email = StringVar()
    address = StringVar()

    connect_win = Toplevel()
    connect_win.grab_set()
    connect_win.title('Add student window')
    connect_win.geometry('400x400+400+400')
    connect_win.resizable(False, False)

    name_label = Label(connect_win, text='Name', font=('chiller', 30, 'italic bold'))
    name_label.place(x=20, y=0, width=200, height=50)

    roll_no_label = Label(connect_win, text='Roll_no', font=('chiller', 30, 'italic bold'))
    roll_no_label.place(x=20, y=50, width=200, height=50)

    Id_label = Label(connect_win, text='Id', font=('chiller', 30, 'italic bold'))
    Id_label.place(x=20, y=100, width=200, height=50)

    Phone_no_label = Label(connect_win, text='Phone_no', font=('chiller', 30, 'italic bold'))
    Phone_no_label.place(x=20, y=150, width=200, height=50)

    Email_label = Label(connect_win, text='Email', font=('chiller', 30, 'italic bold'))
    Email_label.place(x=20, y=200, width=200, height=50)

    address_label = Label(connect_win, text='address', font=('chiller', 30, 'italic bold'))
    address_label.place(x=20, y=250, width=200, height=50)

    name_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=name)
    name_label.place(x=250, y=0, width=200, height=50)

    roll_no_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=roll_no)
    roll_no_label.place(x=250, y=50, width=200, height=50)

    Id_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=id)
    Id_label.place(x=250, y=100, width=200, height=50)

    Phone_no_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=phone_no)
    Phone_no_label.place(x=250, y=150, width=200, height=50)

    Email_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=email)
    Email_label.place(x=250, y=200, width=200, height=50)

    address_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=address)
    address_label.place(x=250, y=250, width=200, height=50)

    submit_button = Button(connect_win, text='submit', width=23, font=('chiller', 10, 'italic bold'), relief=RIDGE,
                           borderwidth=4, bg='cyan', command=submit_add)

    submit_button.place(x=100, y=350, width=180, height=50)

    connect_win.mainloop()


def delete_function():
    def submit_delete():
        id_get = id.get()
        if not id_get:
            messagebox.showwarning("Input Error", "Please enter an ID to delete.")
            return

        try:
            # Use parameterized query to prevent SQL injection
            sql_query = 'DELETE FROM student1 WHERE id = %s'
            mycursor.execute(sql_query, (id_get,))
            con.commit()

            # Check if the row was actually deleted
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", f"Student with ID {id_get} deleted successfully.")
            else:
                messagebox.showwarning("Not Found", f"No student found with ID {id_get}.")

        except mysql.connector.Error as err:
            messagebox.showerror('Database Error', f'Error: {err}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    id = StringVar()
    delete_win = Toplevel()
    delete_win.title('delete student window')
    delete_win.grab_set()
    delete_win.geometry('400x200+200+200')

    Id_label = Label(delete_win, text='Id', font=('chiller', 30, 'italic bold'))
    Id_label.place(x=10, y=0, width=200, height=50)

    Id_label = Entry(delete_win, font=('chiller', 30, 'italic bold'), textvariable=id)
    Id_label.place(x=200, y=0, width=200, height=50)

    submit_button = Button(delete_win, text='submit', width=23, font=('chiller', 10, 'italic bold'), relief=RIDGE,
                           borderwidth=4, bg='cyan', command=submit_delete)

    submit_button.place(x=100, y=100, width=180, height=50)

    delete_win.mainloop()


def update_function():
    def update_submit():
        name_get = name.get()
        roll_no_get = roll_no.get()
        id_get = id.get()
        phone_no_get = phone_no.get()
        email_get = email.get()
        address_get = address.get()

        if not id_get:
            messagebox.showwarning("Input Error", "Please enter an ID to update.")
            return

        try:
            # Check if the provided ID exists in the database
            mycursor.execute("SELECT * FROM student1 WHERE id = %s", (id_get,))
            existing_entries = mycursor.fetchall()

            if not existing_entries:
                messagebox.showwarning("Not Found", f"No student found with ID {id_get}.")
                return

            # Build the update query based on which fields are provided
            updates = []
            values = []

            if name_get:
                updates.append("Name = %s")
                values.append(name_get)
            if roll_no_get:
                updates.append("Roll_no = %s")
                values.append(roll_no_get)
            if phone_no_get:
                updates.append("phone_no = %s")
                values.append(phone_no_get)
            if email_get:
                updates.append("email = %s")
                values.append(email_get)
            if address_get:
                updates.append("address = %s")
                values.append(address_get)

            if not updates:
                messagebox.showwarning("Input Error", "Please enter at least one field to update.")
                return

            update_query = "UPDATE student1 SET " + ", ".join(updates) + " WHERE id = %s"
            values.append(id_get)

            mycursor.execute(update_query, tuple(values))
            con.commit()

            messagebox.showinfo("Success", f"Student with ID {id_get} updated successfully.")

        except mysql.connector.Error as err:
            messagebox.showerror('Database Error', f'Error: {err}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')






    name = StringVar()
    roll_no = StringVar()
    id = StringVar()
    phone_no = StringVar()
    email = StringVar()
    address = StringVar()

    connect_win = Toplevel()
    connect_win.grab_set()
    connect_win.title('update student info window')
    connect_win.geometry('400x400+400+400')
    connect_win.resizable(False, False)

    name_label = Label(connect_win, text='Name', font=('chiller', 30, 'italic bold'))
    name_label.place(x=20, y=0, width=200, height=50)

    roll_no_label = Label(connect_win, text='Roll_no', font=('chiller', 30, 'italic bold'))
    roll_no_label.place(x=20, y=50, width=200, height=50)

    Id_label = Label(connect_win, text='Id', font=('chiller', 30, 'italic bold'))
    Id_label.place(x=20, y=100, width=200, height=50)

    Phone_no_label = Label(connect_win, text='Phone_no', font=('chiller', 30, 'italic bold'))
    Phone_no_label.place(x=20, y=150, width=200, height=50)

    Email_label = Label(connect_win, text='Email', font=('chiller', 30, 'italic bold'))
    Email_label.place(x=20, y=200, width=200, height=50)

    address_label = Label(connect_win, text='address', font=('chiller', 30, 'italic bold'))
    address_label.place(x=20, y=250, width=200, height=50)

    name_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=name)
    name_label.place(x=250, y=0, width=200, height=50)

    roll_no_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=roll_no)
    roll_no_label.place(x=250, y=50, width=200, height=50)

    Id_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=id)
    Id_label.place(x=250, y=100, width=200, height=50)

    Phone_no_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=phone_no)
    Phone_no_label.place(x=250, y=150, width=200, height=50)

    Email_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=email)
    Email_label.place(x=250, y=200, width=200, height=50)

    address_label = Entry(connect_win, font=('chiller', 30, 'italic bold'), textvariable=address)
    address_label.place(x=250, y=250, width=200, height=50)

    submit_button = Button(connect_win, text='submit', width=23, font=('chiller', 10, 'italic bold'), relief=RIDGE,
                           borderwidth=4, bg='cyan', command=update_submit)

    submit_button.place(x=100, y=350, width=180, height=50)

    connect_win.mainloop()


def show_function():
    pass


def exit_database():
    res = messagebox.askyesnocancel("Do you want to exit this database")
    if res:
        root.destroy()


def connectDb():
    def sql_connect():
        global mycursor, con
        host = Host_var.get()
        user = user_var.get()
        password = password_var.get()
        host = 'localhost'
        user = 'root'
        password = '232002@Jas'
        print(host, user, password)
        try:
            con = mysql.connector.connect(host=host, user=user, password=password)
            mycursor = con.cursor()
        except:
            messagebox.showerror('notification', 'Please enter correct data')
            return
        try:
            st = 'create database new_connect'
            mycursor.execute(st)
            use = 'use new_connect'
            mycursor.execute(use)
            create = 'create table student1(Name varchar(20) NOT NULL, Roll_no int NOT NULL unique key,id int NOT NULL primary key,phone_no varchar(15) NOT NULL, email varchar(60) NOT NULL, address varchar(50) NOT NULL)'
            mycursor.execute(create)
            messagebox.showinfo('connected', 'now you are connected to the database')

        except:
            use = 'use new_connect'
            mycursor.execute(use)
            messagebox.showinfo('connected', 'ready to use the database')

    Host_var = StringVar()
    user_var = StringVar()
    password_var = StringVar()
    connect_win = Toplevel()
    connect_win.grab_set()
    connect_win.title('Connect window')
    connect_win.geometry('400x400+400+400')
    connect_win.resizable(False, False)
    Host_label = Label(connect_win, text='Host', font=('chiller', 30, 'italic bold'))
    Host_label.place(x=20, y=0, width=200, height=50)

    user_label = Label(connect_win, text='User_name', font=('chiller', 30, 'italic bold'))
    user_label.place(x=20, y=50, width=200, height=50)

    password_label = Label(connect_win, text='Password', font=('chiller', 30, 'italic bold'))
    password_label.place(x=20, y=100, width=200, height=50)

    entry_host = Entry(connect_win, font=('chiller', 30, 'italic bold'), bd=5, textvariable=Host_var)
    entry_host.place(x=250, y=0, width=150, height=50)

    entry_User = Entry(connect_win, font=('chiller', 30, 'italic bold'), bd=5, textvariable=user_var)
    entry_User.place(x=250, y=50, width=150, height=50)

    entry_Pass = Entry(connect_win, font=('chiller', 30, 'italic bold'), bd=5, textvariable=password_var)
    entry_Pass.place(x=250, y=100, width=150, height=50)

    submit_button = Button(connect_win, text='submit', width=23, font=('chiller', 10, 'italic bold'), relief=RIDGE,
                           borderwidth=4, bg='cyan', command=sql_connect)

    submit_button.place(x=100, y=200, width=180, height=50)

    connect_win.mainloop()


root = Tk()
root.title('Student_database')
root.geometry('800x700+10+10')
root.configure(background="red")
root.resizable(False, False)
# ++++++++++++++++++++frames++++++++++++++++++
option_left_frame = Frame(root, bg='white', relief=GROOVE, borderwidth=5)
option_left_frame.place(x=5, y=100, width=300, height=630)

add_button = Button(root, text="Add student", width=23, font=('chiller', 20, 'italic bold'), relief=RIDGE,
                    borderwidth=4, bg='cyan', command=add_functionality)
add_button.place(x=20, y=120, width=180, height=50)

del_button = Button(root, text="Delete student", width=23, font=('chiller', 20, 'italic bold'), relief=RIDGE,
                    borderwidth=4, bg='cyan', command=delete_function)
del_button.place(x=20, y=180, width=180, height=50)

update_button = Button(root, text="Update student", width=23, font=('chiller', 20, 'italic bold'), relief=RIDGE,
                       borderwidth=4, bg='cyan', command=update_function)
update_button.place(x=20, y=250, width=180, height=50)

show_button = Button(root, text="show students", width=23, font=('chiller', 20, 'italic bold'), relief=RIDGE,
                     borderwidth=4, bg='cyan', command=show_function)
show_button.place(x=20, y=320, width=180, height=50)

exit_button = Button(root, text="Exit", width=23, font=('chiller', 20, 'italic bold'), relief=RIDGE, borderwidth=4,
                     bg='cyan', command=exit_database)
exit_button.place(x=20, y=390, width=180, height=50)

option_right_frame = Frame(root, bg='white', relief=GROOVE, borderwidth=5)
option_right_frame.place(x=320, y=100, width=450, height=630)

welcome_label = Label(root, text='Welcome to my student database', font=('chiller', 30, 'italic bold'), relief=RIDGE,
                      borderwidth=4, width=200, bg='cyan')
welcome_label.place(x=100, y=0, width=500, height=50)

connect_button = Button(root, text="Connect to Database", width=23, font=('chiller', 10, 'italic bold'), relief=RIDGE,
                        borderwidth=4, bg='cyan', command=connectDb)
connect_button.place(x=620, y=0, width=180, height=50)
root.mainloop()
