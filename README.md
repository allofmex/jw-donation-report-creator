# Tool to fill TO-67b form

This tool is usefull to automatically fill TO-67b pdf form based on bank account files
(Spendenbestätigungen aus Bankauszügen).
The resulting pdf files are complete and just need to be printed and signed.


# Preparation

### Configuration
Copy file `settings/example.config.yml` to `settings/contig.yml`
and update it with your own settings (congregation name,...)


### Bank account report
Export your bank account report (Kontoauszug) for the whole year in CSV-MT940 format


### Address data
Prepare list of names and address
- csv format
- filed delimiter is `;`
- Quote all text cells (with `"`)
- colums: "lastname, firstname";"street";"plz";"place"


### PDF form
Original TO-67b pdf file has automaticall updating fields (total, sum). 
As of now, we found no way to trigger this updates, after this tool 
filled the other form fields. Manually writing those fields
is not working as well (empty in result pdf)

##### Workarround
Manually edit original TO-67b pdf file (for example via online pdf editor like [https://dochub.com](https://dochub.com) (registration required))
- remove both sum form fields (Gesamtbetrag, Gesamtsumme)
- add new simple text form fields instead (text-align right)
- edit field names in `settings/config.yml` to use names of newly created fields in pdf
(you may use `run.py ... --verbose` option to find field name, should be last 2 in list)


# Setup
Install Python 3 if not already present

Add the following packages

```
pip3 install PyPDF2 readchar
```

> PyPDF2 for reading und writing pdf (incl. it's form data)

> readchar for user input (single key without ENTER)

Download this repositories files and extract in new folder

# Usage
Run like

```
 ./run.py --source=mt940.csv --addressFile=user.csv --form=TO-67b.pdf --range=01.2022-12.2022
```
Result pdf files will be created in new subfolder `out/`
