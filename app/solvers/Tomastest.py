shablon5 = '202200000020001101001001202001'
shablon4 = '100021101001002020200020001020'
shablon3 = '010100200202100002020102010010'
shablon2 = '020010020010010000112010020202'
shablon1 = '001002012100220210000200100100'
def tomas(string: str) -> str:

    n = [0, 0, 0, 0, 0]
    for i in range(30):
        if string[i] == shablon1[i]:
            n[0] += 1
        elif string[i] == shablon2[i]:
            n[1] += 1
        elif string[i] == shablon3[i]:
            n[2] += 1
        elif string[i] == shablon4[i]:
            n[3] += 1
        elif string[i] == shablon5[i]:
            n[4] += 1

    im = 0
    for i, ztip in enumerate(n):
        if ztip >= n[im]:
            im = i
   # print(n)
    match im:
        case 0:
            return "Соперничество"
        case 1:
            return  "Сотрудничество"
        case 2:
            return "Компромисс"
        case 3:
            return "Избегание"
        case 4:
            return "Приспособление"




