import logging
import pandas as pd
import re
from datetime import datetime
import time

def parse_officers(file:str)->dict:         
    try:
        with open(file) as f:
            data = []
            for line in f:
                officer = {}
                try:         
                    # The first 5 elements are at fixed positions, so use list indices. 
                    # Convert data type where appropriate for minimal validation
                    
                    # Company Number with validation as this seems like multi-part primary key
                    officer['comp_num'] = int(line[0:8])           #e.g. 88958775
                    if len(str(officer['comp_num'])) != 8:
                        raise ValueError(
                            f'Company Number {officer["comp_num"]} is not 8 digits'
                        )
                    # Person Number with validation as this seems like multi-part primary key
                    officer['pers_num'] = int(line[8:20])          #e.g. 556806630001
                    if len(str(officer['pers_num'])) != 12:
                        raise ValueError(
                            f'Person Number {officer["pers_num"]} is not 12 digits'
                        )
                    officer['appnt_date'] = datetime.strptime(line[27:35],'%Y%m%d').date()   #e.g. 20190429
                    officer['postcode'] = line[43:51].strip()      #e.g. CR4 1XW
                    
                    # Where postcode missing, seems replaced by extra whitespace and shifts data right.
                    # From end of normal postcode position, find first non-space digits if fits YYYYMM
                    # e.g line 135 & 142 in sample
                    dob_search = re.search(r'^\s*\d{6}', line[51:])
                    officer['dob_yyyymm'] = int(dob_search[0]) if dob_search is not None else None
                        
                    # The name & address info starts at first non-digit element after fixed position 
                    # then separated by '<'
                    # - Remove first digit chars from position 57 onwards to account for rare extra spaces
                    # - from missing postcode records
                    cleaned_line = re.sub(r'^\s*\d+','', line[57:])
                    sep_data = [x.strip() for x in cleaned_line.split('<')]
                    
                    officer['title'] = sep_data[0]
                    officer['first_name'] = sep_data[1]
                    officer['last_name'] = sep_data[2]
                    officer['honours'] = sep_data[3]
                    officer['care_of'] = sep_data[4]
                    officer['po_box'] = sep_data[5]
                    officer['address_1'] = sep_data[6]
                    officer['address_2'] = sep_data[7]
                    officer['town'] = sep_data[8]
                    officer['county'] = sep_data[9]
                    officer['country'] = sep_data[10]
                    
                    data.append(officer)
                except Exception:
                    logging.warn(f'Error parsing row {line}', exc_info=True)
                    
        # Convert list of dicts to pandas dataframe with correct data types 
        return pd.DataFrame.from_dict(data).convert_dtypes()
    
    except Exception:
            logging.error(f'Error reading & processing file {file}', exc_info=True)


def main():
    """Main workflow takes input file from ./input_data/ parses data into dict and pandas then  
    outputs CSV to ./data_output/"""
    
    logging.getLogger().setLevel(logging.WARN)

    input_file = './part1/data_input/officer_snapshot.txt'
    data = parse_officers(input_file)
    
    output_file = f'./part1/data_output/officers_{time.strftime("%Y%m%d_%H%M%S")}.csv'
    data.to_csv(output_file)
    
    print(f'Successfully output to {output_file}')    

          
if __name__ == '__main__':
    main()
