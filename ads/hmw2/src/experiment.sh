function generate {
    echo " $1 $(python3 pattern_generator.py $1)"
}

parameters="vpa_ref_Vicugna_pacos-2.0.1_chrUn.fa"

for i in `seq 1 20`
do
    parameters+=$(generate $i)
done

echo "bruteforce"
./bruteforce $parameters >> output.txt
echo "horspool"
./horspool $parameters >> output.txt
echo "bndm"
./bndm $parameters >> output.txt
echo "bom"
./bom $parameters >> output.txt
