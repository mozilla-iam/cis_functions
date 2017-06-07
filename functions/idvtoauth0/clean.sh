#!/bin/bash

### Cleanup virtualenv post-deploy
find . -d -not -name ".." -not -name "." -not -name "*.json" -not -name "clean.sh" -not -name "main.py" -not -name "authzero.py" -not -name "function.*" -not -name "utils.py" -not -name "requirements.txt" | xargs rm -fr &> /dev/null
find . -type f -name "*.py" -name "*.so" -not -name "*.json" -not -name "clean.sh" -not -name "main.py"  -not -name "authzero.py" -not -name "utils.py" -not -name "function.*" -not -name "requirements.txt" | xargs rm -fr &> /dev/null
find . -type f -name "*.py" -name "*.so" -not -name "*.json" -not -name "clean.sh" -not -name "utils.py" -not -name "authzero.py" -not -name "function.*" -not -name "requirements.txt" | xargs rm -fr &> /dev/null
