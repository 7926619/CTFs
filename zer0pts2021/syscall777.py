from z3 import *
import binascii

args = [BitVec(f"args[{i}]", 32) for i in range(0, 14)]

s = Solver()

s.add(args[0] == 0x3072657a)
s.add(args[1] == 0x7b737470)

for j in range(14):
    M = [BitVec(f"M[{j}][{i}]", 32) for i in range(0, 14)]
    s.add(M[0] == args[j % 14])
    s.add(M[1] == M[0] ^ args[(j+1) % 14])
    s.add(M[2] == M[1] ^ args[(j+2) % 14])
    s.add(M[3] == M[2] ^ args[(j+3) % 14])
    s.add(M[4] == M[0] + M[1] + M[2] + M[3])
    s.add(M[5] == M[0] - M[1] + M[2] - M[3])
    s.add(M[6] == M[0] + M[1] - M[2] - M[3])
    s.add(M[7] == M[0] - M[1] - M[2] + M[3])
    s.add(M[8] == ((M[4] | M[5]) ^ (M[6] & M[7])) & 0xffffffff)
    s.add(M[9] == ((M[5] | M[6]) ^ (M[7] & M[4])) & 0xffffffff)
    s.add(M[10] == ((M[6] | M[7]) ^ (M[4] & M[5])) & 0xffffffff)
    s.add(M[11] == ((M[7] | M[4]) ^ (M[5] & M[6])) & 0xffffffff)

    s.add(Or(
        And(M[8] == 4127179254, M[9] == 4126139894, M[10] == 665780030, M[11] == 666819390),
        And(M[8] == 1933881070, M[9] == 2002783966, M[10] == 1601724370, M[11] == 1532821474),
        And(M[8] == 4255576062, M[9] == 3116543486, M[10] == 3151668710, M[11] == 4290701286),
        And(M[8] == 1670347938, M[9] == 4056898606, M[10] == 2583645294, M[11] == 197094626),
        And(M[8] == 2720551936, M[9] == 1627051272, M[10] == 1627379644, M[11] == 2720880308),
        And(M[8] == 2307981054, M[9] == 3415533530, M[10] == 3281895882, M[11] == 2174343406),
        And(M[8] == 2673307092, M[9] == 251771212, M[10] == 251771212, M[11] == 2673307092),
        And(M[8] == 4139379682, M[9] == 3602496994, M[10] == 3606265306, M[11] == 4143147994),
        And(M[8] == 4192373742, M[9] == 4088827598, M[10] == 3015552726, M[11] == 3119098870),
        And(M[8] == 530288564, M[9] == 530288564, M[10] == 3917315412, M[11] == 3917315412),
        And(M[8] == 4025255646, M[9] == 2813168974, M[10] == 614968622, M[11] == 1827055294),
        And(M[8] == 3747612986, M[9] == 1340672294, M[10] == 1301225350, M[11] == 3708166042),
        And(M[8] == 3098492862, M[9] == 3064954302, M[10] == 3086875838, M[11] == 3120414398),
        And(M[8] == 2130820044, M[9] == 2115580844, M[10] == 2130523044, M[11] == 2145762244)
    ))

for i in range(0, len(args)):
  s.add(((args[i]) & 0xff) <= 126)
  s.add(((args[i] >> 8) & 0xff) <= 126)
  s.add(((args[i] >> 16) & 0xff) <= 126)
  s.add(((args[i] >> 24) & 0xff) <= 126)

if s.check() == sat:
    m = s.model()
    flag = ""
    for i in range(14):
        st = '%08x' % (m[args[i]].as_long())
        st = "".join(map(str.__add__, st[-2::-2] ,st[-1::-2]))
        flag += str(binascii.unhexlify(st.encode()), 'ascii')
    print(flag)
