#!/usr/bin/python3

import shutil
import os
import getpass
import socket
import datetime
from subprocess import Popen, PIPE
#--------------------------------------------------------------------------
#External Function
def write_data_user(data,username):
    f = open("/var/log/personaldata/{0}_data.log".format(username), "a") #Abre o crea si es necesario
    f.write(data)
    f.close()
def invalid_parameter():
        print("invalid parameter")
def check_user(username,state):
    #Primero obtenemos us datos personales
    try:
        f = open("/var/log/personaldata/{0}_data.log".format(username), "r") #Accedemos a lo
        hours=f.readline().strip().split('-') #con strip removemos todo los  caracteres blanco 
        valid_ip=f.readline().strip().split('-')
        f.close()
    except OSError as error:
        print(error)
        return
    
    current_ip = socket.gethostbyname(socket.gethostname()) #obtenemos el ip address del usuario
    now = datetime.datetime.now().strftime("%H:%M") #Obtenemos el tiempo del usuario
    #REGISTRAMOS EN LOG
    try:
        f = open("/var/log/shell/usuario_horarios_log", "a")
        f.write("{0} {1} {2} {3}\n".format(now,state,username,current_ip)) #Escribimo el ingreso o salida del usuario
        #Checkear si el usuario ingreso fuera de su horario
        #Formateamos el horario
        horario_de_entrada=hours[0] if len(hours[0]) == 5 else '0'+ hours[0]
        horario_de_salida=hours[1] if len(hours[1]) == 5 else '0'+ hours[1]
        now=now if len(now)== 5 else '0'+now
        if(horario_de_entrada>now or horario_de_salida<now): #si esta fuera de rango el  ingreso o salida del usuario
            f.write("Fuera del horario regular en ubicacion:{0} \n".format(current_ip))
        f.close()
    except OSError as error:
        print(error)
        return
def get_paths(paths):
        #Obtenemos los path de los parametros
    try:
        paths=paths.split(" ") #separamos los parametros
        src=paths[0] 
        dest=paths[1]
        return [src,dest]
    except IndexError: 
        print("Missing parameter")
        return False
    except:
        print("Invalid parameter")
        return False
def write_transfer_log(command):
    #Funcion para escribir la transferencia ocurrida
    try:
        date=datetime.datetime.now().strftime("(%Y-%m-%d %H:%M:%S)") #obtenemos el dia con su hora
        f = open("/var/log/Shell_transferencias.log", "a") # abrimos el archivo
        f.write("{0} - {1}\n".format(date,command)) #Cargamos los datos
        f.close() #Cerramos
    except OSError as error:
        print(error)
    except:
        print("Error al escribir en el transfer log")
def write_commands_log(command):
    try:
        #Funcion para escribir en log todos los comando ejecutados
        date=datetime.datetime.now().strftime("(%Y-%m-%d %H:%M:%S)") #obtenemos el dia con su hora
        f = open("/var/log/shell/shell.log", "a") # abrimos el archivo
        f.write("{0} - {1} - {2}\n".format(date,getpass.getuser(),command)) #Cargamos los datos
        f.close() #Cerramos
    except OSError as error:
        print(error)
    except:
        print("Error al escribir en el command log")

def write_error_log(error):
    try:
        #Funcion para escribir en log todos los errores ocurrido
        date=datetime.datetime.now().strftime("(%Y-%m-%d %H:%M:%S)") #obtenemos el dia con su hora
        f = open("/var/log/shell/sistema_error.log", "a") # abrimos el archivo
        f.write("{0} - {1} - {2}\n".format(date,getpass.getuser(),error)) #Cargamos los datos
        f.close() #Cerramos
    except OSError as error:
        print(error)
    except:
        print("Error al escribir en el command log")
#----------------------------------------------------------------------------
#Comands Function
def shell_transfer(command):
    #Ejecutar transferencia
    log=command
    command=command.replace('transfer','scp',1)
    try:
        os.system(command) #Ejecutamos
        write_transfer_log(log) #Escribmos en el log la accion ocurrida
        write_commands_log(log)
    except OSError as error:
        print(error)
        write_error_log(error)

def shell_demon(state,service):
    #Funcion para apagar y prender servicios
    if state == 'up':
        try:
            p=Popen(["systemctl", service, "start"], stdin=PIPE, stdout=PIPE, stderr=PIPE) #Corre el servicio
            write_commands_log("demon"+state+" "+service)            
        except OSError as error:
            print(error)
            write_error_log(error)
    elif state == 'dw':
        try:
            p=Popen(["systemctl", service, "stop"], stdin=PIPE, stdout=PIPE, stderr=PIPE) #para el servicio
            write_commands_log("demon"+state+" "+service)            
        except OSError as error:
            print(error) 
            write_error_log(error)
    else:
        print("invalid command: try demonup or demondw")


def shell_newpasswd(command):
    params=command
    command=command.replace("contraseña","passwd",1)
    command=command.replace("contrasena","passwd",1)
    # command='sudo '+command
    try:
        os.system(command)
        write_commands_log(params)
    except OSError as error:
        print(error)
        write_error_log(error)
def shell_newuser(command):
    #Comando para crear usuarios
    #args=adduser <USERNAME> <HORARIO DE ENTRADA-HORARIO DE SALIDA> <IP1>-<IP2>...
    #EJEMPLO:adduser lfsuser 09:00-16:00 192.168.0.3-193.4.5.1.4
    args=command
    args=args.split(" ")
    try:
        username=args[1]
        timerange=args[2]
        locations=args[3]
        data="{0}\n{1}".format(timerange,locations)
        try:
            os.system("useradd {}".format(username))
            print("user {0} created".format(username))
            write_data_user(data,username)
            write_commands_log(command)
        except OSError as error:
            print(error)
            write_error_log(error)
    except:
        try:
            # command='sudo '+command
            os.system(command.replace('usuario','useradd',1))
        except OSError as error:
            print(error)
            write_error_log(error)

