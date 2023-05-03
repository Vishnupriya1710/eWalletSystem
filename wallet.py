import tkinter as tk 
from tkinter import *
from tkinter import ttk 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
# from py_mainform import mainform
import mysql.connector
from datetime import datetime, timedelta
import string
import random
from decimal import Decimal
from tkcalendar import DateEntry

root = Tk()
connection = mysql.connector.connect(host='localhost', user='root', port='3306', password='******', database='EWALLET')
c = connection.cursor()

# width and height
w = 450
h = 525
# background color
bgcolor = "#bdc3c7"
global usersession

# ----------- CENTER FORM ------------- #
root.overrideredirect(1) # remove border
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws-w)/2
y = (hs-h)/2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

def incompleteTxn_handling():
    select_query = "UPDATE `send_transaction` SET Cancel_Reason = 'Transaction exceeded 15 days' WHERE datediff(current_timestamp(),Date_Initiated) > 15 and Date_Completed IS NULL;"
    c.execute(select_query)
    connection.commit()
   
print("Let's begin!")
incompleteTxn_handling()


# ----------- HEADER ------------- #

headerframe = tk.Frame(root, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg='#95a5a6', width=w, height=70)
titleframe = tk.Frame(headerframe, bg='yellow', padx=1, pady=1)
title_label = tk.Label(titleframe, text='Login', padx=20, pady=5, bg='green', fg='#fff', font=('Tahoma',24), width=8)
close_button = tk.Button(headerframe, text='x', borderwidth=1, relief='solid', font=('Verdana',12))

headerframe.pack()
titleframe.pack()
title_label.pack()
close_button.pack()

titleframe.place(y=26, relx=0.5, anchor=CENTER)
close_button.place(x=410, y=10)

# close window
def close_win():
    root.destroy()

close_button['command'] = close_win

# ----------- END HEADER ------------- #

mainframe = tk.Frame(root, width=w, height=h)

# ----------- Login Page ------------- #
loginframe = tk.Frame(mainframe, width=w, height=h)
login_contentframe = tk.Frame(loginframe, padx=30, pady=100, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

username_label = tk.Label(login_contentframe, text='Username:', font=('Verdana',16), bg=bgcolor)
password_label = tk.Label(login_contentframe, text='Password:', font=('Verdana',16), bg=bgcolor)

username_entry = tk.Entry(login_contentframe, font=('Verdana',16))
password_entry = tk.Entry(login_contentframe, font=('Verdana',16), show='*')

login_button = tk.Button(login_contentframe,text="Login", font=('Verdana',16), bg='#2980b9',fg='#fff', padx=25, pady=10, width=25)

go_register_label = tk.Label(login_contentframe, text=">> don't have an account? create one" , font=('Verdana',10), bg=bgcolor, fg='red')

mainframe.pack(fill='both', expand=1)
loginframe.pack(fill='both', expand=1)
login_contentframe.pack(fill='both', expand=1)

username_label.grid(row=0, column=0, pady=10)
username_entry.grid(row=0, column=1)

password_label.grid(row=1, column=0, pady=10)
password_entry.grid(row=1, column=1)

login_button.grid(row=2, column=0, columnspan=2, pady=40)

go_register_label.grid(row=3, column=0, columnspan=2, pady=20)

# create a function to display the register frame
def go_to_register():
    loginframe.forget()
    registerframe.pack(fill="both", expand=1)
    title_label['text'] = 'Register'
    title_label['bg'] = '#27ae60'

go_register_label.bind("<Button-1>", lambda page: go_to_register())

def loginAuth(username, password):
    global usersession
    global sessionssn
    vals = (username,password,)
    select_query = "SELECT ssn FROM `user_account` WHERE `username` = %s AND `password` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        usersession = username
        sessionssn = user[0]
        return True
    else:
        usersession = ""
        return False

def checkOtp():
    otp = otpvalue.get().strip()
    print(otp)
    if otp=="123456":
        vals = (sessionssn,)
        select_query = "UPDATE USER_ACCOUNT SET PBAVERIFIED=1 WHERE SSN = %s"
        c.execute(select_query, vals)
        connection.commit()
        result = c.fetchone()
        # getAccountInfo(usersession)
        otpframe = Toplevel(verifyElec_frame)
        otpframe.geometry('600x600')
        e=Label(otpframe,width=30,text='Account Verified Successfully!').pack()
        tk.Button(otpframe, name="ok", text="OK", font=('Verdana',8), command=mainMenu(event="")).pack()
        otpframe.withdraw()
    else:
        verifyElec()
    return TRUE

def verifyElec():
    global otpvalue
    global verifyElec_frame
    verifyElec_frame = Toplevel(verifyFrame)
    verifyElec_frame.geometry('500x500')
    tk.Label(verifyElec_frame,text='Enter the OTP :', font=('Verdana',14)).grid(row=0,column=0)
    otpvalue = tk.Entry(verifyElec_frame,font=('Verdana',14), width=10)
    otpvalue.grid(row=0,column=1)
    tk.Button(verifyElec_frame, name="ok2", text="OK", font=('Verdana',8), command=checkOtp).grid(row=1)

def verify():
    global elecAddr
    global elecAddr_entry_phoneno
    global elecAddr_entry_email
    global verifyFrame
    vals = (usersession,)
    select_query = "SELECT pbaverified FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(select_query, vals)
    result = c.fetchone()
    pbaverifiedFlag = result[0]
    if pbaverifiedFlag:
        msg1 = Toplevel(accountInfo)
        msg1.geometry('300x300')
        e=Label(msg1,width=30,text='Account is already verified')
        e.pack()
    else:
        verifyFrame = Toplevel(accountInfo)
        verifyFrame.geometry('600x600')
        e=Label(verifyFrame,width=30,text='Choose to verify',background='yellow')
        e.grid(row=3)
        radiosframe = tk.Frame(verifyFrame)
        elecAddr = StringVar()
        elecAddr.set('PhoneNo')
        phonenum_radiobutton = tk.Radiobutton(verifyFrame, text='Phone Number', font=('Verdana',14), bg=bgcolor, variable=elecAddr, value='PhoneNo')
        email_radiobutton = tk.Radiobutton(verifyFrame, text='Email Address', font=('Verdana',14), bg=bgcolor, variable=elecAddr, value='Email')
        phonenum_radiobutton.grid(row=4,column=0)
        email_radiobutton.grid(row=5,column=0)
        elecAddr_entry_phoneno = tk.Entry(verifyFrame, font=('Verdana',14), width=22)
        elecAddr_entry_phoneno.grid(row=4,column=1)
        elecAddr_entry_email = tk.Entry(verifyFrame, font=('Verdana',14), width=22)
        elecAddr_entry_email.grid(row=5,column=1)
        tk.Button(verifyFrame, name="ok1", text="OK", font=('Verdana',8), command=verifyElec).grid(row=6)

def statementMenu():
    Button(statement_frame, text = "Total amount of money sent by a user in a range of dates",command=total_amount_sent_by_user_in_date_range).pack()
    Button(statement_frame, text = "Total amount of money received by a user in a range of dates",command=total_amount_received_by_user_in_date_range).pack()
    Button(statement_frame, text = "Total & average amount of money sent by a user per month",command=monthlyStatSent).pack()
    Button(statement_frame, text = "Total & average amount of money received by a user per month",command=monthlyStatRcvd).pack()
    # Button(statement_frame, text = "Transactions with the maximum amount of money per month").pack()
    Button(statement_frame, text = "Best users",command=bestUsers).pack()

def bestUsers():
    global stmtOp6
    stmtOp6 = Toplevel(statement_frame)
    stmtOp6.geometry('900x900')
    query="CREATE OR REPLACE VIEW creditDebitTxn AS SELECT stid, sendamount, date_initiated, sendssn, sendidentifier, date_completed, (select username from user_Account where ssn=%s) as username, concat(CASE WHEN sendssn=%s THEN 'Credit' ELSE 'Debit' END) AS TxnType FROM send_transaction WHERE (sendssn=%s) OR (SendIdentifier in (SELECT phoneno FROM USER_ACCOUNT WHERE ssn=%s) OR SendIdentifier in (SELECT emailAdd from Email where userssn=%s)) and date_completed is not null"
    vals=(sessionssn,sessionssn,sessionssn,sessionssn,sessionssn,)
    c.execute(query,vals)
    connection.commit()
    query="SELECT stid,sendamount,date_initiated,sendidentifier,date_completed,txntype FROM creditDebitTxn where txntype='Credit' and sendamount=(SELECT MAX(sendamount) FROM creditDebitTxn where txntype='Credit')"
    c.execute(query)
    result=c.fetchall()
    header = ['STId','SendAmount','Date_Initiated','SendIdentifier','Date_Completed','TxnType']
    lc=0
    Label(stmtOp6,text="Best User").grid(row=0,column=0)
    Label(stmtOp6,text="Credit").grid(row=0,column=1)

    counter=4

    for eachheader in header:
        e=Label(stmtOp6,width=20,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=counter,column=lc)
        lc=lc+1
    counter = counter+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp6, width=15) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1
    query="SELECT stid,sendamount,date_initiated,sendidentifier,date_completed,txntype FROM creditDebitTxn where txntype='Debit' and sendamount=(SELECT MAX(sendamount) FROM creditDebitTxn where txntype='Debit') and date_completed is not null"
    c.execute(query)
    result=c.fetchall()
    header = ['STId','SendAmount','Date_Initiated','SendIdentifier','Date_Completed','TxnType']
    lc=0
    counter=counter+3
    Label(stmtOp6,text="Best User").grid(row=counter,column=0)
    Label(stmtOp6,text="Debit").grid(row=counter,column=1)
    counter=counter+1
    for eachheader in header:
        e=Label(stmtOp6,width=15,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=counter,column=lc)
        lc=lc+1
    counter = counter+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp6, width=15) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1

