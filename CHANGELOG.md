## 0.5.2 (2024-07-22)

### Refactor

- **model_data**: resolve issue with incorrect converting

## 0.5.1 (2024-07-22)

### Refactor

- **lambda_handler**: remove unneeded replace on dataframe

## 0.5.0 (2024-07-22)

### Feat

- **lambda_handler**: convert categorical variables to sets of indicators

## 0.4.2 (2024-04-22)

### Refactor

- **get_parameter_store_value**: set `WithDecryption` to true

## 0.4.1 (2024-04-19)

### Refactor

- **upload_to_output_bucket**: no longer use env var for bucket name
- **data_preprocessing**: remove unnecassary environment variable

## 0.4.0 (2024-04-07)

### Feat

- **pre-commit-config**: update black and commitizen versions

## 0.3.0 (2024-04-02)

### Feat

- **data_preprocessing**: add function to get value of parameter store

## 0.2.6 (2024-02-24)

### Refactor

- **upload_to_output_bucket**: change output dir to s3 after preprocessing

## 0.2.5 (2024-02-23)

### Refactor

- **data_preprocessing**: add todo for convert catergorial variables to sets

## 0.2.4 (2024-02-19)

### Refactor

- **lambda_handler**: update logging statement to mention the event

## 0.2.3 (2024-02-19)

### Refactor

- **pre_checks_before_processing**: loop through all tags rather than checking first index

## 0.2.2 (2024-01-31)

### Refactor

- **example_responses**: fix typo in file name

## 0.2.1 (2024-01-14)

### Refactor

- **data_preprocessing**: include boto3 client as args for aws operations

## 0.2.0 (2024-01-08)

### Feat

- **data_preprocessing**: initial data preprocessing functions

## 0.1.0 (2024-01-06)

### Feat

- **git**: initial gitignore and pre-commit hooks
- **init**: pseudo code for data preprocessing steps

### Fix

- **models**: incorrect key for getting the object

### Refactor

- **data_preprocessing**: rename file to use underscores, rather than hypen
