# BibFIX

## Description
BibFIX aims to automatically generate *complete*, *consistent* and
*well-formatted* BibTeX records for papers published in 
Computer/Information Science venues given a .bib file.

### Use Case
Your reference bibTeX records were collected/generated using
different sources/methods (e.g., google scholar, dblp, auto-genearted using
a reference manager..etc) resulting in a reference list with inconsistent and incomplete bibTeX records.
You need a quick and easy way to fill in missing fields and regenerate the bibTeX records where all records follow one style using [dblp](https://dblp.org/) or [ACM DL](https://dl.acm.org/). 


## Example
Given this [sample input file](bibtex/bib_sample.bib) at `bibtex/bib_sample.bib`, the following command generates this [output file](bibtex/output_bib.bib) at `bibtex/output_bib.bib` using BibTeX records sourced from [dblp](https://dblp.org/):

```
python bibfix.py -i bibtex/bib_sample.bib -o bibtex/output_bib.bib -src dblp
```
records failed to be retrieved (three in this case) are written into a [seperate file](bibtex/output_bib_failed.bib).

A summary of the process is given in the following run:
```
2022-08-19 20:25:49,727 - Reading the bibtex file..
2022-08-19 20:25:49,872 - Getting things ready... 🔥 
2022-08-20 00:15:23,070 - Starting to retrieve bibtex entries from dblp...
Ref [001]: answer interaction in non-fact...  ---> Done   ✅ 
Ref [002]: multi-method evaluation: lever...  ---> Done   ✅ 
Ref [003]: an intent taxonomy for questio...  ---> Done   ✅ 
::
Ref [026]: generating relevant and inform...  ---> Failed 🙈 
Ref [027]: ontological user profiling in ...  ---> Done   ✅ 
Ref [028]: technological frames: making s...  ---> Done   ✅ 
2022-08-20 00:15:58,199 - ... Task Completed 🥳 ...
.... .... .... .... .... .... .... .... .... .... ....
Summary: 
total ...........  28
Succeeded 🎉 ....  25/28
Failed 🫣 .......  3/28
.... .... .... .... .... .... .... .... .... .... ....
 📃️ Bibtex consistent records are stored @ bibtex/output_bib.bib...
 📃️ Bibtex failed records are stored @ bibtex/output_bib_failed.bib...
......................................................
```

## How to use?
1. **Download** and **install** [python](https://www.python.org/downloads/) 
_(ensure it is included in your environment path)_
2. **Download** [Chrome Driver](https://chromedriver.chromium.org/downloads)
_(choose the version compatible with the Chrome browser installed on your machine)_
3. **Clone** the project.
4. **Place** the downloaded chrome driver in the `tools` directory.  
5. **Install** `selenium==3.141.0` and `bibtexparser`
6. **Run** bibfix.py using the options described below:

| Option &nbsp;&nbsp;  | Description |
| ------------- | ------------- |
| <nobr>-i (--infile) </nobr> | sets the path to the input .bib file.  |
| <nobr> -o (--outfile)</nobr>  | sets the path of the generated output .bib file.  |
| <nobr>-src (--source) </nobr> | sets the desired source of the BibTeX records [dblp or acm]. By default, the script uses dblp to source bibtex records.  |
| <nobr>-k (--keepkeys)</nobr>  | keeps the keys (labels) of the BibTex unchanged so the compile is not affected. It is set to False by default.  |
| <nobr>-hd (--hide) </nobr> | hides the browser instance that is used to scrape bibTeX records. It is set to False by default.  |
| <nobr>-s (--short)</nobr>  | sets the script to use the short version of conference/journal names (under development). It is set to False by default.   |

- Enjoy! 🚀😉

## Limitations and further details
- There are many assumptions used to build this script. For example, the script uses paper titles to search for bib records and assumes that first matching title is the correct one. 
- As opposed to dblp, when using ACM DL as a source for bib records, only papers published in ACM can be found. The rest of the papers will fail and you may want to run the failed list using dblp or generate them manually following the same style. 
- As the script scrapes the content out of web pages, things are not predictable and changes to the structure of web pages can happen which may break the script. Also, the speed of the script is highly dependent on the time taken to load web pages. ACM DL pages take about 5 times more time than dblp web pages to load.  
- The script can be configured to suite one's bibtex formatting preferences. For example, you can change bibtex keys to follow a certain naming convention or change the order of bibtex fields...etc.   
