from collections import defaultdict, Counter

valid = "><+-,.[]"


def parse(brainFuck):
    leftCounter = rightCounter = 0
    brackets = {}
    parsedInput = ''.join([char for char in brainFuck if char in valid])
    for key, char in enumerate(parsedInput):
        if char == "[":
            leftCounter += 1
            rightCounter = leftCounter
            brackets[key] = leftCounter
        elif char == "]":
            while rightCounter in [
                x
                for x, y
                in Counter(brackets.values()).items() if y > 1
            ]:
                rightCounter -= 1
            brackets[key] = rightCounter
    bracketList = defaultdict(list)
    for k, v in brackets.items():
        bracketList[v].append(k)
    bracketList = list(dict(bracketList).values())
    for subList in bracketList:
        subList.sort()
    return parsedInput, bracketList


def main(args):
    parsedInput = args[0]
    brackets = args[1]
    counter = tapeCounter = 0
    tape = [0]*30000
    output = []
    while counter < len(parsedInput):
        char = parsedInput[counter]
        if char == ">":
            tapeCounter += 1
        elif char == "<":
            tapeCounter -= 1
        elif char == "+":
            tape[tapeCounter] += 1
        elif char == "-":
            tape[tapeCounter] -= 1
        elif char == ",":
            tape[tapeCounter] = ord(input("Enter: ")[0])
        elif char == ".":
            print(chr(tape[tapeCounter]), end='')
        elif char == "[" and tape[tapeCounter] == 0:
            key = [y[0] for y in brackets].index(counter)
            counter = brackets[key][1]
            continue
        elif char == "]" and tape[tapeCounter] != 0:
            key = [y[1] for y in brackets].index(counter)
            counter = brackets[key][0]
            continue
        counter += 1


def execute(source):
    main(parse(source))
