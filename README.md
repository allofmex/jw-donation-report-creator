# Preparation

Original TO-67b has automaticall updating fields (total sum). 
As of now, we found no way to trigger this updates after this tool 
filled the other form fields and manually writing those fields
is not working as well (empty in result pdf)

### Workarround
Manually edit original TO-67b pdf file
- remove both sum form fields (Gesamtbetrag, Gesamtsumme)
- add new simple text form fields instead (text-align right)
- edit script to use field names of newly created fields

(tested with https://dochub.com, registration required)

# Setup

```
pip3 install PyPDF2
```

PyPDF2 for reading und writing pdf (incl. it's form data)

