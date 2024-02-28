rm -rf archives/*
python3 searcher.py -s 10 -l rust -i mit -o ./results/temp.json -m 100000
python3 archive_getter.py -s ./results/temp.json -o ./archives -b 10
python3 unpacker.py -s archives -q ".*\.rs$" -r

files=$(find archives/ -type f | wc -l)
lines=$(find archives/ -type f -exec cat {} + | wc -l)
data=$(du -hs archives/ | awk '{print $1}')
echo "Found $files files containing $lines lines of Rust code."
echo "Amounting to $data of data."
