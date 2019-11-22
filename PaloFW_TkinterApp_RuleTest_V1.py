from datetime import datetime
import paramiko,sys,re
import getpass
import time

from tkinter import *
import tkinter.messagebox



window= Tk()
window.title("Palo FW Test Tool")
window.geometry("1150x500")

username_var = StringVar()
fw_var = StringVar()
password_var = StringVar()
fw_var = StringVar()
vsys_var = StringVar()
vsys_name = StringVar()
SourceIP_var = StringVar()
DestinationIP_var = StringVar()
Port_var = StringVar()


def main():
    user_name = username_var.get()
    #print(user_name)
    user_password = password_var.get()
    host_name = fw_var.get()
    #print(hostname)
    fwname = fw_var.get()
    #vsysname = vsys_dict[vsys_var.get()]
    # sourceip=SourceIP_var.get()
    # destinationip = DestinationIP_var.get()
    # port=Port_var.get()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect (host_name, port = 22 , username =user_name , password = user_password)
    return ssh
    # transport = ssh.get_transport()

    # return transport


def login_fw(transport,host_name=fw_var.get()):

    transport = transport.get_transport()
    session = transport.open_session()
    session.get_pty()
    session.invoke_shell() 
    #session.keep_this = ssh

    print(f" Connected to FW {host_name} ")
    pager_cli ='set cli pager off \n'
    pager_cli = pager_cli.encode()
    session.send(pager_cli)
    time.sleep(2)
    pager_output = session.recv(9999)
    print(pager_output.decode())

    vsys_command ="set system setting target-vsys vsys\t\t"
    vsys_command = vsys_command.encode()
    session.send(vsys_command)
    time.sleep(5)
    vsys_command_output = session.recv(65535)
    time.sleep(1)
    #print(vsys_command_output.decode())

    print("Creating VSYS List")

    x = vsys_command_output.decode().split("\n")



    vsys_names = [] 
    for i in x[1:-1]:
        v = re.findall(r'vsys.*',i)
        if len(v)>0:
            #print(v[0])
            vsys_names.append(v[0])
    

    vsys_droplist = OptionMenu(window,vsys_var,*vsys_names)
    vsys_var.set("select vsys name..")
    vsys_droplist.config(width=15)
    vsys_droplist.place(x=940,y=293)



def find_rule(transport,SourceIP_var,DestinationIP_var,vsys_name,Port_var):

    client = transport
    vsysname = vsys_name.get()
    sourceip=SourceIP_var.get()
    destinationip = DestinationIP_var.get()
    port=Port_var.get()
    print(f"printing details for vsysname = {vsysname}  sourceip = {sourceip} destinationip = {destinationip} port = {port}")

    
    command1 =f"set system setting target-vsys {vsysname} \n"
    command2= f'test security-policy-match source {sourceip} destination {destinationip} destination-port {port} protocol 6 \n'

    commands = command1+command2
    print(commands)

    stdin,stdout,stderr = client.exec_command(' ')
    stdin.channel.send(commands)
    stdin.channel.shutdown_write()

    resp = stdout.read().decode('utf_8')
    print (f"printing output for command ****************************************{commands}***")
    time.sleep(1)
    print(resp)

    x1=resp
    


    window1=Tk()
    scrollbar=Scrollbar(window).pack(side=RIGHT,fill=Y)
    window1.title("Welcome to Second Windows")
    window1.geometry('900x500')

    text = Text(window1)
    text.insert(INSERT, x1)
    #text.insert(END, "Bye Bye.....")
    text.pack(fill=BOTH)




label1 = Label(window,text="Palo FW Rule Testing Tool", fg="black",bg="grey",relief="raised",font=("arial",20,"bold"))
label1.pack()

L1_username = Label(window, text="User Name",relief="raised",width=10,font=("arial",10,"bold"))
L1_username.place( x=20, y=100)

E1_username = Entry(window, textvar=username_var,bd =2,width=30)
E1_username.place( x=150, y=100)


L2_password = Label(window, text="Password",relief="raised",width=10,font=("arial",10,"bold"))
L2_password.place(x=20, y=150)

E2_password = Entry(window, bd =2,textvar=password_var,show="*",width=30)
E2_password.place( x=150, y=150)

## Creating label for Firewall name with Two option, One is entry and second in option box. Currently option box is enable. 

L3_FirewallName = Label(window, text="HostName/IP",relief="raised",width=10,font=("arial",10,"bold"))
L3_FirewallName.place(x=20, y=200)

.fw_lists = ['fw1a','fw2a','fw3a']

fw_droplist = OptionMenu(window,fw_var,*fw_lists)
fw_var.set("select fw name..")
fw_droplist.config(width=20)
fw_droplist.place(x=150,y=200)

SourceIP = Label(window, text="SourceIP",relief="raised",width=10,font=("arial",10,"bold"))
SourceIP.place(x=20, y=300)

E4_SourceIP = Entry(window, textvar=SourceIP_var,bd =2,width=15)
E4_SourceIP.place( x=150, y=300)

DestinationIP = Label(window, text="DestinationIP",relief="raised",width=12,font=("arial",10,"bold"))
DestinationIP.place(x=290, y=300)

E5_DestinationIP = Entry(window,textvar=DestinationIP_var, bd =2,width=15)
E5_DestinationIP.place( x=430, y=300)

Ports = Label(window, text="TCP_Port",relief="raised",width=10,font=("arial",10,"bold"))
Ports.place(x=580, y=300)

E6_Ports = Entry(window,textvar=Port_var,bd =2,width=10)
E6_Ports.place(x=700, y=300)

Vsys_Name = Label(window, text="Vsys-Name",relief="raised",width=12,font=("arial",10,"bold"))
Vsys_Name.place(x=800, y=300)


E7_vsys = Entry(window,textvar=vsys_name,bd =2,width=15)
E7_vsys.place(x=800, y=350)

B1_Login = Button(window, text="LOGIN",relief="raised",command=lambda:login_fw(main(),host_name=fw_var.get()),width=10,font=("arial",10,"bold"))
B1_Login.place(x=400, y=195)



B1_FIND_RULE = Button(window, text="FIND_RULE",relief="raised",command=lambda:find_rule(main(),SourceIP_var,DestinationIP_var,vsys_name,Port_var),width=10,font=("arial",10,"bold"))
B1_FIND_RULE.place(x=20, y=400)

B2_Exit = Button(window, text="EXIT",relief="raised",command=window.destroy,width=10,font=("arial",10,"bold"))
B2_Exit.place(x=150, y=400)



window.mainloop()
















