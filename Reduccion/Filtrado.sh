#!/bin/bash

#Funcionamiento:
#./Filtrado.sh {path} {mode_operation} {date}
#./Filtrado.sh "/media/soporte/RAWDATA/HYOa/" 1 2022/08/30

#Reduccion de datos

python3 Filtrado.py -f 2.72216796875   -path $1 -code 0 -C $2 -date $3 -R 1
python3 Filtrado.py -f 2.7221646392718 -path $1 -code 0 -C $2 -date $3 -R 1
python3 Filtrado.py -f 2.7221712982282 -path $1 -code 0 -C $2 -date $3 -R 1

python3 Filtrado.py -f 3.64990234375   -path $1 -code 0 -C $2 -date $3 -R 1
python3 Filtrado.py -f 3.6499056732282 -path $1 -code 0 -C $2 -date $3 -R 1
python3 Filtrado.py -f 3.6498990142718 -path $1 -code 0 -C $2 -date $3 -R 1

# Almacenar datos de salida en diferente ruta:
#python3 Filtrado.py -f 3.6498990142718 -code 2 -C $1 -date $2 -R 1 -path_o "/media/soporte/PROCDATA/Same_Struct/"
