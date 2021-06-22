#!/bin/bash

python user_gen_token.py
python server_gen_token.py
python user_search.py
python server_search.py

rm user_token user_query user_pad server_reply result.json
