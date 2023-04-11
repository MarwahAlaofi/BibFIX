from selenium import webdriver
import logging
import sys
import argparse
from utilities import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# read command arguments
argv = sys.argv[1:]

# setup command argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile', nargs=1, type=argparse.FileType('r'))
parser.add_argument('-o', '--outfile', nargs=1, type=argparse.FileType('w'))
parser.add_argument('-k', '--keepkey', action='store_true')
parser.add_argument('-s', '--short', action='store_true')
parser.add_argument('-src', '--source', nargs='?', type=str, default='dblp')
parser.add_argument('-hd', '--hide', action='store_true')  # to hide the browser window

'''example of a full shell command to fetch bibtex from acm dl,
set them to the short form (-s) and keep the citation keys (-k):'''
# python bibfix.py -i bib_to_fix.bib -o fixed_bib.bib -src acm -k -s


try:
    args = parser.parse_args()
except:
    logging.error("Error parsing arguments")
    exit()

# read bibtex records from the provided input file
try:
    logging.info("Reading the bibtex file..")
    with args.infile[0] as bibtex_file:
        bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

except Exception as e:
    logging.error("invalid bibtex formatting!")
    print(e)
    exit()

# setup the web driver to chrome and provide the path of the downloaded driver
# (this could be customised to use other browsers)
logging.info("Getting things ready... 🔥 ")
chrome_options = webdriver.ChromeOptions()
if args.hide == True:
    chrome_options.add_argument("--headless")

driver = webdriver.Chrome('tools/chromedriver', options=chrome_options)

logging.info("Starting to retrieve bibtex entries from " + args.source + "...")
titles = []
bibtex_results = []
failed_bibtex = []

ref_no = 1
for en in bib_database.get_entry_list():
    # remove non-alphanumerical charachters from the paper title (e.g., })
    en['title'] = preprocess_title(en['title'])
    print("Ref [" + str("%03d" % (ref_no,)) + "]: " + en['title'][0:30] + "... ", end="")

    if args.source == "acm":
        # create a url and provide the title to be searched
        url = "https://dl.acm.org/action/doSearch?AllField=" + en['title']
        driver.get(url)
        try:
            cite_btn = driver.find_element_by_xpath('// *[ @ id = "pb-page-content"]/div/main/div[1]/div/div[2]/div/ul/li[1]/div[2]/div[2]/div/ \
                                          div[3]/div/div[3]/ul[1]/li[1]/a')
            cite_btn.click()
            driver.implicitly_wait(10)

            bibtex_text = driver.find_element_by_xpath('//*[@id="selectedTab"]/div/pre/div/div').get_attribute(
                'innerHTML')
            parsed_bibtex = bibtexparser.bparser.BibTexParser(common_strings=True).parse(bibtex_str=bibtex_text)

            parsed_bibtex.entries[0]['title'] = preprocess_title(parsed_bibtex.entries[0]['title'])
            if parsed_bibtex.entries[0]['title'] != en['title']:
                raise Exception()

            if args.keepkey:
                parsed_bibtex.entries[0]['ID'] = en['ID']

            bibtex_str = bibtexparser.dumps(parsed_bibtex)
            bibtex_results.append((ref_no, format_bib_entry(bibtex_str)))
            print(" ---> Done   ✅ ")

        except:
            # failed_bibtex_str = json.dumps(en)
            failed_bibtex.append((ref_no, format_bib_entry(en)))
            print(" ---> Failed 🙈 ")

    else:  # If dblp
        # create a url and provide the title to be searched
        url = "https://dblp.org/search?q=" + en['title']

        driver.get(url)

        try:
            article_list = driver.find_element_by_xpath('//*[@id="completesearch-publs"]/div/ul')
            first_pup = article_list.find_elements_by_class_name('publ')[0]
            first_pup_links = first_pup.find_elements_by_tag_name('a')
            for link in first_pup_links:
                # print(link.get_attribute('href'))
                if link.get_attribute('href').endswith('bibtex'):
                    break
            first_pup_bibtex_url = link.get_attribute('href')
            driver.get(first_pup_bibtex_url)
            bibtex_text = driver.find_element_by_xpath('/html/body/div[2]/div[4]/pre').get_attribute('innerHTML')
            parsed_bibtex = bibtexparser.bparser.BibTexParser(common_strings=True).parse(bibtex_str=bibtex_text)
            parsed_bibtex.entries[0]['title'] = preprocess_title(parsed_bibtex.entries[0]['title'])

            if parsed_bibtex.entries[0]['title'] != en['title']:
                raise Exception()

            if args.keepkey:
                parsed_bibtex.entries[0]['ID'] = en['ID'] # keep the original keys
            bibtex_str = bibtexparser.dumps(parsed_bibtex)
            bibtex_results.append((ref_no, format_bib_entry(bibtex_str)))
            print(" ---> Done   ✅ ")

        except:
            # failed_bibtex_str = json.dumps(en)
            failed_bibtex.append((ref_no, format_bib_entry(en)))
            print(" ---> Failed 🙈 ")

    ref_no = ref_no + 1

# print a summary
logging.info("... Task Completed 🥳 ...")
print(".... .... .... .... .... .... .... .... .... .... ....")

print("Summary: ")
print("total ...........  " + str("%02d" % (len(bib_database.get_entry_list(), ))))
print("Succeeded 🎉 ....  " + str("%02d" % (len(bibtex_results, ))) + "/" + str(
    "%02d" % (len(bib_database.get_entry_list(), ))))
print("Failed 🫣 .......  " + str(len(failed_bibtex)) + "/" + str(len(bib_database.get_entry_list())))

print(".... .... .... .... .... .... .... .... .... .... ....")
# save the retrieved bibtex records to the supplied output file path
with args.outfile[0] as f:
    for r in bibtex_results:
        f.write(r[1] + '\n')
    print(" 📃️ Bibtex consistent records are stored @ " + args.outfile[0].name + "...")

    failed_bib_file_name = str.split(args.outfile[0].name, '.')[0] + '_failed.bib'
    with open(failed_bib_file_name, 'w') as f:
        for r in failed_bibtex:
            f.write(r[1] + '\n')
        print(" 📃️ Bibtex failed records are stored @ " + failed_bib_file_name + "...")

print("......................................................")

# todo: check for ref with more than 1 match
# todo: the short/long version