def stmt1():
    date_str = startdate.get_date()
    stdate = datetime.strftime(date_str, '%Y-%m-%d %H:%M:%S')
    date_str = enddate.get_date()
    endate = datetime.strftime(date_str, '%Y-%m-%d %H:%M:%S')
    endate = datetime.strptime(endate,'%Y-%m-%d %H:%M:%S')
    endate = endate + timedelta(hours=23,minutes=59,seconds=59)
    select_query = ("SELECT sum(SendAmount) FROM `send_transaction` WHERE SendSSN=%s and (Date_Initiated BETWEEN %s AND %s) and Date_Completed is not null")
    vals = (sessionssn, stdate, endate)
    c.execute(select_query, vals)
    result = c.fetchone()
    totalTxn = result[0]

    select_query = ("SELECT stid, sendamount, date_initiated, memo, sendidentifier, date_completed FROM send_transaction WHERE sendssn = %s "+
                    "and (Date_Initiated BETWEEN %s AND %s) and Date_Completed is not null")
    vals = (sessionssn, stdate, endate)
    c.execute(select_query, vals)
    result = c.fetchall()
    counter=7
    header = ['STId','SendAmount','Date_Initiated','Memo','SendIdentifier','Date_Completed']
    lc=0
    for eachheader in header:
        e=Label(stmtOp1,width=20,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=6,column=lc)
        lc=lc+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp1, width=20) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1
    Label(stmtOp1,text="Total amount").grid(row=counter,column=0)
    Label(stmtOp1,text=totalTxn).grid(row=counter,column=1)

