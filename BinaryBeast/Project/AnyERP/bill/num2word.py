final = ""


def word(b):
    """
    :param b: number to be converted to words
    :type b: int
    :return: number in words in Indian Format
    :rtype: string
    """

    global final
    one = ('One', 'Two', 'Three', 'Four', 'Five',
           'Six', 'Seven', 'Eight', 'Nine')
    two = ('Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty',
           'Sixty', 'Seventy', 'Eighty', 'Ninety')
    ten = ('Eleven', 'Twelve', 'Thirteeen', 'Fourteen', 'Fifteen',
           'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen')
    four = ('Hundred', 'Thousand', 'Lakh', 'Crore')
    if(b == 0):
        final += "Zero"
        # print("zero", end=" ")

    elif(len(str(b)) == 1 and b >= 0):
        final += one[b - 1] + " "
        # print(one[b - 1], end=" ")

    elif(len(str(b)) == 2 and b % 10 == 0):
        final += two[b // 10 - 1] + " "
        # print(two[b // 10 - 1], end=" ")

    elif(len(str(b)) == 2 and b < 20):
        final += ten[int(b % 10 - 1)] + " "
        # print(ten[int(b % 10 - 1)], end=" ")

    elif(len(str(b)) == 2 and b >= 20):
        b_length = len(str(b))
        msd = pow(10, b_length - 1)
        while msd > 0:
            msn = b // msd
            msn = msn * msd
            word(msn)
            b = b - msn
            msd = msd // 10

    elif(len(str(b)) == 3):
        if(b % 100 == 0):
            # print(one[b // 100 - 1], four[0], end=" ")
            final += one[b // 100 - 1] + " " + four[0] + " "
        else:
            word(b // 100)
            # print(four[0], end=" ")
            final += four[0] + " "
            word(b % 100)

    elif(len(str(b)) == 4):
        if(b % 1000 == 0):
            # print(one[b // 1000 - 1], four[1], end=" ")
            final += one[b // 1000 - 1] + " " + four[1] + " "
        else:
            word(b // 1000)
            final += four[1] + " "
            # print(four[1], end=" ")
            word(b % 1000)

    elif(len(str(b)) == 5):
        if(b % 10000 == 0):
            final += two[b // 10000 - 1] + " " + four[1] + " "
            # print(two[b // 10000 - 1], four[1], end=" ")
        else:
            word(b // 1000)
            final += four[1] + " "
            # print(four[1], end=" ")
        if(b % 1000 != 0):
            word(b % 1000)

    elif(len(str(b)) == 6):
        if(b % 100000 == 0):
            final += one[b // 100000 - 1] + " " + four[2] + " "
            # print(one[b // 100000 - 1], four[2], end=" ")
        else:
            word(b // 100000)
            final += four[2] + " "
            # print(four[2], end=" ")
            word(b % 100000)

    elif(len(str(b)) == 7):
        if(b % 1000000 == 0):
            final += two[b // 1000000 - 1] + " " + four[2] + " "
            # print(two[b // 1000000 - 1], four[2], end=" ")
        else:
            word(b // 100000)
            final += four[2] + " "
            # print(four[2], end=" ")

        if(b % 100000 != 0):
            word(b % 100000)

    elif(len(str(b)) == 8):
        if(b % 10000000 == 0):
            final += one[b // 10000000 - 1] + " " + four[3] + " "
            # print(one[b // 10000000 - 1], four[3], end=" ")
        else:
            word(b // 10000000)
            final += four[3] + " "
            # print(four[3], end=" ")
            word(b % 10000000)

    elif(len(str(b)) == 9):
        if(b % 100000000 == 0):
            final += two[b // 100000000 - 1] + " " + four[3] + " "
            # print(two[b // 100000000 - 1], four[3], end=" ")
        else:
            word(b // 10000000)
            final += four[3] + " "
            # print(four[3], end=" ")
        if(b % 10000000 != 0):
            word(b % 10000000)
    return(final + "" + "only")

def convert_to_words(b):
    global final
    final = ""
    return word(b)