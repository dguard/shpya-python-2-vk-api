import json
from collections import Counter
from urllib.request import urlopen
from functools import reduce


def get_followers(_id):
    """make request to vk api and returns user subscriptions as list."""
    url = 'http://api.vk.com/method/users.getSubscriptions.json?uid=' + _id.__str__()
    data = urlopen(url).read().decode('utf8')
    data = json.loads(data)
    return data['response']['users']['items']


def get_followers_in_range(start, end, completed, counter):
    """
    make request to api of vk and modify followers of users
    as dictionary in the following format: "uid: count of followers".
    """
    for _id in range(start, end):
        user_subs = get_followers(_id)
        for sub in user_subs:
            counter[sub] += 1
        print(_id, "/", end)
    completed.append(1)  # specify that thread is completed

# if this file was loaded NOT as module
if __name__ == "__main__":
    import _thread
    import math

    COUNT_OF_THREADS = 10
    COUNT_OF_USERS_TO_TEST = 100
    COUNT_OF_RESULTS = 30  # count of users with max followers

    threads_completed = []
    count_for_thread = math.floor(COUNT_OF_USERS_TO_TEST / COUNT_OF_THREADS)
    l = _thread.allocate_lock()

    list_counters = []

    # run threads
    for i in range(COUNT_OF_THREADS):
        counter = Counter()
        _thread.start_new_thread(get_followers_in_range, (
            count_for_thread*i + 1, count_for_thread*(i+1), threads_completed, counter)
        )
        list_counters.append(counter)

    # wait for completing all threads
    while len(threads_completed) != COUNT_OF_THREADS:
        pass

    # merge results from threads
    subs_counter = reduce(lambda x, y: x+y, list_counters, Counter())

    # show results
    for uid, val in subs_counter.most_common(COUNT_OF_RESULTS):
        print("пользователь \"%s\", подписчики: %s" % (uid, val,))