def stmt2():
    date_str = startdate.get_date()
    stdate = datetime.strftime(date_str, '%Y-%m-%d %H:%M:%S')
    date_str = enddate.get_date()
    endate = datetime.strftime(date_str, '%Y-%m-%d %H:%M:%S')
    endate = datetime.strptime(endate,'%Y-%m-%d %H:%M:%S')
    endate = endate + timedelta(hours=23,minutes=59,seconds=59)
    select_query = ("SELECT SUM(SendAmount) FROM send_transaction WHERE (SendIdentifier in (SELECT phoneno FROM USER_ACCOUNT WHERE ssn=%s) OR SendIdentifier in (SELECT emailAdd from Email where userssn=%s)) and (Date_Initiated BETWEEN %s AND %s) and Date_Completed is not null")
    vals = (sessionssn,sessionssn, stdate, endate)
    c.execute(select_query, vals)
    result = c.fetchone()
    totalTxn = result[0]

    select_query = ("SELECT STId, SendAmount, Date_initiated, memo, (select username from user_account where ssn=sendssn), Date_completed  FROM send_transaction WHERE (SendIdentifier in (SELECT phoneno FROM USER_ACCOUNT WHERE ssn=%s) OR SendIdentifier in (SELECT emailAdd from Email where userssn=%s)) and (Date_Initiated BETWEEN %s AND %s) and Date_Completed is not null")
    vals = (sessionssn,sessionssn, stdate, endate)
    c.execute(select_query, vals)
    result = c.fetchall()
    counter=7
    header = ['STId','SendAmount','Date_Initiated','Memo','Sender','Date_Completed']
    lc=0
    for eachheader in header:
        e=Label(stmtOp2,width=15,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=6,column=lc)
        lc=lc+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp2, width=15) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1
    Label(stmtOp2,text="Total amount").grid(row=counter,column=0)
    Label(stmtOp2,text=totalTxn).grid(row=counter,column=1)

def monthlyStatSent():
    global stmtOp3
    stmtOp3 = Toplevel(statement_frame)
    stmtOp3.geometry('900x900')
    Label(stmtOp3,text="Monthly Statement",font=("Arial", 16)).grid(row=0,column=0)
    Label(stmtOp3,text="Debit(Sent)",font=("Arial", 16)).grid(row=0,column=1)

    select_query = ("SELECT SUM(SendAmount), AVG(SendAmount), YEAR(date_initiated), MONTH(date_initiated) FROM send_transaction WHERE sendssn=%s AND date_completed is not null GROUP BY YEAR(date_initiated), MONTH(date_initiated)")
    vals = (sessionssn,)
    c.execute(select_query, vals)
    result = c.fetchall()
    counter=2
    header = ['Total','Average','Year','Month']
    lc=0
    for eachheader in header:
        e=Label(stmtOp3,width=15,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=counter-1,column=lc)
        lc=lc+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp3, width=15) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1

def monthlyStatRcvd():
    stmtOp4 = Toplevel(statement_frame)
    stmtOp4.geometry('900x900')
    Label(stmtOp4,text="Monthly Statement",font=("Arial", 16)).grid(row=0,column=0)
    Label(stmtOp4,text="Credit(Received)",font=("Arial", 16)).grid(row=0,column=1)

    select_query = ("SELECT SUM(SendAmount), AVG(SendAmount), YEAR(date_initiated), MONTH(date_initiated) FROM send_transaction WHERE (SendIdentifier in (SELECT phoneno FROM USER_ACCOUNT WHERE ssn=%s) OR SendIdentifier in (SELECT emailAdd from Email where userssn=%s)) AND date_completed is not null GROUP BY YEAR(date_initiated), MONTH(date_initiated)")
    vals = (sessionssn,sessionssn,)
    c.execute(select_query, vals)
    result = c.fetchall()
    counter=2
    header = ['Total','Average','Year','Month']
    lc=0
    for eachheader in header:
        e=Label(stmtOp4,width=15,text=eachheader,borderwidth=2, relief='ridge',anchor='w',background='yellow')
        e.grid(row=counter-1,column=lc)
        lc=lc+1
    for rowval in result:
            for j in range(0,len(rowval)):
                e = Entry(stmtOp4, width=15) 
                e.grid(row=counter, column=j) 
                e.insert(END, rowval[j])
                e.config(state=DISABLED)
                e.config(foreground="black", background="white")
            counter = counter+1    

def total_amount_sent_by_user_in_date_range():
    global startdate
    global enddate
    global stmtOp1
    stmtOp1 = Toplevel(statement_frame)
    stmtOp1.geometry('900x900')
    Label(stmtOp1,text="Enter the Start Date :").grid(row=2,column=0)
    startdate=DateEntry(stmtOp1,selectmode='day')
    startdate.grid(row=2,column=1,padx=15)
    Label(stmtOp1,text="Enter the End Date :").grid(row=3,column=0)
    enddate=DateEntry(stmtOp1,selectmode='day')
    enddate.grid(row=3,column=1,padx=15)
    Button(stmtOp1, text = "Get Transactions",command=stmt1).grid(row=4,column=0)

def total_amount_received_by_user_in_date_range():
    global startdate
    global enddate
    global stmtOp2
    stmtOp2 = Toplevel(statement_frame)
    stmtOp2.geometry('900x900')
    Label(stmtOp2,text="Enter the Start Date :").grid(row=2,column=0)
    startdate=DateEntry(stmtOp2,selectmode='day')
    startdate.grid(row=2,column=1,padx=15)
    Label(stmtOp2,text="Enter the End Date :").grid(row=3,column=0)
    enddate=DateEntry(stmtOp2,selectmode='day')
    enddate.grid(row=3,column=1,padx=15)
    Button(stmtOp2, text = "Get Transactions",command=stmt2).grid(row=4,column=0)

