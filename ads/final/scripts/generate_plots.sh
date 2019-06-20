folder=../data/

for file in $(ls $folder | grep "_experiment")
do
    python3 plots.py $folder$file
done