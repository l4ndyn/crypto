import random
import sympy as sp

def generate_private_key(n=8):
    w = [0] * n

    #generate n-sized superincreasing sequence
    w[0] = random.randint(1,100)
    sum = w[0]

    for i in range(1, n):
        w[i] = random.randint(sum + 1, 2 * sum)
        sum += w[i]

    #definition
    q = random.randint(sum + 1, 2 * sum)

    while True:
        r = random.randint(2, q)
        if sp.gcd(q, r) == 1:
            break
    
    return (w, q, r)

def generate_public_key(private_key):
    (w, q, r) = private_key
    return [(wi * r) % q for wi in w]

def split(nums, chunk_size, stride = 8):
    """
    Transforms a list of bytes `nums` that are separated into `stride` sized chunks into a new list of bytes that are separated into `chunk_size` sized chunks.
    """

    #reverses the bits of num
    def reverse(num):
        rev = 0
        for i in range(stride):
            rev = (rev << 1) + num % 2
            num >>= 1

        return rev
    
    result = []
    
    curr_ind = -1 #index of currently processed number from the original list
    rem_size = 0 #remaining size of the currently processed number (in bits)

    while True:
        resx = 0

        #extract chunk_size amount of bits from the original list front to back
        for i in range(chunk_size):
            #if we've ran out of the current number, get the next
            if rem_size == 0:
                curr_ind += 1
                
                #if we've arrived at the end of the list, the conversion is done
                if curr_ind >= len(nums):
                    if i > 0:
                        result.append(resx)

                    return result

                #reverse the number so the bits can be fetched from the front first
                x = reverse(nums[curr_ind])
                rem_size = stride

            #fetch the bits back to front (of the reversed number)
            resx = (resx << 1) + x % 2
            x >>= 1

            rem_size -= 1

        result.append(resx)

def encrypt_mh(message, public_key):
    #reverse the public key to account for the bits of the message extracted backwards
    b = list(reversed(public_key))

    #regroup the bits of the message so they are in chunks corresponding to the public key
    msg = split(message, len(b))

    #calculate each character's dot product with the public key (considering the bits as components)
    return [sum([b[i] * ((m >> i) % 2) for i in range(len(b))]) for m in msg]

def ext_euc(m, n):
    """
    Finds the gcd of `m` and `n` (`g`), and the numbers `a` and `b` such that `a` * `m` + `b` * `n` = `g`.
    The value returned is `(g, a, b)`.
    """
    m2 = m // n
    n2 = m - m2 * n
    #m = m2 * n + n2

    if n2 == 0:
        return n, 0, 1
    
    m_2, n_2 = n, n2
    #n2_2  =  x * m_2 + m2_2 * n_2  =  x * m_2 + m2_2 * (1 * m - m2 * n)  =  x * m_2 + m2_2 * m - m2_2 * m2 * n  =  m2_2 * m + (-m2_2 * m2 + x) * n

    g, x, m2_2 = ext_euc(m_2, n_2)
    return g, m2_2, -m2_2 * m2 + x

def subset_sum(w, s):
    """
    Finds a subset of `w` that sums to `s`. `w` must be a superincreasing sequence.
    The return value contains the indices of the elements that make up the subset.
    """

    res = []

    #move backwards in the list and subtract each number that is smaller than the sum
    ind = len(w) - 1
    while ind >= 0:
        if w[ind] <= s:
            s -= w[ind]
            res.append(ind)
        
        #if s is 0, res contains the subset
        if s == 0:
            return res

        ind -= 1

    return []


def decrypt_mh(message, private_key):
    def bit_pos_to_num(bpos):
        """Constructs a number which has its the bits set at the positions given in `bpos`."""
        return sum([1 << (len(w) - b - 1) for b in bpos])

    (w, q, r) = private_key
    (_, ri, _) = ext_euc(r, q) #modular inverse of r

    #definition
    return [bit_pos_to_num(subset_sum(w, ri * m % q)) for m in message]