def addLinkFields(uname):
    global addBAfield
    global lBaId, lBaNum
    addBAfield = Toplevel(accountInfo)
    addBAfield.geometry('400x200')
    lBaIdLabel=Label(addBAfield,width=20,text='Bank Id',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    lBaId = Entry(addBAfield, width=30) 
    lBaNumLabel=Label(addBAfield,width=15,text='Account Number',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    lBaNum = Entry(addBAfield, width=30) 
    linkBtn = tk.Button(addBAfield, name="linkBtn", text="Add", width=10, command=lambda: linkBA(uname))
    lBaIdLabel.pack()
    lBaId.pack()
    lBaNumLabel.pack()
    lBaNum.pack()
    linkBtn.pack()

def linkBA(uname):
    #check existing account details 
    bankId1 = lBaId.get()
    bankNo = lBaNum.get()
    user_query = "SELECT * FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(user_query, (uname,))
    user = c.fetchone()
    existingBId = user[4]
    existingBaNum = user[5]
    existingBAVerified = user[6]
    
    accntcheck_query = "SELECT * FROM `HAS_ADDITIONAL` WHERE `SSN` = %s AND BankId=%s AND BANumber=%s"
    c.execute(accntcheck_query, (user[0],bankId1,bankNo))
    accntcheckresult = c.fetchone()
    if(accntcheckresult.count == 0):
        tk.messagebox.showerror(title="Error!", message="This bank-account is not listed. Please go back and add new bank account before linking! ")
        addBAfield.withdraw()
        return False
    
    #link new bank account from has additional table
    updateqry = "UPDATE USER_ACCOUNT SET UserBankId=%s, UserBANumber=%s, PBAVerified=%s WHERE SSN=%s"
    c.execute(updateqry,(bankId1,bankNo,accntcheckresult[3],user[0]))
    connection.commit()

    #add the main account to has additional if its not there
    checkqry = "SELECT * FROM HAS_ADDITIONAL WHERE SSN=%s AND BankId=%s AND BANumber=%s"
    c.execute(checkqry,(user[0],existingBId,existingBaNum))
    checkqryRes = c.fetchone()

    if(checkqryRes.count==0):
        qry = "INSERT INTO HAS_ADDITIONAL VALUES (%s,%s,%s,%s)"
        c.execute(qry,(user[0],existingBId,existingBaNum,existingBAVerified))
        connection.commit()
    
    tk.messagebox.showinfo(title="Successful!", message="Bank Linked Successfully!")
    addModify.withdraw()
    return True

def addBankFields(uname):
    global addBankWIndow
    addBankWIndow = Toplevel(accountInfo)
    addBankWIndow.geometry('400x400')
    global adbankId, adbANo
    adbankIdLabel=Label(addBankWIndow,width=20,text='Bank Id',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    adbankId = Entry(addBankWIndow, width=30) 
    adBANoLabel=Label(addBankWIndow,width=15,text='Account Number',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    adbANo = Entry(addBankWIndow, width=30) 
    addbnk_button = tk.Button(addBankWIndow, name="addbnk_button", text="Add", width=10, command=lambda: addBank(uname))
    adbankIdLabel.pack()
    adbankId.pack()
    adBANoLabel.pack()
    adbANo.pack()
    addbnk_button.pack()

def addBank(uname):
    bankId1 = adbankId.get()
    bankNo = adbANo.get()
    user_query = "SELECT SSN FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(user_query, (uname,))
    user= c.fetchone()
    insertqry = "INSERT INTO BANK_ACCOUNT VALUES (%s,%s)"
    c.execute(insertqry,(bankId1,bankNo))
    connection.commit()
    insertqry2 = "INSERT INTO HAS_ADDITIONAL VALUES (%s,%s,%s,%s)"
    c.execute(insertqry2,(user[0],bankId1,bankNo,0))
    connection.commit()
    tk.messagebox.showinfo(title="Successful!", message="Bank Added Successfully!")
    addBankWIndow.withdraw()
    return True

def addEmail(usersession):
    #get email address entered
    emailId = em.get()
    #get the user's ssn
    user_query = "SELECT SSN FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(user_query, (usersession,))
    user = c.fetchone()
    #check if email already exists in email table
    emailExistqry = "SELECT * FROM EMAIL WHERE EmailAdd=%s"
    c.execute(emailExistqry, (emailId,))
    emailExist = c.fetchall()
    if(len(emailExist) != 0):
        tk.messagebox.showerror(title="Error!", message="Email already exists!")
        addfield.withdraw()
        return False
       
    #check if email already exists in email table
    #add email address to elec_addr table if it does not exist
    emailExistqry = "SELECT * FROM ELEC_ADDRESS WHERE Identifier=%s"
    c.execute(emailExistqry, (emailId,))
    emailExist = c.fetchall()
    if(len(emailExist) == 0):
        queryAddtoEA = "INSERT INTO ELEC_ADDRESS VALUES (%s, %s, %s)"
        c.execute(queryAddtoEA,(emailId,0,'EMAIL'))
        connection.commit()
    
    #add email address to email table
    queryAdd = "INSERT INTO EMAIL VALUES (%s, %s)"
    c.execute(queryAdd,(emailId,user[0]))
    connection.commit()
    tk.messagebox.showinfo(title="Successful!", message="Email Added Successfully!")
    addfield.withdraw()
    return True

def removeEmail(uname):
    emailId = rmem.get()
    checkEmailQry = "SELECT * FROM EMAIL WHERE EmailAdd=%s AND UserSSN = (SELECT SSN FROM USER_ACCOUNT WHERE UserName = %s)"
    c.execute(checkEmailQry,(emailId,uname))
    checkEmailres = c.fetchall()
    print(checkEmailres)
    if(len(checkEmailres) == 0):
         tk.messagebox.showerror(title="Error!", message="This email Id does not exist!")
         rmvfield.withdraw()
         return False

    querydel = "DELETE FROM `EMAIL` WHERE EmailAdd = %s"
    querydelfromEA = "DELETE FROM `ELEC_ADDRESS` WHERE Identifier = %s"
    c.execute(querydel,(emailId,))
    c.execute(querydelfromEA,(emailId,))
    connection.commit()
    tk.messagebox.showinfo(title="Success!", message="Email Deleted!")
    rmvfield.withdraw()
    return True
    # print(emailId)

def getAllEmail(uname):
    global addModify
    addModify = Toplevel(accountInfo)
    addModify.geometry('800x500')

    #get the email ids listed for this username from the email table
    email_query = "SELECT EmailAdd FROM `EMAIL` as e JOIN `USER_ACCOUNT` as u WHERE e.UserSSN=u.SSN and u.SSN = (SELECT u1.SSN FROM `USER_ACCOUNT` AS u1 WHERE u1.UserName = %s)"
    c.execute(email_query, (uname,))
    emailList = c.fetchall()
    i=0
    #dynamic naming and deletion not working
    for j in range(len(emailList)):
        e = Entry(addModify, width=30) 
        e.grid(row=j,column=0)
        e.insert(END, emailList[j])
        e.config(state=DISABLED)
        e.config(foreground="black", background="white")
        i=i+1

    #function : new email addition
    def addfields():
        global addfield
        global em
        addfield = Toplevel(addModify)
        addfield.geometry('400x200')
        em = Entry(addfield, width=30) 
        em.grid(row=0,column=0)
        add_btn = tk.Button(addfield, name="add_btn", text="Add", width=10, command=lambda: addEmail(uname))
        add_btn.grid(row=0,column=2)
    
    #function : email deletion
    def addDelEmFields():
        global rmvfield
        global rmem
        rmvfield = Toplevel(addModify)
        rmvfield.geometry('400x200')
        rmem = Entry(rmvfield, width=30) 
        rmem.grid(row=0,column=0)
        rmem_btn = tk.Button(rmvfield, name="rmem_btn", text="Remove", width=10, command=lambda: removeEmail(uname))
        rmem_btn.grid(row=0,column=2)

        
    #a button to add email    
    add_button = tk.Button(addModify, name="add_button", text="New Email Id", width=10, command=lambda: addfields())
    add_button.grid(row=i+5,column=0)
    #buttons for removing email
    rmv_button = tk.Button(addModify, name="del", text="Delete Email", width=15, command=lambda: addDelEmFields())
    rmv_button.grid(row=i+7,column=0)

def addFieldsModify(uname):
    global addModify
    addModify = Toplevel(accountInfo)
    addModify.geometry('800x500')
    global username, mphone
    #ssnLabel=Label(addModify,width=15,text='SSN',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    #ssn = Entry(addModify, width=30) 
    unameLabel=Label(addModify,width=15,text='UserName',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    username = Entry(addModify, width=30) 
    phnLabel=Label(addModify,width=15,text='Phone',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    mphone = Entry(addModify, width=30) 
    mdfy_button = tk.Button(addModify, name="mdfy_button", text="OK", width=10, command=lambda: modifyDetails(uname))
    #ssnLabel.pack()
    #ssn.pack()
    unameLabel.pack()
    username.pack()
    phnLabel.pack()
    mphone.pack()
    mdfy_button.pack()

def modifyDetails(uname):
    val = (username.get(),mphone.get(), uname,)

    select_query = "SELECT * FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(select_query, (uname,))
    currentuser = c.fetchone()

    #check if ssn and username does not exist already
    dupCheck = "SELECT * FROM USER_ACCOUNT WHERE UserName = %s"
    c.execute(dupCheck,(username.get(),))
    userExists = c.fetchall()
    if(len(userExists) != 0):
       tk.messagebox.showerror(title="Error in Updation!", message="UserName already exists")
       addModify.withdraw()
       return False
    
    #check if phone num exists in elec_address table
    phoneCheck = "SELECT * FROM ELEC_ADDRESS WHERE Identifier=%s"
    c.execute(phoneCheck,(mphone.get(),))
    phoneValid = c.fetchall()
    if(len(phoneValid) == 0):
       phoneAdd = "INSERT INTO ELEC_ADDRESS VALUES (%s,%s,%s)"
       c.execute(phoneAdd,(mphone.get(),0,"PHONE"))
       connection.commit()

    #if all checks passed then --->       
    query1 = "UPDATE USER_ACCOUNT SET UserName=%s, PhoneNo=%s WHERE UserName = %s"
    c.execute(query1,val)
    connection.commit()
    tk.messagebox.showinfo(title="Successful!", message="Info Updated!")
    addModify.withdraw()
    getAccountInfo(uname)
    return True

def getAccountInfo(uname):
    select_query = "SELECT * FROM `USER_ACCOUNT` WHERE `UserName` = %s"
    c.execute(select_query, (uname,))
    user = c.fetchone()
    
    #table headers        
    e=Label(accountInfo,width=15,text='SSN',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=0)
    e=Label(accountInfo,width=15,text='UserName',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=1)
    e=Label(accountInfo,width=15,text='PhoneNo',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=2)
    e=Label(accountInfo,width=15,text='Balance',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=3)
    e=Label(accountInfo,width=15,text='UserBankID',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=4)
    e=Label(accountInfo,width=15,text='UserBANumber',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=5)
    e=Label(accountInfo,width=15,text='Verified',borderwidth=2, relief='ridge',anchor='w',background='yellow')
    e.grid(row=0,column=6)

    for j in range(len(user)-1):
            e = Entry(accountInfo, width=15) 
            e.grid(row=1, column=j) 
            e.insert(END, user[j])
            e.config(state=DISABLED)
            e.config(foreground="black", background="white")

    modify_button = tk.Button(accountInfo, name="modify_button", text="Modify Account Info", width=15, font=('Verdana',8),command=lambda: addFieldsModify(uname))
    modify_button.grid(row=2,column=8,sticky=E)
    viewEmail_button = tk.Button(accountInfo, name="viewEmail_button", text="View Email Ids", width=15,font=('Verdana',8), command=lambda: getAllEmail(uname))
    viewEmail_button.grid(row=3,column=8,sticky=E)
    addBnk_button = tk.Button(accountInfo, name="addBnk_button", text="Add New Bank", width=15,font=('Verdana',8), command=lambda: addBankFields(uname))
    addBnk_button.grid(row=4,column=8,sticky=E)
    addLnk_button = tk.Button(accountInfo, name="addLnk_button", text="Link Bank Account", width=15,font=('Verdana',8), command=lambda: addLinkFields(uname))
    addLnk_button.grid(row=5,column=8,sticky=E)
    m = tk.Button(accountInfo, name="modify_button4", text="Verify Account",font=('Verdana',8), command=verify)
    m.grid(row=6,column=8,sticky=E)

def addSndMoneyFields(uname):
    global amt, memo, phone
    #email
    amtLabel=Label(sendMoney,width=15,text='Amount',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    amt = Entry(sendMoney, width=30) 
    memoLabel=Label(sendMoney,width=15,text='Memo',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    memo = Entry(sendMoney, width=30) 
    phnLabel=Label(sendMoney,width=15,text='Phone/Email',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    phone = Entry(sendMoney, width=30) 
    #emlabel=Label(sendMoney,width=15,text='Email',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    #email = Entry(sendMoney, width=30) 
    snd_button = tk.Button(sendMoney, name="snd_button", text="Send", width=10, command=lambda: sendMoneyToUser(uname))
    amtLabel.pack()
    amt.pack()
    memoLabel.pack()
    memo.pack()
    phnLabel.pack()
    phone.pack()
    #emlabel.pack()
    #email.pack()
    snd_button.pack()

def sendMoneyToUser(usersession):

    def addFieldCancel():
        global rsn
        rsnLabel=Label(cancelTrans,width=15,text='Reason to Cancel',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
        rsn = Entry(cancelTrans, width=30)
        cancel_btn= tk.Button(cancelTrans, name="cancel_btn", text="OK", width=5, command=lambda: cancelTransaction(stId))
        rsnLabel.pack()
        rsn.pack()
        cancel_btn.pack()
    
    global transId    
    amount = amt.get()
    Memo = memo.get()
    toPhone = phone.get()
    #toEmail = email.get()
    isPhone = 0
    #fetch details of the logged in user
    currentUserCheckqry = "SELECT * FROM USER_ACCOUNT WHERE UserName= %s"
    c.execute(currentUserCheckqry,(usersession,))
    currentUserCheck = c.fetchone()
    if(toPhone == ''):
        tk.messagebox.showerror(title="Error!", message="Invalid Email/Phone!")
        return False
    elif(toPhone.isdigit()):
        isPhone=1
    elif(toPhone.isdigit()==False):
        isPhone =0
    
    userCheck = 0
    eaIdentifer = ""
    if(isPhone==1):
        touserCheckQuery = "SELECT * FROM USER_ACCOUNT WHERE PhoneNo = %s"
        c.execute(touserCheckQuery,(toPhone,))
        userCheck = c.fetchall()
    elif(isPhone==0):
        touserCheckQuery = "SELECT * FROM EMAIL WHERE EmailAdd = %s AND UserSSN = %s"
        c.execute(touserCheckQuery,(toPhone,currentUserCheck[0]))
        userCheck = c.fetchall()

    if(currentUserCheck[3] < Decimal(amount)):
        tk.messagebox.showerror(title="Error in Sending!", message="Insufficient Balance!")
        return False
    if(len(userCheck) == 0):
        init_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stId = ''.join([random.choice(string.digits) for n in range(15)])
        #add unknown email/phone to elec_address table
        queryAddtoEA = "INSERT INTO ELEC_ADDRESS VALUES (%s, %s, %s)"
        if(isPhone==1):
            c.execute(queryAddtoEA,(toPhone,0,'PHONE'))
            eaIdentifer = toPhone
        else:
            c.execute(queryAddtoEA,(toPhone,0,'EMAIL'))
            eaIdentifer = toPhone
        connection.commit()
        #add transaction to send transaction table
        comp_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        querySend = "INSERT INTO SEND_TRANSACTION VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
        c.execute(querySend,(stId,amount,init_date,Memo,"",currentUserCheck[0],eaIdentifer,comp_date))
        connection.commit()
        queryBalanceUpdate = "UPDATE USER_ACCOUNT SET BALANCE=BALANCE-%s WHERE SSN = %s"
        c.execute(queryBalanceUpdate,(amount,currentUserCheck[0]))
        connection.commit()
        #tk.messagebox.showinfo(title="Sent", message="Money sent to the user. This user has 15 days to sign up to EWALLET in order to recieve the money. If not, the money will be credited back to your account!")
        #button to cancel transaction
        global cancelTrans
        cancelTrans = Toplevel(sendMoney)
        cancelTrans.geometry('850x200')
        #show trans successful message here and do u wanna cancel? 
        show_txt = tk.Label(cancelTrans,text="Money sent to the user. This user has 15 days to sign up to EWALLET in order to recieve the money. If not, the money will be credited back to your account!")
        cncl_text = tk.Label(cancelTrans,text="You can cancel this transaction within the next 10 minutes. Do you want to cancel?")
        cncl_button = tk.Button(cancelTrans, name="cncl_button", text="Cancel", width=10, command=lambda: addFieldCancel())
        show_txt.pack()
        cncl_text.pack()
        cncl_button.pack()
        
    else:
        init_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if(isPhone==1):
            eaIdentifer = toPhone
        else:
            eaIdentifer = toPhone
        stId = ''.join([random.choice(string.digits) for n in range(15)])
        #add transaction to send transaction table
        querySend = "INSERT INTO SEND_TRANSACTION VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
        comp_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute(querySend,(stId,amount,init_date,Memo,"",currentUserCheck[0],eaIdentifer,comp_date))
        connection.commit()
        print("Amount Sent!")
        queryBalanceUpdate = "UPDATE USER_ACCOUNT SET BALANCE=BALANCE-%s WHERE SSN = %s"
        c.execute(queryBalanceUpdate,(amount,currentUserCheck[0]))
        connection.commit()
        queryBalanceUpdate2 = ""
        if(isPhone == 1):
            queryBalanceUpdate2 = "UPDATE USER_ACCOUNT SET BALANCE=BALANCE+%s WHERE PhoneNo = %s"
            c.execute(queryBalanceUpdate2,(amount,eaIdentifer))
        else:
            queryBalanceUpdate2 = "UPDATE USER_ACCOUNT SET BALANCE=BALANCE+%s WHERE SSN = (SELECT UserSSN from EMAIL WHERE EmailAdd=%s)"
            c.execute(queryBalanceUpdate2,(amount,eaIdentifer))
        connection.commit()
        tk.messagebox.showinfo(title="Sent", message="Transaction Completed!")
        #button to cancel transaction
        #sendMoney.withdraw()
        #global cancelTrans
        cancelTrans = Toplevel(sendMoney)
        cancelTrans.geometry('850x200')
        #show trans successful message here and do u wanna cancel? 
        show_txt = tk.Label(cancelTrans,text="Transaction Successful!")
        cncl_text = tk.Label(cancelTrans,text="You can cancel this transaction within the next 10 minutes. Do you want to cancel?")
        cncl_button = tk.Button(cancelTrans, name="cncl_button", text="Cancel", width=10, command=lambda: addFieldCancel())
        show_txt.pack()
        cncl_text.pack()
        cncl_button.pack()
        #return True

def addReqMoneyFields(uname):
    global reqamt, reqmemo, person
    reqamtLabel=Label(reqMoney,width=20,text='Requested Amount',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    reqamt = Entry(reqMoney, width=30) 
    reqmemoLabel=Label(reqMoney,width=15,text='Memo',borderwidth=2, relief='ridge',anchor='w',background='light blue')
    reqmemo = Entry(reqMoney, width=30) 
    personLabel=Label(reqMoney,width=30,text='Person Email/Phone',borderwidth=2, relief='ridge',anchor='nw',background='light blue')
    person = Entry(reqMoney, width=30)
    req_button = tk.Button(reqMoney, name="req_button", text="Request", width=10, command=lambda: requestMoney(uname))
    reqamtLabel.pack()
    reqamt.pack()
    reqmemoLabel.pack()
    reqmemo.pack()
    personLabel.pack()
    person.pack()
    req_button.pack()

def requestMoney(usersession):
    #collect data to be sent
    amount = reqamt.get()
    Memo = reqmemo.get()
    personId = person.get()

    currentUserCheckqry = "SELECT * FROM USER_ACCOUNT WHERE UserName= %s"
    c.execute(currentUserCheckqry,(usersession,))
    currentUserCheck = c.fetchone()
    reqssn = currentUserCheck[0]

    if(personId.isdigit()):
        userPhoneCheck = "SELECT * FROM USER_ACCOUNT WHERE PhoneNo= %s"
        c.execute(userPhoneCheck,(personId,))
        userPhoneRes= c.fetchone()
        if(len(userPhoneRes)== 0):
            tk.messagebox.showerror(title="Error!", message="Phone Number not found!")
            reqMoney.withdraw()
            return False
        else:
            phoneValidCheck = "SELECT * FROM ELEC_ADDRESS WHERE Identifier=%s AND Verified=%s AND EType=%s"
            c.execute(phoneValidCheck,(personId,1,'PHONE'))
            phoneRes = c.fetchone()
            if(len(phoneRes)==0):
                tk.messagebox.showerror(title="Error!", message="Phone Number should be verified!")
                reqMoney.withdraw()
                return False
            else:
                reqId = ''.join([random.choice(string.digits) for n in range(15)])
                req_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                reqQuery = "INSERT INTO REQUEST_TRANSACTION VALUES (%s, %s, %s, %s, %s)"
                c.execute(reqQuery,(reqId,amount,req_date,Memo,reqssn))
                connection.commit()
                reqFromQuery = "INSERT INTO `FROM` VALUES (%s, %s, %s)"
                c.execute(reqFromQuery,(reqId,personId,100.00))
                connection.commit()
                tk.messagebox.showinfo(title="Successful!", message="Request Sent Successfully!") 
                reqMoney.withdraw()
                return True             
    else:
        userEmailCheck = "SELECT * FROM EMAIL WHERE EmailAdd= %s"
        c.execute(userEmailCheck,(personId,))
        userEmailCheck= c.fetchone()
        if(len(userEmailCheck)== 0):
            tk.messagebox.showerror(title="Error!", message="Email not found!")
            reqMoney.withdraw()
            return False
        else:
            emailValidCheck = "SELECT * FROM ELEC_ADDRESS WHERE Identifier=%s AND Verified=%s AND EType=%s"
            c.execute(emailValidCheck,(personId,1,'EMAIL'))
            emailRes = c.fetchone()
            if(len(emailRes)==0):
                tk.messagebox.showerror(title="Error!", message="Email should be verified!")
                reqMoney.withdraw()
                return False
            else:
                reqId = ''.join([random.choice(string.digits) for n in range(15)])
                req_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                reqQuery = "INSERT INTO REQUEST_TRANSACTION VALUES (%s, %s, %s, %s, %s)"
                c.execute(reqQuery,(reqId,amount,req_date,Memo,reqssn))
                connection.commit()
                reqFromQuery = "INSERT INTO `FROM` VALUES (%s, %s, %s)"
                c.execute(reqFromQuery,(reqId,personId,100.00))
                connection.commit()
                tk.messagebox.showinfo(title="Successful!", message="Request Sent Successfully!")  
                reqMoney.withdraw()
                return True

def cancelTransaction(transId):
    reason = rsn.get()
    #if all checks passed then --->   
    checkTransQry = "SELECT * FROM SEND_TRANSACTION WHERE STid = %s"
    c.execute(checkTransQry,(transId,))
    trans = c.fetchone()
    date_init = datetime.strptime(str(trans[2]),'%Y-%m-%d %H:%M:%S')
    trans_date = date_init + timedelta(minutes=10)
    if(trans_date >= datetime.now()):
        query1 = "UPDATE SEND_TRANSACTION SET Cancel_Reason=%s,Date_Completed=%s WHERE STid = %s"
        c.execute(query1,(reason, None, transId))
        connection.commit()
        #UPDATE BALANCE
        query2 = "UPDATE USER_ACCOUNT SET Balance=Balance + %s WHERE SSN = %s"
        c.execute(query2, (Decimal(trans[1]),trans[5]))
        connection.commit()
        tk.messagebox.showerror(title="Success!", message="Transaction Cancelled!")
        cancelTrans.withdraw()
        return TRUE
    else:
        tk.messagebox.showerror(title="Cancellation not possible!", message="10 minutes have passed!")
        cancelTrans.withdraw()
        return False

def mainMenu(event):
    if value_inside.get() == "Account Info":
        global accountInfo
        accountInfo = Toplevel(root1)
        accountInfo.geometry('600x500')
        getAccountInfo(usersession)        
    elif value_inside.get() == "Send Money":
        global sendMoney
        sendMoney = Toplevel(root1)
        sendMoney.geometry('600x500')
        addSndMoneyFields(usersession)        
    elif value_inside.get() == "Request Money":
        global reqMoney
        reqMoney = Toplevel(root1)
        reqMoney.geometry('600x500')
        addReqMoneyFields(usersession)
    elif value_inside.get() == "Statements":
        global statement_frame
        statement_frame = Toplevel(root1)
        statement_frame.geometry('600x600')
        statementMenu()
    elif value_inside.get() == "Sign Out":
        root1.destroy()
     
# create a function to make the user login
def login():
    uname= username_entry.get().strip()
    pwd = password_entry.get().strip()
    authentication=loginAuth(uname,pwd)
    print("Set the usersession as : ")
    print(usersession)
    if authentication:
        global value_inside
        global root1
        root1=Toplevel(root)
        root1.geometry('400x500')
        options_list = ["Main Menu","Account Info", "Send Money", "Request Money", "Statements","Sign Out"]
        value_inside = StringVar(root1)
        value_inside.set("Select an Option")
        question_menu = OptionMenu(root1, value_inside, *options_list,command=mainMenu)
        print(question_menu)
        print(value_inside.get())
        question_menu.pack()
    else:
        global authFailed
        authFailed=Toplevel(root)
        authFailed.geometry('400x500')
        Label(authFailed,text='The login information is wrong! Please try again!').pack()
        relogin_button = tk.Button(authFailed,text="OK",command=lambda:go_to_login()).pack()
        #relogin_button['command'] = go_to_login
        #relogin_button.bind("<Button-1>", lambda page: go_to_login())

login_button['command'] = login

# ----------- Register Page ------------- #
registerframe = tk.Frame(mainframe, width=w, height=h)
register_contentframe = tk.Frame(registerframe, padx=15, pady=15, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

ssn_label_rg = tk.Label(register_contentframe, text='SSN:', font=('Verdana',14), bg=bgcolor)
username_label_rg = tk.Label(register_contentframe, text='Username:', font=('Verdana',14), bg=bgcolor)
password_label_rg = tk.Label(register_contentframe, text='Password:', font=('Verdana',14), bg=bgcolor)
confirmpass_label_rg = tk.Label(register_contentframe, text='Re-Password:', font=('Verdana',14), bg=bgcolor)
phone_label_rg = tk.Label(register_contentframe, text='Phone:', font=('Verdana',14), bg=bgcolor)
userbankid_label_rg = tk.Label(register_contentframe, text='Bank ID:', font=('Verdana',14), bg=bgcolor)
userbanumber_label_rg = tk.Label(register_contentframe, text='Account Number', font=('Verdana',14), bg=bgcolor)
email_label_rg = tk.Label(register_contentframe, text='Mail ID', font=('Verdana',14), bg=bgcolor)


ssn_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
username_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
password_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')
confirmpass_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')
phone_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
userbankid_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
userbanumber_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)
email_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)

register_button = tk.Button(register_contentframe,text="Register", font=('Verdana',16), bg='#2980b9',fg='#fff', padx=25, pady=10, width=25)
go_login_label = tk.Label(register_contentframe, text=">> already have an account? sign in" , font=('Verdana',10), bg=bgcolor, fg='red')

register_contentframe.pack(fill='both', expand=1)

ssn_label_rg.grid(row=0, column=0, pady=5, sticky='e')
ssn_entry_rg.grid(row=0, column=1)

username_label_rg.grid(row=1, column=0, pady=5, sticky='e')
username_entry_rg.grid(row=1, column=1)

password_label_rg.grid(row=2, column=0, pady=5, sticky='e')
password_entry_rg.grid(row=2, column=1)

confirmpass_label_rg.grid(row=3, column=0, pady=5, sticky='e')
confirmpass_entry_rg.grid(row=3, column=1)

phone_label_rg.grid(row=4, column=0, pady=5, sticky='e')
phone_entry_rg.grid(row=4, column=1)

userbankid_label_rg.grid(row=5, column=0, pady=5, sticky='e')
userbankid_entry_rg.grid(row=5, column=1)

userbanumber_label_rg.grid(row=6, column=0, pady=5, sticky='e')
userbanumber_entry_rg.grid(row=6, column=1)

email_label_rg.grid(row=7, column=0, pady=5, sticky='e')
email_entry_rg.grid(row=7, column=1)

register_button.grid(row=8, column=0, columnspan=2, pady=20)

go_login_label.grid(row=9, column=0, columnspan=2, pady=10)

# create a function to display the login frame
def go_to_login():
    authFailed.withdraw()
    registerframe.forget()
    loginframe.pack(fill="both", expand=1)
    title_label['text'] = 'Login'
    title_label['bg'] = '#2980b9'


go_login_label.bind("<Button-1>", lambda page: go_to_login())
# --------------------------------------- #
# create a function to check if the username already exists
def check_username(username):
    username = username_entry_rg.get().strip()
    vals = (username,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        return True
    else:
        return False
# --------------------------------------- #
# create a function to register a new user
# create a function to register a new user
def register():
    ssn = ssn_entry_rg.get().strip() # remove white space
    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()
    phone = phone_entry_rg.get().strip()
    userbankid = userbankid_entry_rg.get().strip()
    userbanumber = userbanumber_entry_rg.get().strip()
    email = email_entry_rg.get().strip()
   
    if len(ssn) > 0 and  len(username) > 0 and len(password) > 0 and len(phone) > 0:
        if check_username(username) == False: 
            if password == confirm_password:
                vals = (ssn, username, password, phone, userbankid, userbanumber)
                insert_query = "INSERT INTO `USER_ACCOUNT`(`ssn`, `username`, `password`, `phoneno`, `userbankid`, `userbanumber`) VALUES (%s,%s,%s,%s,%s,%s)"
                c.execute(insert_query, vals)
                vals = (email,ssn)
                insert_query = "INSERT INTO `EMAIL`(`emailadd`, `userssn`) VALUES (%s,%s)"
                c.execute(insert_query, vals)
                connection.commit()
                messagebox.showinfo('Register','your account has been created successfully')
            else:
                messagebox.showwarning('Password','incorrect password confirmation')
        else:
            messagebox.showwarning('Duplicate Username','This Username Already Exists, try another one')
    else:
        messagebox.showwarning('Empty Fields','make sure to enter all the information')

register_button['command'] = register
# --------------------------------------- #
# ------------------------------------------------------------------------ #
root.mainloop()
