@echo off
REM Run Python File 1 and show output
echo Extracting Data From GEM Portal
python "C:\Users\20353979\Downloads\chromedriver-win64\value_csv_update2.py"
echo Finished running value_csv_update2.py Extracted data from GEM Portal.

REM Run Python File 2 and show output
echo Removing Rows From bid_data.csv
python "C:\Users\20353979\Downloads\chromedriver-win64\Filter_CSV\remove_row.py"
echo Finished running remove_row.py filtered bids file removing short bids.

REM Run Python File 3 and show output
echo Getting Filtered Output
python "C:\Users\20353979\Downloads\chromedriver-win64\Filter_CSV\filter_csv.py"
echo Finished running filter_csv.py generated finale output for GEM Portal.

REM Run Python File 4 and show output
echo Getting Filtered Output from DEFPROC
python "C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\sel_ext_defproc.py"
echo Finished running sel_ext_defproc.py generated finale output for defproc.

REM Run Python File 5 and show output
echo Getting Filtered Output from GARDEN SHIPYARD
python "C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\sel_ext_garden.py"
echo Finished running sel_ext_garden.py generated finale output for GARDEN SHIPYARD.

REM Run Python File 6 and show output
echo Getting Filtered Output from GOA SHIPYARD
python "C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\sel_ext_goa.py"
echo Finished running sel_ext_goa.py generated finale output for GOA SHIPYARD.

REM Run Python File 7 and show output
echo Getting Filtered Output from HINDUSTAN SHIPYARD
python "C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\sel_ext_hindustan.py"
echo Finished running sel_ext_hindustan generated finale output for HINDUSTAN SHIPYARD.

REM Run Python File 8 and show output
echo Getting Filtered Output from MAZGAON SHIPYARD
python "C:\Users\20353979\Desktop\Intern Rohit\DEFPROC_SEL\sel_ext_mazgaon.py"
echo Finished running sel_ext_mazgaon.py generated finale output for MAZGAON SHIPYARD.


echo All Python scripts executed successfully!
pause
