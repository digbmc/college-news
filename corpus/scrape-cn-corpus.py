# import statements
from urllib import request # used to open/read webpages
from bs4 import BeautifulSoup # used to extract data from HTML
from time import sleep # used to tell the program to delay/pause
import os # used to make a folder

# generating the list of URLs for the pages of search results
pages = [] # create a list
for index in range(0, 67): # run a loop for each number, 0 to 66
    # define the base url
    url = "https://digitalcollections-staging.tricolib.brynmawr.edu/collections/bryn-mawr-college-news?page="
    # add the index number (the page number), which must be made into a string
    url += str(index)
    # add the new url to the list of pages
    pages.append(url)

# getting all of the links from each search results page
entries = [] # create a list
for page in pages: # for every url defined in pages, do these steps:
    response = request.urlopen(page) # open the webpage
    webContent = response.read() # read the HTML
    soup = BeautifulSoup(webContent, "html.parser") # create a BeautifulSoup object 
    # filter the soup to include only the specific div tags that have the links we want
    div_links = soup.find_all("div", class_="solr-fields islandora-inline-metadata col-xs-12 col-sm-8 col-md-9")
    # the base URL for the newspaper issues
    url_base = "https://digitalcollections-staging.tricolib.brynmawr.edu"
    for link in div_links: # for every div tag that we just filtered out:
        link_tag = link.find("a") # take the link tag element
        relative_url = link_tag.get("href") # get the url from the link tag
        entries.append(url_base + relative_url) # add the full url to the list of entries
    sleep(1) # pause for one second

# if there isn't already a folder named "issues", make one  
if os.path.exists("issues") == False: ## Changed conditional (ATM - 6/15)
        os.mkdir("issues") ## changed from makedirs() to mkdir()

# getting the text from all of the entry pages
for entry in entries: # for each entry-specific url, do these steps:
    response = request.urlopen(entry) # open the webpage
    webContent = response.read() # read the HTML
    soup = BeautifulSoup(webContent, "html.parser") # create a BeautifulSoup object
    body = soup.find("p", class_="ocr_full_text text-left") # select the OCR text element
    text = body.get_text() # get the text from the OCR text element
    # select the date element and get the text from it
    date = soup.find("div", class_ = "dcdate field-value col-xs-8 no-gutter-right").get_text()
    # create a filename using the date from the previous line
    filename = "issues/cn" + str(date).strip() + ".txt" 
    f = open(filename, "w") # create a file with the filename defined above
    f.write(text) # copy the OCR text into the new file
    f.close() # close the file
    sleep(1) # pause for one second



# Al Nash
# 6/15/21

"""
ATM notes: 'issues' make directory did not work
"""