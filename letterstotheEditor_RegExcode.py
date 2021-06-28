from os import listdir
import re
import csv

filenames = listdir("C:/Users/thisi/Desktop/Python/all-cn-issues/issues")
    # file path to where all college news issues are

row_list = []
    # creating list for the loop to append to make csv file

for filename in filenames:
    
    newstext = "C:/Users/thisi/Desktop/Python/all-cn-issues/issues/" + filename

    f = open(newstext, encoding="utf-8")

    text = f.read()
        # turning text into string variables

    letters = re.findall(r"letter.{7,12}editor.{0,1}|.{0,2}to the editor.{0,30}|.{0,9}to the.{6,15}news", text, re.IGNORECASE)
        # using RegEx findall function to locate letters to the editor (and its variations)
        # re.I allows us to ignore cases
        # the word "college" has a lot of ocr noise to I decided to work around it

    if letters:
        for letter in letters:
            fulltext = text.split(letter, 1)[1]
            cleantext = fulltext.split("\n\n\n\n\n", 1)[0]
                # split string to get the specific chunk of text for letters to the editor
                    # 4 new lines may cause python to get more texts than we need, but it's a safer choice
                    # because of OCR noise, 3 new lines sometimes appear in the middle of an article
            insiderows = [filename, letters, cleantext]

    else:
        insiderows = [filename]

    row_list.append(insiderows)
        # append to the previously created list

    f.close

with open('LetterstotheEditor.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)
        # making csv
            # the "cleantext" appears when clicking the cell in excel
