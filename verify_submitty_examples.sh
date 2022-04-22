#!/bin/bash

# Pre clean up of python build folders
find . -type d -name __pycache__ -prune -exec rm -rf {} \;
find . -type d -name .pytest_cache -prune -exec rm -rf {} \;

# Check each example
for i in */ 
do 
  [[ -d "$i" ]] || break
  echo "Running ${i} example"; 

  cd "${i}" || exit

  # Run the submitty test for each submission
  for i in submissions/*/ 
  do 
    [[ -d "$i" ]] || break
    echo " - Check submission ${i}"; 


    # Copy over test files and submission
    rm -rf tmp

    mkdir tmp
    cp config/test_input/* tmp/
    cp "${i}"* tmp/

    # Execute test
    cd tmp || exit
    pipenv run python test_submitty.py 1> output.txt 2> error.txt
    status=$?

    if [[ $i == *"failing"* ]]
    then

      # Expected failing submission
      if [[ $status -ne 0 ]]
      then
        echo "   * Successful - Found incorrect submission"
      else
        echo "   --- Failed to find error ---"
        cat output.txt 
        echo "   --- Failed to find error ---"
        exit 1
      fi

    else 

      # Expecte successful submission
      if [[ $status -eq 0 ]]
      then
        echo "   * Successful - Confirmed solution"
      else
        echo "   --- Failed solution ---"
        cat output.txt 
        echo "   --- Failed solution ---"
        exit 1
      fi
    fi

    # clean up
    cd .. || exit
    rm -rf tmp

  # end of submission
  done

  # Move back up to project root.
  cd .. || exit

# end of example
done
