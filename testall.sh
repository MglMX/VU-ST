for i in `seq -w 12`
do
    ./hangman -d < tests/tc$i.in
done
