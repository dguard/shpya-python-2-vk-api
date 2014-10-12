import json
from urllib.request import urlopen


def get_followers(_id):
    """make request to vk api and returns user subscriptions as list."""
    url = 'http://api.vk.com/method/users.getSubscriptions.json?uid=' + _id.__str__()
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    return data['response']['users']['items']


def get_followers_in_range(start, end, completed, summary):
    """
    make request to api of vk and modify followers of users
    as dictionary in the following format: "uid: count of followers".
    """
    for _id in range(start, end):
        user_subs = get_followers(_id)
        for sub in user_subs:
            if sub not in summary:
                summary[sub] = 1
            else:
                summary[sub] += 1
        print(_id, "/", end)
    completed.append(1)  # specify that thread is completed

# if this file was loaded NOT as module
if __name__ == "__main__":
    import _thread
    import math
    import operator

    COUNT_OF_THREADS = 10
    COUNT_OF_USERS_TO_TEST = 100
    COUNT_OF_RESULTS = 30  # count of users with max followers

    threads_completed = []
    count_for_thread = math.floor(COUNT_OF_USERS_TO_TEST / COUNT_OF_THREADS)
    l = _thread.allocate_lock()

    list_summary = []

    # run threads
    for i in range(COUNT_OF_THREADS):
        _sum = {}
        _thread.start_new_thread(get_followers_in_range, (
            count_for_thread*i + 1, count_for_thread*(i+1), threads_completed, _sum)
        )
        list_summary.append(_sum)

    # wait for completing all threads
    while len(threads_completed) != COUNT_OF_THREADS:
        pass

    # merge results from threads
    dict_subs = {}
    for i in range(COUNT_OF_THREADS):
        for uid, val in list_summary[i].items():
            if uid not in dict_subs:
                dict_subs[uid] = val
            else:
                dict_subs[uid] += val

    # sort dictionary and get first 30 users with max followers as list
    list_subs = list(sorted(dict_subs.items(), key=operator.itemgetter(1), reverse=True)[:COUNT_OF_RESULTS])

    # show results
    for uid, val in list_subs:
        print("пользователь \"%s\", подписчики: %s" % (uid, val,))
