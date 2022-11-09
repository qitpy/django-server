#!/bin/sh
input() {
  echo Command Line inteface:
  echo 1 - BUILD
  echo 2 - RUN
  echo 3 - TEST
  echo 4 - CORVERAGE
  echo 5 - FLAKE8
  echo 6 - exit
  read -p 'Your choice: ' command
  echo
  if ! [[ "$command" =~ ^[+-]?[0-9]+\.?[0-9]*$ ]] || ! [[ "$command" =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]
  then
      echo "Inputs must be a numbers"
      return 0
  fi
  return "$command"
}

job() {
  number=0
  while [ $number != 0 ]
  do
    input
    number=$?
    if [ $number == 1 ]
    then
      echo 1 nha
    elif [ $number == 2 ]
    then
      echo 2 nha
    elif [ $number == 3 ]
    then
      echo 3 nha
    elif [ $number == 4 ]
    then
      echo 4 nha
    elif [ $number == 5 ]
    then
      echo 5 nha
    elif [ $number == 6 ]
    then
      exit 0
    fi
    number=0
  done
}

job






