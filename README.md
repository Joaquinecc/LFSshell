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
En la linea del usuario la ultima seccion se indica el shell, modificarlo por el  "directorio"/LFSshell.py<br/>

## Comandos
**copiar**       Simula a 'cp'.<br/>
**mover**       simula a 'mv'. <br/>
**renombrar**       Renombra un archivo. El segundo parametro es unicamente el nuevo nombre<br/>
**listar**       Simula a 'ls'. <br/>
**creardir**       Simula a 'mkdir'.<br/>
**ir**       Simula a 'cd'. <br/>
**permisos**       Simula a 'chmod'. <br/>
**propietario**       Simula a 'chown'. <br/>
**contrasena**       Simula a 'passwd'. <br/>
**usuario**       Simula a 'useradd' con informacion del timempo de ingreso y salida, y tambine sus ubicaciones. <br/>
EJEMPLO:usuario lfsuser 09:00-16:00 192.168.0.3-193.4.5.1.4.<br/>
En forma general usuario USERNAME HORARIO DE ENTRADA-HORARIO DE SALIDA IP1-IP2-.. <br/>
**exit**       Equivalente a 'exit'. <br/>
**demonup**    Levanta un demonio<br/>
**demondw**      Apaga un demonio<br/>
**transfer**       Simula scp<br/>

### Errore comun
Si se obiene este error /usr/bin/python3^M : bad interpreter <br/>
Ejecutar
> sed -i 's/\r//' LFSshell.py




