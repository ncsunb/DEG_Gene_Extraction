# Purpose
To extract names or data for Genes  expressed under a single or in two conditions.

# Requirements
1. To run this program, you must have Python installed.
_If you have macOS_ you may install [Python](https://docs.brew.sh/Homebrew-and-Python) through the [HomeBrew](https://brew.sh/) package manager by pasting these commands into your terminal : 
```
# install the HomeBrew package manager if you do not already have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install python
brew install python3
```
2. You must have the Python [pandas](https://pypi.org/project/pandas/) package installed. You may use pip to install this by pasting this command into your terminal: `pip3 install pandas`.
You may wish to do this inside a virtual enviroment (or if you use HomeBrew it may instruct you to use a virtual environment before attempting to install things with pip) by pasting these commands into your terninal:
```
mkdir venv # make a directory for your virtual environment

python3 -m venv venv
source venv/bin/activate
# or if you are on Windows and your filepaths use backslashes instead of forward slashes `venv\bin\activate`

pip3 install pandas
```

That should be it!
When you wish to deactivate your virtual environment after you are done using it, use this command:
```
deactivate
```

# Downloading this project
1. Start by installing [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), if you haven't already.

2. From the terminal, navigate (using `cd path-of-your-folder-where-you-want-it`, replacing path-of-your-folder-where-you-want-it with the actual path) to the directory you wish to download this project to. 

3. Paste the following command in your terminal `git clone https://github.com/ncsunb/DEG_Gene_Extraction.git`

That's it!


# Usage
To run this program **move your xlsx files to the same folder as this project**, then
1. Navigate to the folder containing the files for this project via the terminal (use `cd path-where-you-downloaded-this-project/DEG_Gene_Extraction/` or, if you are on Windows and your filepaths use backslashes instead of forward slashes, use `cd path-where-you-downloaded-this-project\DEG_Gene_Extraction\`), if you haven't already.

2. Activate your virtual environment (`source path-to-your-venv-folder/venv/bin/activate` or if you are on Windows and your filepaths use backslashes instead of forward slashes `source path-to-your-venv-folder\venv\bin\activate`), if you haven't already.

3. Paste this command into your terminal `python3 report_DEG.py` (or press 'Run' if you have it open in VSCode or another IDE).

4. You will be prompted to enter some information about your files:
example:
```
Please provide the file name of spreadsheet #1: RLS1MtvsWt.xlsx
Please provide the sheet name containing the genes within RLS1MtvsWt.xlsx: RLS1_TAP_TA_GO
Please provide the file name of spreadsheet #2: MultivsUni.xlsx
Please provide the sheet name containing the genes within MultivsUni.xlsx: master file
Generating report...

Done!
```
Look for the output files in the same folder as this project.
- One file will be named deg_report-{timestamp}.xlsx -- this is the xlsx file containing the data from the original xlsx files, but separated into different sheets based on the intersection and difference of gene names for the different files   
_e.g._, deg_report-20240725112005.xlsx
- There should be 3 .txt files named something like your 2 input file names with _unique_genes a timestamp, and common-genes-{timestamp}.txt; these files just contain the names of the unique and shared genes, respectively.   
_e.g._, RLS1MtvsWt_unique_genes-20240725112005.txt MultivsUni_unique_genes-20240725112005.txt and common_genes-20240725112005.txt
