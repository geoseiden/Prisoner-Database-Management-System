import mysql.connector as my
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import tix 
from ttkthemes import ThemedStyle #pip install required

def coh(button, colorOnHover, colorOnLeave):

        button.bind("<Enter>", func=lambda e: button.config(
                bg=colorOnHover))

        button.bind("<Leave>", func=lambda e: button.config(
                bg=colorOnLeave))

def login():
        def submitact():
                global u
                u = Username.get()
                global p
                p = password.get()
        
                print()
                
                root.destroy()
                
                menu(u, p)
                

        
        root = tix.Tk()
        root.configure(bg='#696969')
        root.geometry('310x90')
        root.title("PDMS Login Page")
        
        
        lblfrstrow = tk.Label(root, text ="Username -",font=('Helvetica'),bg='#696969',fg='black')
        lblfrstrow.grid(row=0,column=0)
        Username = tk.Entry(root, width = 35)
        Username.grid(row=0,column=1)
        
        lblsecrow = tk.Label(root, text ="Password -",font=('Helvetica'),bg='#696969',fg='black')
        lblsecrow.grid(row=1,column=0)
        
        password = tk.Entry(root, width = 35,show="*")
        password.grid(row=1,column=1)
        
        
        submitbtn = tk.Button(root, text ="Login",bg ='seagreen', command =lambda:[submitact()],borderwidth=0,font=('Helvetica'))
        submitbtn.grid(row=2,column=1,sticky='nsew')
        coh(submitbtn,'green','seagreen')
        tip=tix.Balloon(root)
        tip.bind_widget(submitbtn,balloonmsg="Program will quit if password is wrong")

        root.mainloop()

