def find_dictionary(original_string, idx):
    if original_string[idx:idx + 1] in dictionary:
        for word in dictionary[original_string[idx:idx + 1]]:
            next_index = idx + len(word)
            if original_string[idx:next_index] == word:
                return next_index

    return idx + 1


if __name__ == '__main__':
    dictionary = {
        "c": ["c=", "c-"],
        "d": ["dz=", "d-"],
        "l": ["lj"],
        "n": ["nj"],
        "s": ["s="],
        "z": ["z="]
    }

    inputString = input()
    answer = 0
    i = 0
    while i < len(inputString):
        i = find_dictionary(inputString, i)
        answer += 1

    print(answer)
