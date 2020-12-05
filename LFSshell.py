import shutil
def get_paths(paths):
        #Obtenemos los path de los parametros
    try:
        paths=paths.split(" ") #separamos los parametros
        src=paths[0] 
        dest=paths[1]
        return [dest,src]
    except IndexError: 
        print("Missing the dest parameter")
        return False
    except:
        print("Invalid parameter")
        return False

def shell_copy(parameters):
    #Funcion que simula el comando copiar
    #Hacemos la copia
    paths=get_paths(parameters)
    if paths == False :
        return False
    src=paths[0] 
    dest=paths[1]
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
        else:
            print("Command not found")


if '__main__' == __name__:
    main()

shutil.copy("test/test1","")