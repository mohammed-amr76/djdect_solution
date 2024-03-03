# David Jones Data Engineer Coding Test

## Overview

This python project will implement the customer purchase amount segmentations, as required by the coding test. 

## Setup

### 1. Setup virtual environment

```bash

cd <local-path>/djdect_solution
python3 -m venv .venv
source ./bin/activate
pip3 install -r requirements.txt
```

### 2. Running tests
```bash
pip install pytest
python3 -m unittest discover tests
```

### 3. Executing main script
The primary script being run `main.py` can take several optional arguments, depending on how the `data/CustData.json` file has been defined.

#### Parameter details
- `--customer_id_column`:
    - Type: String
    - Description: Name of column that identifies different customers in data set
    - Default: 'customer_id'

- `--purchase_amount_column`:
    - Type: String
    - Description: Name of column that identifies customer purchase amounts
    - Default: 'purchase_amount'

- `--total_purchase_amount_column`:
    - Type: String
    - Description: Name of new column to be added, which will indicate total purchase amounts per customer
    - Default: 'total_purchase_amount'

- `--customer_segment_column`:
    - Type: String
    - Description: Name of new column to be added, which will indicate a customer"s segment, based on their total purchase amount
    - Default: 'customer_segment'

#### Parameter usage examples
```bash
cd src/

# if the customer identifier column and customer purchase amount column in the source file do match the above defaults
python3 main.py

# if the customer identifier column and customer purchase amount column in the source file don't match the above defaults
python3 main.py \
 --customer_id_column 'customer_name' \
 --purchase_amount_column 'customer_purchase'
 
# if the extra new columns are to be specifically named as well
python3 main.py \
 --customer_id_column 'customer_name' \
 --purchase_amount_column 'customer_purchase' \
 --total_purchase_amount_column 'total_customer_purchase' \
 --customer_segment_column 'customer_purchase_segment'
```




