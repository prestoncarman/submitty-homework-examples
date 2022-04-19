#!/bin/bash

# Run the submitty test for each submission

for i in $(ls -d */); 
do 
  echo ${i}; 
done

# Copy over test files and submission
rm -rf tmp

mkdir tmp
cp config/test_input/* tmp/
cp submissions/solution/* tmp/

# Execute test
cd tmp
python3 test_submitty.py 1> output.txt 2> error.txt
status=$?
if [[ $status -eq 0 ]]
then
  echo "--- Successful - Confirmed solution ---"
else
  echo "--- Failed solution ---"
  cat output.txt 
  echo "--- Failed solution ---"
  exit 1
fi

# clean up
cd ..
rm -rf tmp


# Failed submission
mkdir tmp
cp config/test_input/* tmp/
cp submissions/failing_function/* tmp/

# Execute test
cd tmp
python3 test_submitty.py 1> output.txt 2> error.txt
status=$?
if [[ $status -ne 0 ]]
then
  echo "--- Successful - Found incorrect submission ---"
else
  echo "--- Failed to find error ---"
  cat output.txt 
  echo "--- Failed to find error ---"
  exit 1
fi

# clean up
cd ..
rm -rf tmp
