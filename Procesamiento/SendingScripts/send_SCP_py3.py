import os,glob,datetime
import argparse
import pexpect #pip install --user  pexpect
import time
# En caso no se pueda enviar hacer escribir etas lineas >

#ssh -X -C wmaster@jro-app.igp.gob.pe -p 6633

#Resultado >
#The authenticity of host '[jro-app.igp.gob.pe]:6633 ([181.177.244.71]:6633)' can't be established.
#RSA key fingerprint is 24:ea:fe:d5:4e:91:8d:82:d5:7d:1f:bf:e2:0c:36:70.
#Are you sure you want to continue connecting (yes/no)? yes

debug = True

def sendBySCP(Incommand, location): #"%04d/%02d/%02d 00:00:00"%(tnow.year,tnow.month,tnow.day)
        username = "wmaster"
        password = "mst2010vhf"#"123456"
        #port = "-p6633"
        host = "jro-app.igp.gob.pe"#"25.59.69.206"
        #hostdirectory = "/home/wmaster/web2/web_signalchain/data/%s/%s/%s/figures"%(place,rxname,day)
        #command = "sshfs %s %s@%s:%s %s -o nonempty "%(port,username,host,hostdirectory,mountpoint)
        command = Incommand
        if debug:
                print(command)

        console = pexpect.spawn('/bin/bash', ['-c',command])
        try:
            os.system(command)  #La magia
            #Para reconocerlos se debe usar la siguiente linea >
            console = pexpect.spawn('/bin/bash', ['-c',command])

            if not (location == 11 or location == 12):
                console.expect(username + "@" + host + "'s password:")
                time.sleep(2)
                        #usual response > wmaster@jro-app.igp.gob.pe's password:
                console.sendline(password)
            time.sleep(3)
            console.expect(pexpect.EOF)
            return True
        except Exception:
                if debug:
                        print( str("Error"))
                return False
###################################INGRESANDO CODIGO 0 o 2##############################################################
parser = argparse.ArgumentParser()
parser.add_argument('-code',action='store',dest='code_seleccionado',help='Code para generar Spectro off-line 0,1,2')
parser.add_argument('-lo',action='store',dest='localstation',default =11 ,help='Codigo de estacion 11 JRO A, 12 JRO B, 21 HYO A, 22 HYO B, etc..')
parser.add_argument('-path',action='store',dest='path',default= "/home/igp-114/Pictures/", help='Directorio principal donde estan los resultados a enviar')
parser.add_argument('-type',action='store',dest='type',default ="params" ,help='Determines the type of data to be sent')


results= parser.parse_args()
code= int(results.code_seleccionado)
rxcode= int(results.localstation)
PATH = str(results.path)
datatype = str(results.type)

###########################################################################################################################
tdstr = datetime.date.today()
str1 = tdstr + datetime.timedelta(days=-1)
yesterday = str1.strftime("%Y%j")

dlist = []
file_lines = []
station_type = "A" if rxcode % 10 == 1 else "B"
with open("Doys_not_sent_%s_%s"%(datatype,station_type),"r") as f:
        # The Doys_not_sent file have data about the doys that hasn't been sent, each line represents a doys
        # And each line has the same doy or None for each code, None represents that the data hasn't
        # been sent yet for that code.
        for line in f.readlines():
                file_lines.append(line[:-1].split(","))

                doy_or_none = file_lines[-1][code]
                if doy_or_none != "None":
                        dlist.append(doy_or_none)

if yesterday not in [doy for line in file_lines for doy in line]:
        dlist.append(yesterday)
        file_lines.append([yesterday]*3)


location_dict = {11:"JRO_A", 12: "JRO_B", 21:"HYO_A", 22:"HYO_B", 31:"MALA",
        41:"MERCED", 51:"BARRANCA", 61:"OROYA"}
if rxcode in [11, 12, 21, 22]:
        station_orientation = "A" if rxcode % 10 == 1 else "B"
else:
        station_orientation = "A"

if rxcode in [11, 12, 21, 22]:
        lo = rxcode
else:
        lo = int(rxcode/10)*10+1

print("PATH",PATH)
if datatype == "params":
        graph_freq0=PATH+"GRAPHICS_SCHAIN_%s/"%location_dict[lo]+'sp'+str(code)+'1_f0'
        graph_freq1=PATH+"GRAPHICS_SCHAIN_%s/"%location_dict[lo]+'sp'+str(code)+'1_f1'
else:
        graph_freq0 = PATH+"RTDI_%s/graphics_schain/"%station_orientation + 'sp'+str(code)+'1_f0'
        graph_freq1 = PATH+"RTDI_%s/graphics_schain/"%station_orientation + 'sp'+str(code)+'1_f1'


str_datatype = "*/" if datatype == "params" else ""

web_type = "web_signalchain" if datatype == "params" else "web_rtdi"
letter = "H" if datatype == "out" else "" # This adds the H.
extension = "out" if datatype == "out" else "jpeg"
out_or_figures = "out" if datatype == "out" else "figures"

