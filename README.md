# LFSshell
Escrito en python3.
## Dependencias
-Python3<br/>
-Openssh<br/>
-systemd<br/>
## Paso previos para el correcto funcionamiento
Se deben crear los siguiente  directorios<br/>
mkdir /var/log<br/>
mkdir /var/log/shell<br/> 
mkdir /var/log/personaldata<br/>
chmod 777 /var/log<br/>

Shell -> Directorio donde se almacena los log de los comandos(shell.log) ,errores(sistema_error.log) y usuario_horarios_log<br/>
log --> Archivos como Shell_transferencias.log<br/>
personaldata -> username_data.log<br/>

## Instalacion

git clone https://github.com/Joaquinecc/LFSshell.git <br/>
cd LFSshell
./LFSShell

Para que sea el shell por defecto de un usuario se debe configurar el archivo /etc/passwd <br/>
En la linea del usuario la ultima seccion se indica el shell, modificarlo por el  <directorio>/LFSshell.py