#!/bin/bash

# Pre clean up of python build folders
find . -type d -name __pycache__ -prune -exec rm -rf {} \;
find . -type d -name .pytest_cache -prune -exec rm -rf {} \;

# Check each example
for example in */ 
do 
  [[ -d "$example" ]] || break
  echo "Running ${example} example"; 

  cd "${example}" || exit

  # Run the submitty test for each submission
  for submission in submissions/*/ 
  do 
    [[ -d "$submission" ]] || break
    echo " - Check submission ${submission}"; 


    # Copy over test files and submission
    rm -rf tmp

    mkdir tmp
    cp "${submission}"* tmp/
    cp config/test_input/* tmp/

    # Execute test
    cd tmp || exit
    pipenv run python test_submitty.py 1> output.txt 2> error.txt
    status=$?

    if [[ $submission == *"failing"* ]]
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

      # Expected successful submission
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

    # Custom validation output check
    if  [[ -f "custom_validation.py" ]]
    then
      actual_file="cv_output.txt"
      expected_file="custom_validation_stdout.txt"

      pipenv run python custom_validation.py 1> cv_output.txt 2> cv_error.txt

      diff "$actual_file" "$expected_file"
      status=$?

      if [[ $status -ne 0 ]]
      then
        printf 'The actual file ("%s") is different from expected ("%s")\n' "$actual_file" "$expected_file"
        exit $status
      else
        echo "   * Successful - Confirmed custom validation result"
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
