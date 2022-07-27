from SPA import SPA
from enumerateSMs import ESMS
from SPASLQP import SPASLQP

filename = 'instances_SPASLQP/instance518.txt'
print('SPA_SLQP: ' + filename)

# Brute Force
# E = ESMS(filename)
# E.choose(1)
# if E.has_one_feasible_matching:
#     print("Brute Force: Has a feasible matching!")
# else:
#     print("Brute Force: No feasible matching!")
# print("\n")

# SPA
spa = SPA(filename)
spa.spa_students()
print("M': Matching in SPA:")
spa.show_matching(False)
# spa.check_stability()
print("SPA blocking pair:", spa.blockingpair)

print("Student_Project:")
print(spa.init_sp)
print("Project_lecturer:")
print(spa.init_plc)
print("Lecturer_project:")
print(spa.init_lp)
print("Lecturer_project_rank:")
print(spa.init_lp_rank)
print("project_rank:")
print(spa.init_proj_rank)
print("\n")

# SPASLQP
s = SPASLQP(filename)
print("Matching in SPASLQP:")
s.show_matching()
s.algorithm_for_SPASLQ()
# print("******* Is feasible?: *******")
print("Matching in SPASLQP feasible:", s.is_feasible)
print("Matching in SPASLQP blocking pair:", s.blockingpair)
