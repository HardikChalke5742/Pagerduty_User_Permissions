import requests
import json
pagerduty_token = "API token"
pagerduty_users_list = []
pagerduty_usersoncall_list = []
pagerduty_usersnotoncall_list = []
pagerduty_headers = {
    "Accept": "applications/vnd.pagerduty+json;version=2",
    "Authorization": "Token token=" + pagerduty_token,
}
response_json = {}

# This function gives a list of all users present in PagerDuty


def get_pagerduty_users_list():

    try:
        response = requests.get(
            "https://api.pagerduty.com/users", headers=pagerduty_headers
        )
       # res = json.loads(response.content)
        if response.status_code != requests.codes.ok:
            print(
                "[ERROR] There was an error querying the PagerDuty api. Response Code: {}".format(
                    response.status_code)
            )
        else:
            response_json = response.json()
            for user in response_json['users']:
                pagerduty_users_list.append(user['id'])
    except:
        print("[ERROR] An error occurred retrieving users from PagerDuty")
    return pagerduty_users_list, response_json


# This function gives a list of all users on call

def get_pagerduty_usersoncall_list():

    try:
        response = requests.get(
            "https://api.pagerduty.com/oncalls", headers=pagerduty_headers
        )

       # res = json.loads(response.content)
        if response.status_code != requests.codes.ok:
            print(
                "[ERROR] There was an error querying the PagerDuty api. Response Code: {}".format(
                    response.status_code)
            )
        else:
            res_json = response.json()
            for oncall in res_json['oncalls']:
                pagerduty_usersoncall_list.append(oncall['user']['id'])
    except:
        print("[ERROR] An error occurred retrieving users from PagerDuty")
    return pagerduty_usersoncall_list

# This function returns list of users not on any schedule


def get_pagerduty_usersnotoncall_list():

    pagerduty_usersnotoncall_list = list(
        set(pagerduty_users_list) - set(pagerduty_usersoncall_list))
    return pagerduty_usersnotoncall_list

# This function updates the role of people not on schedule to stakeholders


def update_role_usersnotoncall(json1):

    pd_headers = {
        "Accept": "applications/vnd.pagerduty+json;version=2",
        "Authorization": "Token token=" + pagerduty_token,
        "Content-Type": "application/json",
    }
    data = {
        "user": {
            "role": "observer"
        }
    }

    for id in get_pagerduty_usersnotoncall_list():
        for user in json1['users']:
            if(id == user['id']):
                if(user['role'] == 'user'):
                    result = requests.put(
                        "https://api.pagerduty.com/users/" + id, headers=pd_headers, data=json.dumps(data))
                    print(result.json())


pagerduty_users_list, response_json = get_pagerduty_users_list()
pagerduty_usersoncall_list = get_pagerduty_usersoncall_list()
pagerduty_usersnotoncall_list = get_pagerduty_usersnotoncall_list()
update_role_usersnotoncall(response_json)
