from enumerateSMs import ESMS
from SPA import SPA

for k in range(1, 20):
    filename = 'instances/instance'+str(k)+'.txt'
    print('instance'+str(k)+'.txt')
    E = ESMS(filename)
    E.choose(1)

    spa = SPA(filename)
    spa.spa_students()
    print("M': Matching in SPA:")
    spa.show_matching(False)
    print('\n')