def menu(u,p):
    """This function provides options to choose from"""
    global mydb
    mydb=my.connect(host='localhost',
                    user=u,
                    passwd=p,
                    database='school')
    global cur
    cur=mydb.cursor()
    cur.execute('select *  from prison;')
    r=cur.fetchall()
    global root1
    root1 = tk.Tk()
    root1.title("Prisoner Database Management System - PDMS")
    root1.configure(bg='black')
    root1.rowconfigure([0],weight=1)
    root1.columnconfigure([0,1,2,3,4],weight=1)
    root1.configure(background='#696969')
    #title = tk.Label(master=root1,text='PRISON MANAGEMENT SYSTEM',font=('Baskerville Old Face',15),bg='#5D5D5D',fg='white',)
    #title.grid(row=0,column=0,columnspan=5,sticky='nsew')
    
    root2=tk.Frame(root1,height=300)
    root2.grid(row=0,column=0,columnspan=5,sticky='nsew')
    st=ThemedStyle(root1)
    st.set_theme('equilux')
    tv=ttk.Treeview(root2,columns=(1,2,3,4),show='headings',height=5)
    tv.pack(side=LEFT)
    tv.heading(1,text='Pr.No')
    tv.column(1,width=100)
    tv.heading(2,text='Name')
    tv.column(2,width=210)
    tv.heading(3,text='City')
    tv.column(3,width=160)
    tv.heading(4,text='Gender')
    tv.column(4,width=145)
    for i in r:
        tv.insert('','end',values=i,tags='M')
    tv.tag_configure('M',font='Helvetica 10')
    scrollbar=Scrollbar(root2,orient='vertical',command=tv.yview)
    scrollbar.pack(side=RIGHT,fill='y')
    
    frm=Frame(root1)
    frm.grid(row=1,column=0,columnspan=5)
    add_b = tk.Button(master=frm,text='New Prisoner',command=lambda:[root1.destroy(),add()],height=2,width=15,font=('Helvetica',12),borderwidth=0,bg='#696969',fg='black')
    add_b.grid(row=0,column=0,sticky='nsew')
    coh(add_b,'#8c8c8c','#696969')
    update_b = tk.Button(master=frm,text='Update Prisoner Data',command=lambda:[root1.destroy(),update()],height=2,width=20,font=('Helvetica',12),borderwidth=0,bg='#696969',fg='black')
    update_b.grid(row=0,column=1,sticky='nsew')
    coh(update_b,'#8c8c8c','#696969')
    delete_b = tk.Button(master=frm,text='Delete Prisoner Data',command=lambda:[root1.destroy(),delete()],height=2,width=20,font=('Helvetica',12),borderwidth=0,bg='#696969',fg='black')
    delete_b.grid(row=0,column=2,sticky='nsew')
    coh(delete_b,'#8c8c8c','#696969')
    exit_b = tk.Button(master=frm,text='Exit',command=lambda:[bye(),root1.destroy()],height=2,width=10,font=('Helvetica',12),borderwidth=0,bg='tomato',fg='black')
    exit_b.grid(row=0,column=3,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    
    mmenu=Menu(root1)
    root1.configure(menu=mmenu)
    crmenu=Menu(mmenu,tearoff=0)
    mmenu.add_cascade(label='More',menu=crmenu)
    crmenu.add_command(label='Mysql Command Line',command=lambda:[os.system('mysqlsh -u {} -p{}'.format(u,p))])
    crmenu.add_command(label='Mysql export',command=lambda:[os.system('mysql -u {} -p{} school>school.sql'.format(u,p))])
    
    root1.mainloop()
                                                
def bye():
        """This function exits the program after closing all connections"""
        cur.close()
        mydb.close()
               
def  check_exists(prno):
    """This function returns True if the student exists in the table prisoner
    otherwise returns False"""
    cur=mydb.cursor()
    sql="select * from prison where prno='%s'"%(prno,)
    cur.execute(sql)
    mydata=cur.fetchall()
    if cur.rowcount==0:
        return False
    else:
        return True
        
   
     
        
                 
def add():
    """This function creates a tkinter environment to add a record of a prisoner"""
    def submit_add():
        """This function adds a record of a prisoner"""
        prno_entry = prno.get()
        name_entry = name.get()
        city_entry = city.get()
        gender_entry = gender.get()
        if check_exists(prno_entry)==False:
            cur.execute("insert into prison values({},'{}','{}','{}')".format(prno_entry,name_entry,city_entry,gender_entry))
            mydb.commit()
            prno.delete(0,tk.END)
            name.delete(0,tk.END)
            city.delete(0,tk.END)
            gender.delete(0,tk.END)
            status['text'] = 'Success'
        else:
            root.destroy()
            add()
    root = tk.Tk()
    root.title('PDMS - New Prisoner')
    root.geometry('800x200+50+185')
    root.configure(bg='#5D5D5D')
    root.rowconfigure([0,1,2,3,4,5],weight=1)
    root.columnconfigure([0,1],weight=1)
    root.resizable(False,False)
    prno_label = tk.Label(master=root,text='Prisoner no:',font=('Arial',10),borderwidth=0,bg='#696969',fg='white')
    prno_label.grid(row=0,column=0,sticky='nsew')
    prno = tk.Entry(master=root)
    prno.grid(row=0,column=1)
    name_label = tk.Label(master=root,text='Name:',borderwidth=0,bg='#696969',fg='white')
    name_label.grid(row=1,column=0,sticky='nsew')
    name = tk.Entry(master=root)
    name.grid(row=1,column=1)
    city_label = tk.Label(master=root,text='City:',borderwidth=0,bg='#696969',fg='white')
    city_label.grid(row=2,column=0,sticky='nsew')
    city = tk.Entry(master=root)
    city.grid(row=2,column=1)
    gender_label = tk.Label(master=root,text='Gender:',borderwidth=0,bg='#696969',fg='white')
    gender_label.grid(row=3,column=0,sticky='nsew')
    gender = tk.Entry(master=root)
    gender.grid(row=3,column=1)
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),menu(u,p)],width=10,font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=4,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    submit_button = tk.Button(master=root,text='Submit',bg='seagreen',fg='white',borderwidth=0,command=lambda:[submit_add()])
    submit_button.grid(row=4,column=1,sticky='nsew')
    coh(submit_button,'green','seagreen')
    status = tk.Label(master=root,text='Status',fg='#9c9c9c')
    status.grid(row=5,column=0,columnspan=2,sticky='nsew')
    root.mainloop()                           
                                
              

