from eight_bit import *

def full_comparator(A, B):
    g0, eq0 = circuit_8_bit(A[0:8], B[0:8])
    g1, eq1 = circuit_8_bit(A[8:16], B[8:16])
    g2, eq2 = circuit_8_bit(A[16:24], B[16:24])
    g3, eq3 = circuit_8_bit(A[24:32], B[24:32])
    g4, eq4 = circuit_8_bit(A[32:40], B[32:40])
    g5, eq5 = circuit_8_bit(A[40:48], B[40:48])
    g6, eq6 = circuit_8_bit(A[48:56], B[48:56])
    g7, eq7 = circuit_8_bit(A[56:64], B[56:64])

    gray_1_1 = gray_node(g1, eq1, g0)
    gray_1_2 = gray_node(g3, eq3, g2)
    gray_1_3 = gray_node(g5, eq5, g4)
    gray_1_4 = gray_node(g7, eq7, g6)

    eq_11 = nor(eq0, eq1)
    eq_12 = nor(eq2, eq3)
    eq_13 = nor(eq4, eq5)
    eq_14 = nor(eq6, eq7)

    black_2_1 = black_node(gray_1_2, eq_12, gray_1_1)
    black_2_2 = black_node(gray_1_4, eq_14, gray_1_3)

    eq_21 = nand(eq_11, eq_12)
    eq_22 = nand(eq_13, eq_14)

    bbig = gray_node(black_2_2, eq_22, black_2_1)
    _eq = nor(eq_21, eq_22)

    return bbig, _eq


def validate_circuit_64_bit():
    incorrect_results = []

    for a in range(512):  
        for b in range(512):  
            A = [(a >> i) & 1 for i in range(64)]
            B = [(b >> i) & 1 for i in range(64)]


            bbig, _eq = full_comparator(A, B)

            expected_bbig = b > a


            if bbig != expected_bbig:
                incorrect_results.append({
                    "A": A,
                    "B": B,
                    "bbig": bbig,
                    "expected_bbig": expected_bbig,
                })

    return incorrect_results

incorrect = validate_circuit_64_bit()
if incorrect:
    expected_correct = 256 * 256
    print(f"Found {len(incorrect)} incorrect results out of {expected_correct} in 64-bit circuit")
    with open("incorrect_full.txt", "w") as f:
        for line in incorrect:
            f.write(json.dumps(line) + "\n") 

else:
    print("All results are correct!")
