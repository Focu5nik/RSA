import random
import math


def simple_euclid(a, b):
    if a < b: a, b = b, a
    while b != 0: 
        a %= b
        a, b = b, a           
    return a


# ax+by=g
# a(x+b)+b(y-a)=g
# (a, s_1, t_1)
def extended_euclid(a, b):
    start_b = b
    swap = False
    if a < b: 
        a, b = b, a
        swap = True

    s, s_1 = 0, 1
    t, t_1 = 1, 0
    while b != 0: 
        temp_s = s_1 - int(a / b) * s
        s_1 = s
        s = temp_s
        temp_t = t_1 - int(a / b) * t
        t_1 = t
        t = temp_t
        a %= b
        a, b = b, a      

    if swap: s_1, t_1 = t_1, s_1        
    return s_1 % start_b


def fast_power_by_module(a, b, M):
    if b == 0: return 1
    t = fast_power_by_module(a, b // 2, M)
    if b % 2 == 0:
        return t * t % M
    else:
        return ((a % M) * (t * t % M )) % M


def encrypt(m, e, N):
    return fast_power_by_module(m, e, N)


def decrypt(c, d, N):
    return fast_power_by_module(c, d, N)


def miller_rabin(n):
    k = int(math.log2(n)) + 1
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)  

            if x == n - 1:
                break
        else:
            return False  

    return True 



def generate_primary(digits_number):
    p = 0
    while True:
        p = random.randint(10 ** (digits_number), 10 ** (digits_number + 1))
        if miller_rabin(p):
            break
    return p



def generate_keys():
    e = 65537
    digits_number = 5
    while True:
        p = generate_primary(digits_number)
        q = generate_primary(digits_number)
        fi_n = (p - 1) * (q - 1)     
        if simple_euclid(e, fi_n) == 1:
            break
    n = p * q   
    d = extended_euclid(e, fi_n)


    # print(p, q)

    return (e, d, n)


def toBinary(n):
    r = []
    while (n > 0):
        r.append(n % 2)
        n = n / 2
    return r
 



def main():

    keys = generate_keys()
    print(f"Keys (e, d, n): {keys}")

    # Max message length 6
    mes = 123456
    print(f"Mes: {mes}")

    encrypted_mes = encrypt(mes, keys[0], keys[2])
    print(f"Encrypted mes: {encrypted_mes}")

    decrypt_mes = decrypt(encrypted_mes, keys[1], keys[2])
    print(f"Decrypted mes: {decrypt_mes}")


if __name__ == "__main__":
    main()