for file in dlist[:]: # Se usa una copia porque dlist puede ser modificado dentro del bucle
        data_written_0 = True #Flag that represents data_written
        data_written_1 = True
        doy = 'd'+file
        jpg_files_0 = glob.glob("%s/%s/%s*.%s"%(graph_freq0, doy,str_datatype,extension))
        jpg_files_0.sort()
        jpg_files_1 = glob.glob("%s/%s/%s*.%s"%(graph_freq1, doy,str_datatype,extension))
        jpg_files_1.sort()
        print("JPG-FREQ 0",jpg_files_0)
        print("JPG-FREQ 1",jpg_files_1)
        print("%s/%s/%s*.%s"%(graph_freq0, doy,str_datatype,extension))
        print("%s/%s/%s*.%s"%(graph_freq1, doy,str_datatype,extension))
        if len(jpg_files_0) is 0 and len(jpg_files_1) is 0:
                print('No hay RESULTADOS en la carpeta!!!')
                continue
        #file_1=os.path.basename(jpg_files[0])[offset:]
        if datatype == "params":
                if jpg_files_0 == []:
                    file_1 = jpg_files_1[0][:-1].split("/")[-3]
                elif jpg_files_1 == []:
                    file_1 = jpg_files_0[0][:-1].split("/")[-3]
                else:
                    file_1 = jpg_files_1[0][:-1].split("/")[-3]
        else:
                if jpg_files_0 == []:
                    file_1 = jpg_files_1[0][:-1].split("/")[-2]
                elif jpg_files_1 == []:
                    file_1 = jpg_files_0[0][:-1].split("/")[-2]
                else:
                    file_1 = jpg_files_1[0][:-1].split("/")[-2]
                #file_1 = jpg_files_1[0][:-1].split("/")[-2]
        file_1 = file_1[1:]

        YEAR=int (file_1[0:4])
        DAYOFYEAR= int(file_1[4:7])
        DAYOFYEAR_str = file_1[4:7]
        d = datetime.date(YEAR, 1, 1) + datetime.timedelta(DAYOFYEAR - 1)
        print("(1) Determinando dia a enviar.")
        print('d.strftime("%Y/%m/%d")>', d.strftime("%Y/%m/%d"))

        MONTH = d.strftime("%m")
        DAY = d.strftime("%d")
        AorB = rxcode%2 # Si es par(B) AorB sera 0, si es impar(A) AorB sera 1.

        if rxcode == 11 or rxcode == 12 :
                rxname = 'JRO'
        if rxcode == 21 or rxcode == 22 :
                rxname = 'HUANCAYO'
        if rxcode == 31 or rxcode == 32 :
                rxname = 'MALA'
        if rxcode == 41 or rxcode == 42 :
                rxname = 'MERCED'
        if rxcode == 51 or rxcode == 52 :
                rxname = 'BARRANCA'
        if rxcode == 61 or rxcode == 62 :
                rxname = 'OROYA'


        if code ==0 and AorB == 1:
                station_name="HFTXANCON"
        if code ==0 and AorB == 0:
                station_name="HFBTXANCON"
        if code ==1 and AorB == 1:
                station_name="HFTXSICAYA"
        if code ==1 and AorB == 0:
                station_name="HFBTXSICAYA"
        if code ==2 and AorB == 1:
                station_name="HFTXICA"
        if code ==2 and AorB == 0:
                station_name="HFBTXICA"

        #remote_folder="/home/wmaster/web2/web_rtdi/data/JRO/%s/%s/%s/%s/figures/"%(station_name, YEAR, MONTH,DAY)
        remote_folder="/home/wmaster/web2/%s/data/%s/%s/%s/%s/%s/%s/"%(web_type,rxname,station_name, YEAR, MONTH,DAY, out_or_figures)
        print("(2) Direccion de llegada de datos.")
        print("Remote_folder: %s"%(remote_folder))
        #Primer Comando, generar carpeta de destino.

        command_1="ssh wmaster@jro-app.igp.gob.pe -p 6633 mkdir -p %s"%(remote_folder)
        if sendBySCP(command_1, rxcode):
                print('Carpeta Creada')


        #os.system("ssh wmaster@jro-app.igp.gob.pe -p 6633 %s "%(command_1))

        #Segundo comando, pasar las imagenes necesarias para la freq 0
        if jpg_files_0 != []:
            print("(3) Enviando resultados frecuencia 0")
            temp_command = "scp -r -P 6633 %s/%s/%s%s%s%s%s*.%s wmaster@jro-app.igp.gob.pe:%s"%(graph_freq0,doy,str_datatype,
            letter,YEAR, DAYOFYEAR_str, rxcode, extension, remote_folder)

            if sendBySCP(temp_command, rxcode):
                print(' -- Datos Enviados F0')
            else:
                data_written_0=False
        else:
            data_written_0=False

        #Segundo comando, pasar las imagenes necesarias para la freq 1                                  AQUI
        #temp_command = "scp -r -P 6633 %s/%s/*.jpeg wmaster@jro-app.igp.gob.pe:%s"%(graph_freq1,doy,remote_folder)
        if jpg_files_1 != []:
            print("(4) Enviando resultados frencuencia 1") #DAYOFYEAR_str
            temp_command = "scp -r -P 6633 %s/%s/%s%s%s%s%s*.%s wmaster@jro-app.igp.gob.pe:%s"%(graph_freq1,doy,str_datatype,
            letter,YEAR, DAYOFYEAR_str, rxcode, extension, remote_folder)

            if sendBySCP(temp_command, rxcode):
                print(' -- Datos enviados F1 ')
            else:
                data_written_1 = False
        else:
            data_written_1=False

        ##Checks if all data where sent, if not save the doy in the file what contains all doy not sent yet.
        if data_written_0 and data_written_1:
                #dlist.remove(file)
                index = [file_lines[i][code] for i in range(len(file_lines))].index(file)
                file_lines[index][code] = "None"
                if file_lines[index].count("None") == 3:
                        file_lines.pop(index)

print("\n\n\n")
os.remove("Doys_not_sent_%s_%s"%(datatype,station_type))
with open("Doys_not_sent_%s_%s"%(datatype,station_type), "w") as f:
        for line in file_lines:
                f.write(line[0]+','+line[1]+','+line[2]+"\n") #File contains date in 2019200 format yeardoy
