import csv
import nltk

def words_per_issue(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        all_words = nltk.word_tokenize(text)
        return len(all_words)

directory = "/issues/"

infile ="/college-news/data/cn-metadata.csv"

new_rows = [['id', 'filename', 'date', 'vol', 'no', 'pages', 'words'],]

with open(infile) as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    for row in reader:
        if count > 0:
            ident = row[0]
            date = row[1]
            long_id = row[2].split('-')
            volume = long_id[2][3:]
            no = long_id[3][2:]
            pages = row[3]
            filename = 'cn' + date + '.txt'
            words = words_per_issue(directory + filename)
            new_row = [ident, filename, date, volume, no, pages, words]
            new_rows.append(new_row)
        else:
            count +=1

#print(new_rows[1:5])

outfile = 'extended-metadata.csv'
with open(outfile, 'w', encoding='utf-8') as csvwrite:
    writer = csv.writer(csvwrite)
    writer.writerows(new_rows)
