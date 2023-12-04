

def keep_digits(txt):
    """Takes a line of text and returns only the digits in it (as a string)"""
    output = ""
    for ch in txt:
        if ch.isdigit():
            output += ch
    return output


NUMBER_TEXT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def transform_number_text(txt):
    """Replaces all word-like numbers in a text string with digits"""
    #The code below didn't work.  "eightwo" should turn into "8wo" not "eigh2"
    #for key, value in NUMBER_TEXT.items():
    #    txt = txt.replace(key, str(value))
    #return txt

    # code below produces intended results:
    output = ""
    for i in range(len(txt)):
        if txt[i].isdigit():
            output += txt[i]
        else:
            for key, value in NUMBER_TEXT.items():
                if txt[i:].startswith(key):
                    output += str(value)
                    i += len(key) - 1

    return output


def do_part1(lines):
    total = 0
    for line in lines:
        line = line.strip()
        digits = keep_digits(line)
        value = int(digits[0] + digits[-1])
        print(f"{line} => {value}")
        total += value

    print(f"Total: {total}")


def do_part2(lines):
    total = 0
    for line in lines:
        line = line.strip()
        line2 = transform_number_text(line)
        digits = keep_digits(line2)
        value = int(digits[0] + digits[-1])
        print(f"{line} => {line2} => {value}")
        total += value

    print(f"Total: {total}")


#with open("data/day01/test2.txt") as fp:
with open("data/day01/input.txt") as fp:
    lines = fp.readlines()

do_part1(lines)
do_part2(lines)
