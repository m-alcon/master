for i in {1..10000}
do
	./experiment | grep -q "Distance difference: 0"
	if [ "$?" -eq "1" ];then
		echo "Fail."
	fi
done

