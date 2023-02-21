import matplotlib.pyplot as plt


if __name__ == '__main__':
    step = float(input())
    minRiseLen = int(input())
    lsb = float(input())

    newVinLine = []
    newVoutLine = []
    newVinLines = []
    newVoutLines = []
    data_DNL_INL = []
    DNL_tab = []
    INL_tab = []
    dataY = []
    dataXFirst = []
    dataXSecond = []
    DNL = []
    INL = []
    isFirstData = []
    mistakeCheck = []
    saveRequest = []

    isTimeWord = True

    file = open("DNL_INL_end.vcsv", "rt")
    lines = file.readlines()
    file.close()

    for line in lines:
        line = line.split(',')
        counter = 0
        for word in line:
            if isTimeWord:
                isTimeWord = False
            else:
                if counter < len(line)/2:
                    if (word == '  ') | (word == '  \n') | (word == '') | (word == '\n'):
                        word = '1000000000'
                    newVinLine.append(float(word.replace('\n', '')))
                    isTimeWord = True
                else:
                    if (word == '  ') | (word == '  \n') | (word == '') | (word == '\n'):
                        word = '1000000000'
                    newVoutLine.append(float(word.replace('\n', '')))
                    isTimeWord = True

            counter += 1

        newVinLines.append(newVinLine)
        newVoutLines.append(newVoutLine)
        newVinLine = []
        newVoutLine = []

    # print(newVoutLines)
    # print(newVinLines)

    for i in range(len(newVoutLines[0])):
        INL.append(0)
        DNL.append(0)
        dataY.append(0)
        dataXFirst.append(0)
        dataXSecond.append(0)
        isFirstData.append(False)
        saveRequest.append(False)
        mistakeCheck.append(0)

    for i in range(len(newVoutLines)-1):
        for j in range (len(newVoutLines[0])):
            if (newVoutLines[i + 1][j] - newVoutLines[i][j] > step) & ~isFirstData[j]:
                dataY[j] = newVoutLines[i][j]
                dataXFirst[j] = newVinLines[i][j]
                isFirstData[j] = True
                mistakeCheck[j] = 0
            elif (newVoutLines[i + 1][j] - newVoutLines[i][j] < step) & isFirstData[j] & (mistakeCheck[j] > minRiseLen):
                DNL[j] = newVoutLines[i+1][j] - dataY[j] - lsb
                INL[j] += DNL[j]
                dataXSecond[j] = newVinLines[i+1][j]
                isFirstData[j] = False
                mistakeCheck[j] = 0
                saveRequest[j] = True
            elif (newVoutLines[i + 1][j] - newVoutLines[i][j] < step) & isFirstData[j] & (mistakeCheck[j] < minRiseLen):
                dataXFirst[j] = 0
                dataY[j] = 0
                mistakeCheck[j] = 0
                isFirstData[j] = False

            if saveRequest[j]:
                data_DNL_INL.append([j, dataXFirst[j], dataXSecond[j], DNL[j]/lsb, INL[j]/lsb])
                saveRequest[j] = False

            mistakeCheck[j] += 1

    # print(data_DNL_INL)

    for data in data_DNL_INL:
        DNL_tab.append(data[3])
        INL_tab.append(data[4])

    file = open("DNL_INL.txt", "w")
    for line in data_DNL_INL:
        file.write("index = " + str(line[0]) + " Od " + str(line[1]) + " do " + str(line[2]) + " DNL = " + str(line[3]) + " lsb " + " INL = " + str(line[4]) + " lsb " + "\n")
    file.write("min DNL: " + str(min(DNL_tab)) + " lsb " + "max DNL: " + str(max(DNL_tab)) + " lsb " + "min INL: " + str(min(INL_tab)) + " lsb " + "max INL: " + str(max(INL_tab)) + " lsb " + "\n")
    file.close()

    maxIndex = 0

    x = [[0]]
    y = [[0]]
    yy = [[0]]

    # data_DNL_INL.append([j, dataXFirst[j], dataXSecond[j], DNL[j]/lsb, INL[j]/lsb])
    for data in data_DNL_INL:
        if data[0] > maxIndex:
            while len(x) != data[0]+1:
                x.append([0])
                y.append([0])
                yy.append([0])
            maxIndex = data[0]

        x[data[0]].append(data[1])
        y[data[0]].append(y[data[0]][len(y[data[0]]) - 1])
        yy[data[0]].append(yy[data[0]][len(yy[data[0]]) - 1])
        x[data[0]].append(data[2])
        y[data[0]].append(data[3])
        yy[data[0]].append(data[4])

    for i in range(len(x)):
        x[i].append(2.5)
        y[i].append(y[i][len(y[i])-1])
        yy[i].append(yy[i][len(yy[i])-1])

    plt.plot([0, 2.5], [0, 0])

    for i in range(maxIndex+1):
        plt.plot(x[i], y[i])

    plt.xlabel("V[V]")
    plt.ylabel("DNL[lsb]")
    plt.title("DNL(V)")
    plt.show()

    plt.plot([0, 2.5], [0, 0])

    for i in range(maxIndex+1):
        plt.plot(x[i], yy[i])

    plt.xlabel("V[V]")
    plt.ylabel("INL[lsb]")
    plt.title("INL(V)")
    plt.show()

    # for i in range(len(newLines)-2):
    #     if (abs(newLines[i + 1][1] - newLines[i][1]) > step) & ~isFirstData:
    #         dataY = newLines[i][1]
    #         dataX = newLines[i][0]
    #         isFirstData = True
    #         mistakeCheck = 0
    #     elif (abs(newLines[i + 1][1] - newLines[i][1]) < step) & isFirstData & (mistakeCheck > minRiseLen):
    #         DNL = newLines[i][1] - dataY - 0.15625
    #         INL += DNL
    #         data_DNL_INL.append([dataX, newLines[i][0], DNL/0.15625, INL/0.15625])
    #         isFirstData = False
    #         mistakeCheck = 0
    #     elif (abs(newLines[i + 1][1] - newLines[i][1]) < step) & isFirstData & (mistakeCheck < minRiseLen):
    #         mistakeCheck = 0
    #         isFirstData = False
    #     mistakeCheck += 1
    #
    #
    # for data in data_DNL_INL:
    #     DNL_tab.append(data[2])
    #     INL_tab.append(data[3])
    #
    # file = open("DNL_INL.txt", "w")
    # for line in data_DNL_INL:
    #     file.writelines("Od " + str(line[0]) + " do " + str(line[1]) + " DNL = " + str(line[2]) + " lsb " + " INL = " + str(line[3]) + " lsb " + "\n")
    # file.write("min DNL: " + str(min(DNL_tab))
    #            + " lsb " + "max DNL: " + str(max(DNL_tab)) + " lsb " + "min INL: " + str(min(INL_tab)) + " lsb " + "max INL: " + str(max(INL_tab)) + " lsb " + "\n")
    # file.close()
