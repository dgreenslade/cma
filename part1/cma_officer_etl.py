import re
import os
import time
import logging
import pandas as pd
from datetime import datetime


def parse_officers(file: str) -> pd.DataFrame:
    """Parse input file into pandas dataframe with correct data types."""
    data = []
    try:
        with open(file) as f:
            for line in f:
                try:
                    officer = {
                        "comp_num": int(line[0:8]),
                        "pers_num": int(line[8:20]),
                        "appnt_date": datetime.strptime(line[27:35], "%Y%m%d").date(),
                        "postcode": line[43:51].strip(),
                    }

                    dob_search = re.search(r"^\s*\d{6}", line[51:])
                    officer["dob_yyyymm"] = int(dob_search[0]) if dob_search else None

                    cleaned_line = re.sub(r"^\s*\d+", "", line[57:])
                    sep_data = [x.strip() for x in cleaned_line.split("<")]

                    officer.update(
                        {
                            "title": sep_data[0],
                            "first_name": sep_data[1],
                            "last_name": sep_data[2],
                            "honours": sep_data[3],
                            "care_of": sep_data[4],
                            "po_box": sep_data[5],
                            "address_1": sep_data[6],
                            "address_2": sep_data[7],
                            "town": sep_data[8],
                            "county": sep_data[9],
                            "country": sep_data[10],
                        }
                    )

                    data.append(officer)
                except Exception:
                    logging.warning(f"Error parsing row {line}", exc_info=True)

        return pd.DataFrame(data).convert_dtypes()

    except FileNotFoundError:
        logging.error(f"Error reading & processing file {file}", exc_info=True)


def main():
    """Call data parsing function on input file, and saves the reformatted data in a new file."""
    logging.getLogger().setLevel(logging.WARN)

    input_file = os.path.join(os.getcwd(), "data_input", "officer_snapshot.txt")
    data = parse_officers(input_file)

    output_file = os.path.join(
        os.getcwd(),
        "data_output",
        f'officers_{time.strftime("%Y%m%d_%H%M%S")}.csv',
    )
    data.to_csv(output_file)

    print(f"Successfully output to {output_file}")


if __name__ == "__main__":
    main()
