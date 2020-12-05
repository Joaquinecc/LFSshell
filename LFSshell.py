import shutil
import os
import getpass
#--------------------------------------------------------------------------
#External Function
def write_data_user(data,username):
    f = open("/var/log/personaldata/data_{0}.log".format(username), "a")
    f.write(data)
    f.close()
def invalid_parameter():
        print("invalid parameter")

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
#----------------------------------------------------------------------------
#Comands Function
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
            os.system("sudo useradd {}".format(username))
            print("user {0} created".format(username))
            write_data_user(data,username)
        except OSError as error:
            print(error)
    except:
        try:
            command='sudo '+command
            os.system(command.replace('newuser','useradd',1))
        except OSError as error:
            print(error)

def shell_chewn(args):
    #Funcion para cambiar el propertario de un archivo o funcion
    args=args.replace("chewn","chown",1)
    try:
        os.system(args) #Cambiamos de propetiario
    except OSError as error:
        print(error)
    except:
        invalid_parameter()

def shell_chmod(args):
    #Funcion para cambiar los permisos sobre un archivo o un conjunto de archivos
    args=get_paths(args)
    if args == False :
        return False
    mode=args[0]
    path=args[1]
    command='chmod {0} {1}'.format(mode,path)
    try:
        os.system(command) #Nos mudadmos de directorio
    except OSError as error:
        print(error)
    except:
        invalid_parameter()

def shell_cd(path):
    #Funcion para mudar de directorio
    try:
        os.chdir(path) #Nos mudadmos de directorio
    except OSError as error:
        print(error)
    except:
        invalid_parameter()

def shell_creatdir(path):
    #Funcion  para crear carpetas
    try:
        os.mkdir(path) #Creamos el directorio
        print("Directorio {} creado".format(path))
    except OSError as error:
        print(error)
    except:
        invalid_parameter()

def shell_list(path):
    #Funcion que simula el comando ls
    try:
        dirs=os.listdir(path) #Obtenemos todos los  directorio del path
        for dir in dirs: #Como retorna un array hacemos un llop y impirmimos
            print(dir)
    except OSError as error:
        print(error)
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
        print("Rename {0} --> {1}".format(src,new_path))
    # except FileNotFoundError:
    #     print('No such file: {0}'.format(src))
    except IsADirectoryError:
        print ("new name = {0} is a directory".format(new_name))
    except NotADirectoryError:
        print ("src = {0} is a directory".format(src))
    except OSError as error:
        print(error)
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
    except FileNotFoundError:
        #File does not exist
        print("File Source {0} does not exist".format(src))
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
        print("copy {0} --> {1}".format(src,new_path))
    except FileNotFoundError:
        #File does not exist
        print("File Source {0} does not exist".format(src))
    except:
        print("Invalid parameter")


def main():
    print("Shell start")

    while True:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        command = input("{} $".format(dir_path))
        if command == "exit":
            break
        elif command[:4] == "copy":
            shell_copy(command[5:])
        elif command[:4] == "move":
            shell_move(command[5:])
        elif command[:6] == "rename":
            shell_rename(command[7:])
        elif command[:4] == "list":
            shell_list(command[5:])
        elif command[:9] == "createdir":
            shell_creatdir(command[10:])
        elif command[:2] == "cd":
            shell_cd(command[3:])
        elif command[:5] == "chmod":
            shell_chmod (command[6:])
        elif command[:5] == "chewn":
            shell_chewn(command)
        elif command[:7] == "newuser":
            shell_newuser(command)
        else:
            print("Command not found")


if '__main__' == __name__:
    main()

# shutil.move("test/test1","test2")
#move test/test1
