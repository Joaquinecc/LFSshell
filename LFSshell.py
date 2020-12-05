import shutil
import os
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
def shell_rename(args):
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
        command = input("shell-$ ")
        if command == "exit":
            break
        elif command[:4] == "copy":
            shell_copy(command[5:])
        elif command[:4] == "move":
            shell_move(command[5:])
        elif command[:6] == "rename":
            shell_rename(command[7:])
        else:
            print("Command not found")


if '__main__' == __name__:
    main()

# shutil.move("test/test1","test2")
#move test/test1
