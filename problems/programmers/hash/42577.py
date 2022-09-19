from sys import stdin
new_input = stdin.readline


def solution(phone_book):
    phone_book.sort(key=lambda x: len(x))

    prefix_list_dict = dict()

    for phone in phone_book:
        candidatePrefixList = prefix_list_dict.get(phone[0], list())

        for candidatePrefix in candidatePrefixList:
            if phone.find(candidatePrefix) == 0:
                return True

        candidatePrefixList.append(phone)

    return False


if __name__ == '__main__':
    print(solution(["119", "97674223", "1195524421"]))
    print(solution(["123","456","789"]))
    print(solution(["12","123","1235","567","88"]))
