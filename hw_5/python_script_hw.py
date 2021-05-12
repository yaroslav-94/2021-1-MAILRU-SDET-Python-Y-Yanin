import os

path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
path_to_log_file = path + "/access.log"
path_to_result_file = path + "/answer_python_script.txt"

rest_api_req_types = [
    "POST",
    "GET",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD"
]

all_req_types = set()
dict_protocols = {}
request_types = {}
top_ten_pop_req = {}
top_five_havy_req = {}
top_five_users = {}

with open(path_to_log_file, "r") as f:
    for line in f:
        arr = line.replace("\"", "").replace("[", "").replace("]", "").split(" ")

        user_url = arr[0]
        request_type = arr[5]
        request_url = arr[6]
        request_code = int(arr[8])
        request_size = int(arr[9]) if arr[9].isalnum() else None

        if rest_api_req_types.count(request_type) >= 0:
            all_req_types.add(request_type)

            # Find location for each url
            if request_type and request_url not in dict_protocols.keys():
                dict_protocols[request_url] = {1}

            # Find number of request's types
            if request_type not in request_types.keys():
                request_types[request_type] = {request_url}
            elif request_type in request_types.keys():
                request_types[request_type].add(request_url)

            # Find top 10 most sended requests
            if request_url not in top_ten_pop_req.keys():
                top_ten_pop_req[request_url] = 1
            elif request_url in top_ten_pop_req.keys():
                top_ten_pop_req[request_url] += 1

            # Find top 5 big size requests with 500>error>=400
            if request_size and request_code:
                if (len(top_five_havy_req) < 5) and (500 > request_code >= 400):
                    top_five_havy_req[request_size] = [request_url, request_code, user_url]
                elif (500 > request_code >= 400) and request_size and request_size >= min(top_five_havy_req.keys()) and \
                        len(top_five_havy_req) == 5:
                    top_five_havy_req.pop(min(top_five_havy_req.keys()))
                    top_five_havy_req[request_size] = [request_url, request_code, user_url]
    
            # Find users which send most request with 600>status code>=500
            if request_code:
                if (user_url not in top_five_users) and (600 > request_code >= 500):
                    top_five_users[user_url] = 1
                elif user_url in top_five_users and (600 > request_code >= 500):
                    top_five_users[user_url] += 1

prot_size = 0
for i in dict_protocols.keys():
    prot_size += len(dict_protocols.get(i))

with open(path_to_result_file, "w+") as f:
    f.write(f"Number of location requests:\n{prot_size}\n\n")

    f.write("Total number of request types:\n")
    for i in request_types.keys():
        f.write(f"{i} - {len(request_types.get(i))}\n")
    f.write("\n")

    fl = 1
    f.write("Top 10 most sended requests:\n")
    for w in sorted(top_ten_pop_req, key=top_ten_pop_req.get, reverse=True):
        if fl < 11:
            f.write(f"{w} - {top_ten_pop_req.get(w)}\n")
            fl += 1
        else:
            break
    f.write("\n")

    f.write("Top 5 havy request with user errors:\n")
    for i in top_five_havy_req.keys():
        info = top_five_havy_req.get(i)
        f.write(f"url: {info[0]}, request status code: {info[1]}, request size: {i}, ip address: {info[2]}\n")
    f.write("\n")

    fl = 1
    f.write("Top 5 users with requests has 5xx errors:\n")
    for w in sorted(top_five_users, key=top_five_users.get, reverse=True):
        if fl < 6:
            f.write(f"{w} - {top_five_users.get(w)}\n")
            fl += 1
        else:
            break
