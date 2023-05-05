#!/bin/bash

# Pre clean up of python build folders
find . -type d -name __pycache__ -prune -exec rm -rf {} \;
find . -type d -name .pytest_cache -prune -exec rm -rf {} \;

temp="tmp"

# Check each example
for example in ./examples/*;
do 
  echo "Checking ${example}"; 
  [[ -d "$example" ]] || break
  echo "Running ${example} example"; 

  cd "${example}" || exit

  # Run the submitty test for each submission
  for submission in submissions/*/;
  do
    [[ -d "$submission" ]] || break
    echo " - Check submission ${submission}"; 

    # Copy over test files and submission
    rm -rf ${temp}

    mkdir ${temp}
    cp "${submission}"* ${temp}/
    cp config/test_input/* ${temp}/
    if  [[ -d "config/custom_validation_code" ]]
    then
      cp config/custom_validation_code/grader.py ${temp}/
      cp config/custom_validation_code/custom_validator_input.json ${temp}/
    fi

    # Execute test
    cd ${temp} || exit
    export PIPENV_PIPFILE=../../../Pipfile
    pipenv run python grade_submitty.py 1> STDOUT.txt 2> STDERR.txt
    status=$?

    if [[ $submission == *"failing"* ]]
    then

      # Expected failing submission
      if [[ $status -ne 0 ]]
      then
        echo "   * Successful - Found incorrect submission"
      else
        echo "   --- Failed to find error ---"
        cat STDOUT.txt 
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
        cat STDOUT.txt 
        echo "   --- Failed solution ---"
        exit 1
      fi
    fi

    # Custom validation output check
    if  [[ -f "grader.py" ]]
    then
      actual_file="validation_results.json"
      expected_file="validation_results_expected.json"

      pipenv run python grader.py 1> cv_output.txt 2> cv_error.txt

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
    rm -rf ${temp}

  # end of submission
  done

  # Move back up to project root.
  cd ../.. || exit

# end of example
done
