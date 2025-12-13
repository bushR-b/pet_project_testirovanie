def keyrsi(string: str) -> list:
    otveti = list(string)
    variants = [['E', 'I'], ['S', 'N'], ['T', 'F'], ['J', 'P']]
    n = []
    _firstchar = otveti[0:64:7]

    _secondchar1 = otveti[1:65:7]
    _secondchar2 = otveti[2:66:7]
    secondchar = _secondchar1 + _secondchar2

    _thirdchar1 = otveti[3:67:7]
    _thirdchar2 = otveti[4:68:7]
    thirdchar = _thirdchar1 + _thirdchar2

    _fourthchar1 = otveti[5:69:7]
    _fourthchar2 = otveti[6:70:7]
    fourthchar = _fourthchar1 + _fourthchar2

    _1variantforfirstchar = _2variantforfirstchar = 0
    _1variantforsecondchar = _2variantforsecondchar = 0
    _1variantforthirdchar = _2variantforthirdchar = 0
    _1variantforfourthchar = _2variantforfourthchar = 0

    for i in range(10):
        if _firstchar[i] == "1":
            _1variantforfirstchar += 1
        elif _firstchar[i] == "2":
            _2variantforfirstchar += 1

        if secondchar[i] == "1":
            _1variantforsecondchar += 1
        elif secondchar[i] == "2":
            _2variantforsecondchar += 1

        if thirdchar[i] == "1":
            _1variantforthirdchar += 1
        elif thirdchar[i] == "2":
            _2variantforthirdchar += 1

        if fourthchar[i] == "1":
            _1variantforfourthchar += 1
        elif fourthchar[i] == "2":
            _2variantforfourthchar += 1

    _first = max(_1variantforfirstchar, _2variantforfirstchar)
    _second = max(_1variantforsecondchar, _2variantforsecondchar)
    _third = max(_1variantforthirdchar, _2variantforthirdchar)
    _fourth = max(_1variantforfourthchar, _2variantforfourthchar)

    if _first == _1variantforfirstchar:
        n.append(variants[0][0])
    elif _first == _2variantforfirstchar:
        n.append(variants[0][1])

    if _second == _1variantforsecondchar:
        n.append(variants[1][0])
    elif _second == _2variantforsecondchar:
        n.append(variants[1][1])

    if _third == _1variantforthirdchar:
        n.append(variants[2][0])
    elif _third == _2variantforthirdchar:
        n.append(variants[2][1])

    if _fourth == _1variantforfourthchar:
        n.append(variants[3][0])
    elif _fourth == _2variantforfourthchar:
        n.append(variants[3][1])

    return "".join(n)





