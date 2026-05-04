logs = [ 
    "192.168.1.1 - - [01/Jan/2024] 'GET /index.html HTTP/1.1' 200",
    "10.0.0.5 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.0 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.2 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.0 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "10.5.5.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 404",
    "192.168.1.1 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "192.168.1.1 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "192.168.1.2 - - [01/Jan/2024] 'GET /admin/panel HTTP/1.1' 403",
    "10.0.0.5 - - [01/Jan/2024] 'GET /index.html HTTP/1.1' 200",
    "192.168.1.1 - - [01/Jan/2024] 'POST /login.php HTTP/1.1' 200"
]

def find_suspicious_activity():
    scanners = []
    suspicious = []
    for l in logs:
        parts = l.split("'")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 1: 
                result.append(part)     # добавляет один элемент в конец списка
            else:
                subparts = part.split(' ')
                subparts = filter(None, subparts)
                result.extend(subparts) # добавляет каждый элемент из другого списка по отдельности

        if result[len(result)-1] == '404':
            x = len(scanners)
            not_found = True
            if x == 0:
                scanners.append(result[0])
                not_found = False
            else:
                while x != 0:
                    if scanners[x-1] == result[0]:
                        not_found = False
                    x -= 1
            if not_found == True:
                scanners.append(result[0])

        if result[len(result)-1] == '403':
            x = len(suspicious)
            forbidden = True
            if x == 0:
                suspicious.append(result[0])
                forbidden = False
            else:
                while x != 0:
                    if suspicious[x-1] == result[0]:
                        forbidden = False
                    x -= 1
            if forbidden == True:
                suspicious.append(result[0])

    my_tuple = (scanners, suspicious)
    print(my_tuple)

find_suspicious_activity()