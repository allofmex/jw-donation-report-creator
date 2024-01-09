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

>
- character set `Latin(-1)`
- field delimiter `;`
- String delimiter `"`
- quote all text cells)

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


Download this repositories files and extract in new folder

```
mkdir jw-donation-report-creator
wget -O - https://github.com/allofmex/jw-donation-report-creator/archive/master.tar.gz | tar xz -C jw-donation-report-creator --strip-components=1
cd jw-donation-report-creator

# Create virtual python environment

apt install python3.11-venv
python3 -m venv ~/jw_donation_form_tool_venv

source ~/jw_donation_form_tool_venv/bin/activate

pip3 install .
```


# Usage
Run like

```

cd /your/path/jw-donation-report-creator
# Activate virtual environment
source ~/jw_donation_form_tool_venv/bin/activate

 ./run.sh --source=mt940.csv --addressFile=user.csv --form=TO-67b.pdf --range=01.2022-12.2022
```
Result pdf files will be created in new subfolder `out/`


# Debugging

You may find this hints helpful in case of problems with result pdf file (may require additional packages

To check if form fields exist in result file

```
pdftk ./out/name.pdf dump_data_fields
```


## Dependencies

- PyPDF2 for reading und writing pdf (incl. it's form data)
- readchar for user input (single key without ENTER)

