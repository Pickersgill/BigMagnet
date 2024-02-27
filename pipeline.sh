python3 searcher.py -s $1 -l rust -i mit -o ./results/temp.json
python3 archive_getter.py -s ./results/temp.json -o ./archives -b 20
