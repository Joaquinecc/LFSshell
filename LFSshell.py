import shutil
def shell_copy(parameters):
    #Funcion que simula el comando copiar
    #Obtenemos los parametros
    try:
        paths=parameters.split(" ") #separamos los parametros
        src=paths[0] 
        dest=paths[1]
    except IndexError: 
        print("Missing parameter")
        return
    except:
        print("Error ocured")
    #Hacemos la copia
    try:
        new_path=shutil.copy(src,dest)
        print("copy {0} --> {1}".format(src,new_path))
    except FileNotFoundError:
        #File does not exist
        print("File Source does not exist")
    except:
        print("Invalid parameter)


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