def delete():
    """This function creates a tkinter environment to delete a record of a prisoner"""
    def submit_delete():
        """This function deletes a record of a prisoner"""
        prno_entry = prno.get()
        cur.execute("delete from prison where prno={}".format(prno_entry))
        mydb.commit()
        prno.delete(0,tk.END)
        text = str(cur.rowcount)+" record(s) deleted"
        status['text'] = text
    root = tk.Tk()
    root.title('PDMS - Delete Prisoner')
    root.geometry('800x100+50+185')
    root.configure(bg='#5D5D5D')
    root.rowconfigure([0,1,2],weight=1)
    root.columnconfigure([0,1],weight=1)
    root.resizable(False,False)
    prno_label = tk.Label(master=root,text='Prisoner no:',font=('Arial',10),borderwidth=0,bg='#696969',fg='white')
    prno_label.grid(row=0,column=0,sticky='nsew')
    prno = tk.Entry(master=root)
    prno.grid(row=0,column=1)
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),menu(u,p)],font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=1,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    submit_button = tk.Button(master=root,text='Submit',bg='seagreen',fg='white',borderwidth=0,command=lambda:[submit_delete()])
    submit_button.grid(row=1,column=1,columnspan=1,sticky='nsew')
    coh(submit_button,'green','seagreen')
    status = tk.Label(master=root,text='Status',fg='black',bg='white')
    status.grid(row=2,column=0,columnspan=2,sticky='nsew')
    root.mainloop()
                 
def update():
    """This functions gives the user options which the user can update"""
    root = tk.Tk()
    root.title('PDMS - Update Data')
    root.geometry('199x150+50+185')
    root.rowconfigure([0,1,2],weight=1)
    root.columnconfigure([0],weight=1)
    root.resizable(False,False)
    updatename_button = tk.Button(master=root,text='Update Name',command=lambda:[root.destroy(),updatename()],borderwidth=0,bg='#696969',fg='white')
    updatename_button.grid(row=0,column=0,sticky='nsew')
    coh(updatename_button,'#8c8c8c','#696969')
    updatecity_button = tk.Button(master=root,text='Update City',command=lambda:[root.destroy(),updatecity()],borderwidth=0,bg='#696969',fg='white')
    updatecity_button.grid(row=1,column=0,sticky='nsew')
    coh(updatecity_button,'#8c8c8c','#696969')
    updategender_button = tk.Button(master=root,text='Update Gender',command=lambda:[root.destroy(),updategender()],borderwidth=0,bg='#696969',fg='white')
    updategender_button.grid(row=2,column=0,sticky='nsew')
    coh( updategender_button,'#8c8c8c','#696969')
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),menu(u,p)],width=10,font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=3,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')    
    root.mainloop()

def updatename():
    """This function creates a tkinter environment to enter details for updating the name"""
    def submit_upname():
        """This functions updates the name in the database"""
        prno_entry = prno.get()
        upname_entry = upname.get()
        cur.execute("update prison set name='{}' where prno={}".format(upname_entry,prno_entry))
        mydb.commit()
        prno.delete(0,tk.END)
        upname.delete(0,tk.END)
        text = str(cur.rowcount)+" record updated successfully"
        status['text'] = text
    root = tk.Tk()
    root.title('PDMS - Update Data - Update Name')
    root.geometry('599x150+251+185')
    root.configure(bg='#696969')
    root.rowconfigure([0,1,2,3],weight=1)
    root.columnconfigure([0,1],weight=1)
    root.resizable(False,False)
    prno_label = tk.Label(master=root,text='Prisoner no:',borderwidth=0,bg='#696969',fg='white')
    prno_label.grid(row=0,column=0,sticky='nsew')
    prno = tk.Entry(master=root,borderwidth=0,bg='white',fg='black')
    prno.grid(row=0,column=1)
    upname_label = tk.Label(master=root,text='Updated name:',borderwidth=0,bg='#696969',fg='white')
    upname_label.grid(row=1,column=0,sticky='nsew')
    upname = tk.Entry(master=root,borderwidth=0,bg='white',fg='black')
    upname.grid(row=1,column=1)
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),update()],width=10,font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=2,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    submit_button = tk.Button(master=root,text='Update',bg='seagreen',fg='white',borderwidth=0,command=lambda:[submit_upname()])
    submit_button.grid(row=2,column=1,sticky='nsew')
    coh(submit_button,'green','seagreen')
    status = tk.Label(master=root,text='Status',fg='#9c9c9c')
    status.grid(row=3,column=0,columnspan=2,sticky='nsew')
    root.mainloop()
               
