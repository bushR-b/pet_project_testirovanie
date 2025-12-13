def motiv(lst: list) -> str:
    shablon = [['1', '2', '3', '4', '5'],
               ['3', '2','5', '4', '1'],
               ['5', '1', '2', '3', '4'],
               ['1', '4', '3', '5', '2'],
               ['2', '1', '3', '5', '4'],
               ['2', '1', '3', '4', '5'],
               ['3', '2', '1', '5', '4'],
               ['4', '1', '3', '5', '2'],
               ['3', '1', '4', '2', '5'],
               ['3', '2', '4', '1', '5'],
               ['1','2', '4', '5', '3'],
               ['2', '3', '5', '1', '4'],
               ['1', '3', '2', '4', '5'],
               ['4', '3', '2', '1', '5']]
    
    mm = [[0 for i in range(5)] for j in range(14)]

    tip = [0 for i in range(5)]


    for i in range(14):
        k = lst[i]
        for j in range(5):
            if shablon[i][j] == k:
                index = j
                mm[i][index] = 1

    for j in range(5):
        tip[j] = 0
        for i in range(14):
            tip[j] += mm[i][j]

    im = 0
    for i, ztip in enumerate(tip):
        if ztip >= tip[im]:
            im = i
            result=im

    match result+1:
        case 1:
            return "У вас ТВОРЧЕСКИЙ тип мотивации"
        case 2:
            return "У вас ИНСТРУМЕНТАЛЬНЫЙ тип мотивации"
        case 3:
            return "У вас СОЦИАЛЬНЫЙ тип мотивации"
        case 4:
            return "У вас НЕЗАВИСИМЫЙ тип мотивации"
        case 5:
            return "Вы не МОТИВИРОВАНЫ на учёбу"

