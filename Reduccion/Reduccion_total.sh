#!/bin/bash
#./Reduccion_total.sh ["Date"] ["path_in"] ["path_out"] [Rx location. JROa:11]
#./Filtrado.sh ["path_in"] [0] [f0:2.72  f1:3.64] ["Date"]  ["path_out"] [Rx location. JROa:11]
echo "Iniciando Filtrado y Reduccion de datos HF ..."
date=$1
path_in=$2
path_out=$3
rx_lo=$4
echo "....Iniciando F0"
screen -S "Reduccion_F0" -d -m ./Filtrado.sh $path_in 0 f0 $date $path_out $rx_lo

for i in {1..4}
do
   echo -n "."
   sleep 1s
done

echo "Iniciando F1"
screen -S "Reduccion_F1" -d -m ./Filtrado.sh $path_in 0 f1 $date $path_out $rx_lo
sleep 1
COUNT=$(screen -list | grep -c "Reduccion_F1")
while [  $COUNT != "0" ]
do
sleep 3
echo "Waiting for Reduct to finish"
COUNT=$(screen -list | grep -c "Reduccion_F1")
done
