import json 

def eq(a, b):
    return a and b

def xor(a, b):
    return a ^ b

def nor(a, b):
    return not (a or b)

def nand(a, b):
    return not (a and b)

def black_node(g1, eq1, g0):
    return not (g1 or (eq1 and g0))

def gray_node(not_g1, not_eq1, not_g0):
    return (not not_g1) or ((not not_eq1) and (not not_g0))

def pre_encode_g(a, b):
    return (not a) and b

def pre_encode_eq(a, b):
    return not xor(a, b)


def circuit_8_bit(A, B):
    pre_enc_g0 = pre_encode_g(A[0], B[0])
    pre_enc_eq0 = pre_encode_eq(A[0], B[0])

    pre_enc_g1 = pre_encode_g(A[1], B[1])
    pre_enc_eq1 = pre_encode_eq(A[1], B[1])

    pre_enc_g2 = pre_encode_g(A[2], B[2])
    pre_enc_eq2 = pre_encode_eq(A[2], B[2])

    pre_enc_g3 = pre_encode_g(A[3], B[3])
    pre_enc_eq3 = pre_encode_eq(A[3], B[3])

    pre_enc_g4 = pre_encode_g(A[4], B[4])
    pre_enc_eq4 = pre_encode_eq(A[4], B[4])

    pre_enc_g5 = pre_encode_g(A[5], B[5])
    pre_enc_eq5 = pre_encode_eq(A[5], B[5])

    pre_enc_g6 = pre_encode_g(A[6], B[6])
    pre_enc_eq6 = pre_encode_eq(A[6], B[6])

    pre_enc_g7 = pre_encode_g(A[7], B[7])
    pre_enc_eq7 = pre_encode_eq(A[7], B[7])

    black_1 = black_node(pre_enc_g1, pre_enc_eq1, pre_enc_g0)
    black_2 = black_node(pre_enc_g3, pre_enc_eq3, pre_enc_g2)
    black_3 = black_node(pre_enc_g5, pre_enc_eq5, pre_enc_g4)
    black_4 = black_node(pre_enc_g7, pre_enc_eq7, pre_enc_g6)

    eq11 = nand(pre_enc_eq0, pre_enc_eq1)
    eq12 = nand(pre_enc_eq2, pre_enc_eq3)
    eq13 = nand(pre_enc_eq4, pre_enc_eq5)
    eq14 = nand(pre_enc_eq6, pre_enc_eq7)

    gray_1 = gray_node(black_2, eq12, black_1)
    gray_2 = gray_node(black_4, eq14, black_3)

    eq21 = nor(eq11, eq12)
    eq22 = nor(eq13, eq14)

    bbig = black_node(gray_2, eq22, gray_1)
    EQ = nand(eq22, eq21)

    return (bbig, EQ)


def validate_circuit_8_bit():
    incorrect_results = []
    for a in range(256):  
        for b in range(256):  
            A = [(a >> i) & 1 for i in range(8)]
            B = [(b >> i) & 1 for i in range(8)]

            bbig, _eq = circuit_8_bit(A, B)

            expected_bbig = not (b > a)
            expected_eq = not (A == B)

            if bbig != expected_bbig or _eq != expected_eq:
                incorrect_results.append({
                    "A": A,
                    "B": B,
                    "bbig": bbig,
                    "expected_bbig": expected_bbig,
                })

    return incorrect_results


def validate_circuit():
    incorrect_results = []

    A = [(0 >> i) & 1 for i in range(8)]
    B = [(1 >> i) & 1 for i in range(8)]

    bbig, _eq = circuit_8_bit(A, B)

    expected_bbig = 1 > 0

    if bbig != expected_bbig:
        incorrect_results.append(
            {
                "A": A,
                "B": B,
                "bbig": bbig,
                "expected_bbig": expected_bbig,
            }
        )

    return incorrect_results


incorrect = validate_circuit_8_bit()

if incorrect:
    expected_correct = 256 * 256
    print(f"Found {len(incorrect)} incorrect results out of {expected_correct} in 8-bit circuit")
    with open("incorrect.txt", "w") as f:
        for line in incorrect:
            f.write(json.dumps(line) + "\n") 
else:
    print("All results are correct!")

