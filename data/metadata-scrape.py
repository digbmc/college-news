# metadata scraping
# import statements

from urllib import request # used to open/read webpages
from bs4 import BeautifulSoup # used to extract data from HTML
from time import sleep # used to tell the program to delay/pause
import csv # used to write the CSV file containing the metadata
import re # regular expressions, used to identify patterns from strings

# generating the list of URLs for the pages of search results
pages = [] # create a list
for index in range(0, 67): # run a loop for each number, 0 to 66
    url = "https://digitalcollections-staging.tricolib.brynmawr.edu/collections/bryn-mawr-college-news?page=" # define the base url
    url += str(index) # add the index number (the page number), which must be made into a string
    pages.append(url) # add the new url to the list of pages

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

# field names
fields = ["id", "date", "volume", "extent"]

#list of rows to go in the csv
rows = []

# getting the metadata from all of the entry pages
for entry in entries: # for each entry-specific url, do these steps:
    response = request.urlopen(entry) # open the webpage
    webContent = response.read() # read the HTML
    soup = BeautifulSoup(webContent, "html.parser") # create a BeautifulSoup object
    # select the date element and get the text from it
    date = soup.find("div", class_ = "dcdate field-value col-xs-8 no-gutter-right").get_text().strip()
    # select the extent element and get the text from it
    extent_text = soup.find("div", class_ = "mods-physicaldescription-extent-ms field-value col-xs-8 no-gutter-right").get_text().strip()
    # use regex to isolate the number of pages
    extent = re.search(r"\d+", extent_text).group(0)
    # select the item identifier element and get the text from it
    volume = soup.find("div", class_ = "mods-identifier-local-ms field-value col-xs-8 no-gutter-right").get_text().strip()
    # extract the object ID number
    id = re.search(r"\d+", entry).group(0)
    # add all of these to the CSV dictionary list
    row = {"id": id, "date": date, "volume": volume, "extent": extent}
    rows.append(row)
    sleep(1) # pause for one second

# write the csv
filename = "cn-metadata.csv"

with open(filename, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(rows)
