#!/bin/bash

return_answer=''
path_to_log="$(pwd)/../access.log"
rest_api_req_types=("POST" "GET " "PUT " "PATCH " "DELETE " "HEAD ")

# Total number of requests
unique_url="$(cat "$path_to_log" | sed 's/"//' | awk '{print $7}' | sort -u | wc -l)"
return_answer+="$(echo -e "Number of location requests  \n$unique_url")\n\n"

# Total number of request types
return_answer+="$(
echo "Total number of request types";
for var in ${rest_api_req_types[*]}; do
  number_req="$(cat "$path_to_log" | sed 's/"//' | awk '{print $6 " " $7}'| sort -u | grep "${var} " | wc -l)"
  if ((number_req > 0)); then
    echo -e "$var - $number_req"
  fi
done
)\n\n"

# Top 10 most sended requests
most_sended="$(cat "$path_to_log" | sed 's/"//' | awk 'BEGIN{FS=" "} {print $7}' | sort | uniq -c | sort -nr | head -n 10)"
return_answer+="$(echo -e "Top 10 most sended requests \n$most_sended")\n\n"

# Top 5 havy request with user errors
havy_req="$(cat $path_to_log | sed 's/"//' | awk 'BEGIN{FS=" "} {print $1 " " $7 " " $9 " " $10}' | grep -i " [4][0-9][0-9] " | sort -k 4 -nr | head -n 5)"
return_answer+="$(echo -e "Top 5 havy request with user errors \n$havy_req")\n\n"

# Top 5 users with most requests with server error
user_req="$(cat "$path_to_log" | sed 's/"//' | awk 'BEGIN{FS=" "} {print $1 " " $9}'| grep -i " [5][0-9][0-9]" | uniq -c | sort -nr| head -n 5)"
return_answer+="$(echo "Top 5 users with requests has 5xx errors \n$user_req")\n\n"

echo -e "$return_answer" > answer_bash.txt
