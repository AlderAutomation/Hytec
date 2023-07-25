file="$1"

# Timing 
echo $(cat ./Success/$file | grep APP_TIMERS)
echo -e "\n"

# Amount of devices 
amount1=$(cat ./Success/$file | grep -o DEV_LOOKUP | wc -l)
amount2=$(cat ./Success/$file | grep DEV_SERIAL_COUNT)
echo "Amount of devices this run based on lookups:"
echo $amount1
echo "Amount of devices this run based on initial serial list lookup in logger:"
echo $amount2
echo -e "\n"

# unassigned Counter
unassigned=$(cat ./Success/$file | grep -o DEV_UNASSIGNED | wc -l)
echo "Amount of Unnassigned devices this run:"
echo $unassigned 
echo -e "\n"

# errors 
echo "There were X number of errors:"
echo $(cat ./Success/$file | grep LOG_ERROR | wc -l)
echo -e "\n"
echo "the following errors occurred:"
echo $(cat ./Success/$file | grep LOG_ERROR)
echo -e "\n"