def shell_chewn(args):
    #Funcion para cambiar el propertario de un archivo o funcion
    command=args
    args=args.replace("propietario","chown",1)
    try:
        os.system(args) #Cambiamos de propetiario
        write_commands_log(command)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        invalid_parameter()

def shell_chmod(args):
    #Funcion para cambiar los permisos sobre un archivo o un conjunto de archivos
    params=args
    # args=get_paths(args)
    # if args == False :
    #     return False
    # mode=args[0]
    # path=args[1]
    # command='chmod {0} {1}'.format(mode,path)
    command = args.replace('permiso','chmod',1)
    print
    try:
        os.system(command) #Nos mudadmos de directorio
        write_commands_log("permiso "+params)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        invalid_parameter()

def shell_cd(path):
    #Funcion para mudar de directorio
    try:
        os.chdir(path) #Nos mudadmos de directorio
        write_commands_log('ir '+path)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        invalid_parameter()

def shell_creatdir(path):
    #Funcion  para crear carpetas
    try:
        os.mkdir(path) #Creamos el directorio
        print("Directorio {} creado".format(path))
        write_commands_log('creadir '+path)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        invalid_parameter()

def shell_list(path):
    #Funcion que simula el comando ls
    try:
        dirs=os.listdir(path) #Obtenemos todos los  directorio del path
        for dir in dirs: #Como retorna un array hacemos un llop y impirmimos
            print(dir)
        write_commands_log('listar '+path)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        invalid_parameter()
def shell_rename(args):
    #Funcion que especificamene modifica el nombre de un directorio


    #Obtenemos los paths
    paths=get_paths(args)
    if paths == False :
        return False
    src=paths[0] 
    new_name=paths[1]
    #Verificamos si el new name no es una direccion
    if(new_name.find("/") != -1):
        print("Second parameter must be a name not an address")
        print("If you want to move a file and rename it, use command : copy ")
        return


    #Creamos el nuevo path
    new_path=""
    index=src.rfind("/")
    if index == -1:
        new_path=new_name
    else:
        new_path=src.replace(src[index+1:],new_name)

    try:
        os.rename(src,new_path)
        print("renombrar {0} --> {1}".format(src,new_path))
        write_commands_log("renombrar "+args)
    # except FileNotFoundError:
    #     print('No such file: {0}'.format(src))
    except IsADirectoryError:
        error="new name = {0} is a directory".format(new_name)
        print(error)
        write_error_log(error)
    except NotADirectoryError:
        error="src = {0} is a directory".format(src)
        print(error)
        write_error_log(error)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        print("Invalid parameter")

def shell_move(args):
    #Funcion que simula el movimiento de archivos a directorios
    #Obtenemos los paths
    paths=get_paths(args)
    if paths == False :
        return False
    src=paths[0] 
    dest=paths[1]
    #Executamos el movimientode archivo
    try:
        new_path=shutil.move(src,dest)
        print("Move {0} --> {1}".format(src,new_path))
        write_commands_log('mover '+ args)
    except FileNotFoundError:
        #File does not exist
        error="File Source {0} does not exist".format(src)
        print(error)
        write_error_log(error)
    except:
        print("Invalid parameter")

def shell_copy(args):
    #Funcion que simula el comando copiar
    #obtenemos los paths
    paths=get_paths(args)
    if paths == False :
        return False
    src=paths[0] 
    dest=paths[1]
    #Hacemos la copia
    try:
        new_path=shutil.copy(src,dest)
        print("copiar {0} --> {1}".format(src,new_path))
        write_commands_log("copiar "+args)
    # except FileNotFoundError:
    #     #File does not exist
    #     error="File Source {0} does not exist".format(src)
    #     print(error)
    #     write_error_log(error)
    except OSError as error:
        print(error)
        write_error_log(error)
    except:
        print("Invalid parameter")


def main():
    print("Shell start")
    username=getpass.getuser()
    check_user(username,"login")
    while True:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        command = input("{} $".format(dir_path))
        if command == "exit":
            break
        elif command[:6] == "copiar":
            shell_copy(command[7:])
        elif command[:5] == "mover":
            shell_move(command[6:])
        elif command[:9] == "renombrar":
            shell_rename(command[10:])
        elif command[:6] == "listar":
            shell_list(command[7:] if len(command)>6 else '.')
        elif command[:7] == "creadir":
            shell_creatdir(command[8:])
        elif command[:2] == "ir":
            shell_cd(command[3:])
        elif command[:7] == "permiso":
            shell_chmod (command)
        elif command[:11] == "propietario":
            shell_chewn(command)
        elif command[:7] == "usuario":
            shell_newuser(command)
        elif command[:10] == "contrasena" or command[:10] == "contraseña":
            shell_newpasswd(command)
        elif command[:6] == "logout":
            check_user(username,"logout")
            write_commands_log("logout")
            break
        elif command[:5] == "demon":
            shell_demon(command[5:7],command[7:])
        elif command[:8]== "transfer":
            shell_transfer(command)
        else:
            os.system(command)

if '__main__' == __name__:
    main()

# shutil.move("test/test1","test2")
#move test/test1
# transfer lp1-2018@127.0.0.1:/home/lp1-2018/Escritorio/LFSSehll/LFSshell/test2 test/namels
#transfer test2/name hola3@127.0.0.1:/home/lp1-2018/Escritorio/LFSSehll/LFSshell/test/a
