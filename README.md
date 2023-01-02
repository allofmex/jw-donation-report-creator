# Preparation

### PDF form
Original TO-67b has automaticall updating fields (total sum). 
As of now, we found no way to trigger this updates after this tool 
filled the other form fields and manually writing those fields
is not working as well (empty in result pdf)

### Address data
Prepare list of names and address
- csv
- filed delimiter is `;`
- Quote all text cells (with `"`)
- colums: "lastname, firstname";"street";"plz";"place"

##### Workarround
Manually edit original TO-67b pdf file
- remove both sum form fields (Gesamtbetrag, Gesamtsumme)
- add new simple text form fields instead (text-align right)
- edit script to use field names of newly created fields (see --verbose option to find field name)

(tested with https://dochub.com, registration required)

# Setup

```
pip3 install PyPDF2 readchar
```

PyPDF2 for reading und writing pdf (incl. it's form data)

readchar for user input (single key without ENTER)

