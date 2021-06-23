#!/bin/bash
read -p "Enter User ID: "  id
read -p "Enter Keyword 1: "  w1
read -p "Enter Keyword 2: "  w2


python user_gen_token.py $id $w1 $w2
python server_gen_token.py
python user_search.py $id
python server_search.py
python user_result.py $id

#rm user_token user_query user_pad server_reply result.json
