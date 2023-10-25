# Part 1

ETL to load transform the `officer_snapshot.csv` file.

The sample file `officer_snapshot.csv` is a mix of whitespace and character separated data.  Output

## Running

From root of the repository, run the following:

```
cd ./part1

pip install requirements.txt

python cma_officer.etl.py
```


## Solution:

- Given that it is not tab separated, I have used specific positions to extract the first several elements, then separated the second sections with the `'<'` separator.  
- The solution returns a new CSV with the data parsed into a new file with timestamp.  The minor validation on through data types ensures a minimum standard.

Resolved issues: 
- Where the postcode is missing it seems to be replaced by extra space characters.  This offsets the data and means that the `'<'` separated fields no longers start in the same position.  I have used regex to remove these extra spaces beyond the postcode section

Issues to resolve in the future:
- Several values are found in incorrect fields, for example there appears to be a postcode in the `county` section of one record (e.g. `county = '75093' & town = 'TEXAS'`)  More advanced pattern matching might be able to identify this, however this would require a bit of research given that any country address is permissable and postcodes formats vary so much.