def updatecity():
    """This function creates a tkinter environment to enter details for updating the city"""
    def submit_upcity():
        """This functions updates the city in the database"""
        prno_entry = prno.get()
        upcity_entry = upcity.get()
        cur.execute("update prison set city='{}' where prno={}".format(upcity_entry,prno_entry))
        mydb.commit()
        prno.delete(0,tk.END)
        upcity.delete(0,tk.END)
        text = str(cur.rowcount)+" record updated successfully"
        status['text'] = text
    root = tk.Tk()
    root.title('PDMS - Update Data - Update City')
    root.geometry('599x150+251+185')
    root.configure(bg='#696969')
    root.rowconfigure([0,1,2,3],weight=1)
    root.columnconfigure([0,1],weight=1)
    root.resizable(False,False)
    prno_label = tk.Label(master=root,text='Prisoner no:',borderwidth=0,bg='#696969',fg='white')
    prno_label.grid(row=0,column=0,sticky='nsew')
    prno = tk.Entry(master=root)
    prno.grid(row=0,column=1)
    upcity_label = tk.Label(master=root,text='Updated city:',borderwidth=0,bg='#696969',fg='white')
    upcity_label.grid(row=1,column=0,sticky='nsew')
    upcity = tk.Entry(master=root)
    upcity.grid(row=1,column=1)
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),update()],width=10,font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=2,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    submit_button = tk.Button(master=root,text='Update',bg='seagreen',fg='white',borderwidth=0,command=lambda:[submit_upcity()])
    submit_button.grid(row=2,column=1,sticky='nsew')
    coh(submit_button,'green','seagreen')
    status = tk.Label(master=root,text='Status')
    status.grid(row=3,column=0,columnspan=2,sticky='nsew')
    root.mainloop()
                
                
                        
def updategender():
    """This function creates a tkinter environment to enter details for updating the gender"""
    def submit_upgender():
        """This functions updates the gender in the database"""
        prno_entry = prno.get()
        upgender_entry = upgender.get()
        cur.execute("update prison set gender='{}' where prno={}".format(upgender_entry,prno_entry))
        mydb.commit()
        prno.delete(0,tk.END)
        upgender.delete(0,tk.END)
        text = str(cur.rowcount)+" record updated successfully"
        status['text'] = text
    root = tk.Tk()
    root.title('PDMS - Update Data - Update Gender')
    root.geometry('599x150+251+185')
    root.configure(bg='#696969')
    root.rowconfigure([0,1,2,3],weight=1)
    root.columnconfigure([0,1],weight=1)
    root.resizable(False,False)
    prno_label = tk.Label(master=root,text='Prisoner no:',borderwidth=0,bg='#696969',fg='white')
    prno_label.grid(row=0,column=0,sticky='nsew')
    prno = tk.Entry(master=root)
    prno.grid(row=0,column=1)
    upgender_label = tk.Label(master=root,text='Updated gender:',borderwidth=0,bg='#696969',fg='white')
    upgender_label.grid(row=1,column=0,sticky='nsew')
    upgender = tk.Entry(master=root)
    upgender.grid(row=1,column=1)
    exit_b = tk.Button(master=root,text='Back',command=lambda:[root.destroy(),update()],width=10,font=('Arial',10),borderwidth=0,bg='tomato',fg='white')
    exit_b.grid(row=2,column=0,sticky='nsew')
    coh(exit_b,'#f03c1d','tomato')
    submit_button = tk.Button(master=root,text='Update',bg='seagreen',fg='white',borderwidth=0,command=lambda:[submit_upgender()])
    submit_button.grid(row=2,column=1,sticky='nsew')
    coh(submit_button,'green','seagreen')
    status = tk.Label(master=root,text='Status',fg='#9c9c9c')
    status.grid(row=3,column=0,columnspan=2,sticky='nsew')
    root.mainloop()
               
login()
