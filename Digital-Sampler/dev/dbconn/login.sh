#!/bin/bash

ssh -L  localhost:39954:localhost:39954 $username@cs506-team-35.cs.wisc.edu

echo $password'\r\n'

echo "1"