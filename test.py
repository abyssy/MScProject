from SPA import SPA
from enumerateSMs import ESMS
from SPASLQP import SPASLQP

filename = 'instances_SPASLQP/instance4.txt'
print('SPA_SLQP: ' + filename)
E = ESMS(filename)
E.choose(1)

spa = SPA(filename)
spa.spa_students()
print("M': Matching in SPA:")
spa.show_matching(False)
spa.check_stability()
print(spa.blockingpair)

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

s = SPASLQP(filename)
print("Matching in SPASLQP:")
s.show_matching()
s.algorithm_for_SPASLQ()
# print("******* Is feasible?: *******")
print(s.is_feasible)
print(s.blockingpair)
