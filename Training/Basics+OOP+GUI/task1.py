def d_r(server):
    av = 0
    drop = 0
    for num in server:
        if num != -1:
            av += num
        else:
            if av > 0:
                av -= 1
            else:
                drop += 1
    return drop

test_cases = [
    [-1, -1, -1, -1],
    [4, -1, -1, -1],
    [1, -1, 1, -1]
]

for case in test_cases:
    print(d_r(case))
