from enumerateSMs import ESMS
from SPA import SPA
from SPASLQP import SPASLQP
from SPA_L import SPA_L

# SPA:
# for k in range(1, 500):
#     filename = 'instances/instance'+str(k)+'.txt'
#     print('instance'+str(k)+'.txt')
#     E = ESMS(filename)
#     E.choose(1)
#
#     spa = SPA(filename)
#     spa.spa_students()
#     print("M': Matching in SPA:")
#     spa.show_matching(False)
#     for student in E.res:
#         project_e = E.res[student]
#         project_s = spa.res[student]
#         if project_e != project_s:
#             print(student, project_e, project_s)
#             print("This matching is not same!!!")
#     print('\n')

# SPA_SLQP:
# for k in range(8001, 10001):
#     filename = 'instances_SPASLQP/instance'+str(k)+'.txt'
#     print('SPA_SLQP: instance' + str(k) + '.txt')
#     E = ESMS(filename)
#     E.choose(1)
#     if E.has_one_feasible_matching:
#         print("Brute Force: Has a feasible matching!")
#     else:
#         print("Brute Force: No feasible matching!")
#
#     s = SPASLQP(filename)
#     print('-' * 50)
#     print("Matching in SPASLQP:")
#     s.show_matching()
#     s.algorithm_for_SPASLQ()
#     # if s.is_feasible:
#     #     print("SPA_SLQP: Has a feasible matching!")
#     # else:
#     #     print("SPA_SLQP: No feasible matching!")
#     # print("******* Is feasible?: *******")
#     # print("Is feasible?:", s.is_feasible)
#
#     # check if two solution same
#     if s.is_feasible != E.has_one_feasible_matching:
#         print('*' * 50)
#         print("The solutions are not same!!!!!!!!!!!!!!!")
#     print("\n")

# SPA_L
for k in range(1, 500):
    filename = 'instances/instance'+str(k)+'.txt'
    print('instance'+str(k)+'.txt')
    E = ESMS(filename)
    E.choose(1)

    spa = SPA_L(filename)
    spa.spa_lecturer()
    print("M': Matching in SPA:")
    spa.show_matching()
    if spa.has_a_stable_matching != E.has_a_matching:
        print("The solutions are not same!!!")
    print('\n')