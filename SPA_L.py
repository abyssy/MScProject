from Reduction import Reduction
from queue import Queue
import copy
from ReadInstance import ReadInstance


class SPA_L:
    def __init__(self, filename):
        self.filename = filename
        r = Reduction(filename)
        # r = ReadInstance()
        # r.read_file(filename)
        self.students = r.students
        self.projects = r.projects
        self.lecturers = r.lecturers
        self.sp = r.sp
        self.plc = r.plc
        self.lp = r.lp
        self.lp_rank = r.lp_rank
        self.proj_rank = r.proj_rank
        self.l_queue = Queue()
        self.res = dict()
        for lecturer in self.lp:
            self.l_queue.put(lecturer)

        # M' in I'
        self.s_p_matching = dict()
        self.p_s_matching = dict()
        self.l_s_matching = dict()

        # M in I
        self.final_matching = dict()

        # used for check stability
        self.init_sp = copy.deepcopy(self.sp)
        self.init_plc = copy.deepcopy(self.plc)
        self.init_lp = copy.deepcopy(self.lp)
        self.init_lp_rank = copy.deepcopy(self.lp_rank)
        self.init_proj_rank = copy.deepcopy(self.proj_rank)
        self.blockingpair = False
        self.project_wstcounter = {project: [0, []] for project in self.plc}
        self.lecturer_wstcounter = {lecturer: [0, []] for lecturer in self.lp}
        self.has_a_stable_matching = False

    def spa_lecturer(self):
        # while (some lecturer lk is under-subscribed and
        global si, pj
        while not self.l_queue.empty():
            # there is some (student, project) pair (si , pj ) where si is not provisionally assigned to pj and
            # pj ∈ Pk is under-subscribed and si ∈ Ljk )
            lecturer = self.l_queue.get()
            if lecturer in self.l_s_matching.keys() and len(self.l_s_matching[lecturer]) >= self.lp[lecturer][0]:
                continue
            # is_start = False
            # for project in self.plc:
            #     if is_start:
            #         break
            #     if self.plc[project][0] != lecturer:
            #         continue
            #     else:
            #         # pj is under-subscribed
            #         if (project in self.p_s_matching.keys() and len(self.p_s_matching[project]) < self.plc[project][1]) \
            #                 or project not in self.p_s_matching.keys():
            #             for student in self.proj_rank[project]:
            #                 print(lecturer, project, student)
            #                 if student not in self.s_p_matching.keys() or self.s_p_matching[student] != project:
            #                     if student in self.s_p_matching.keys() and self.sp[student][1][self.s_p_matching[student]] < self.sp[student][1][project]:
            #                         continue
            #                     is_start = True
            #                     # si = first such student on lk ’s list;
            #                     # si = student
            #                     # pj = first such project on si ’s list;
            #                     # pj = project
            #                     break
            # if not is_start:
            #     # self.l_queue.put(lecturer)
            #     continue

            # si = first such student on lk ’s list;
            is_start = False
            for student in self.lp_rank[lecturer]:
                if is_start:
                    break
                for project in self.sp[student][1]:
                    # print(student, project, lecturer)
                    if self.plc[project][0] == lecturer:
                        if (project in self.p_s_matching.keys() and len(self.p_s_matching[project]) < self.plc[project][1]) \
                                or project not in self.p_s_matching.keys():
                            if student not in self.s_p_matching.keys() or self.s_p_matching[student] != project:
                                if student in self.s_p_matching.keys() and self.sp[student][1][self.s_p_matching[student]] < self.sp[student][1][project]:
                                    continue
                                si = student
                                pj = project
                                is_start = True
                                # print('-----', si, pj, is_start, self.l_s_matching, self.s_p_matching, self.p_s_matching)
                                break
            if not is_start:
                # self.l_queue.put(lecturer)
                continue
            student = si
            # pj = first such project on si ’s list;
            project = pj
            # print('*****', student, project, self.s_p_matching)
            # if (si is provisionally assigned to some project p)
            if student in self.s_p_matching.keys():
                # break the provisional assignment between si and p;
                p = self.s_p_matching[student]
                l = self.plc[p][0]
                self.s_p_matching.pop(student)
                self.p_s_matching[p].remove(student)
                self.l_s_matching[l].remove(student)
                self.l_queue.put(l)
                # print('*****', p, l, student)

            # provisionally assign si to pj ; /* and to lk */
            self.s_p_matching[student] = project
            if project in self.p_s_matching.keys():
                ps_list = self.p_s_matching[project]
                ps_list.append(student)
                self.p_s_matching[project] = ps_list
            else:
                ps_list = [student]
                self.p_s_matching[project] = ps_list
            if lecturer in self.l_s_matching.keys():
                ls_list = self.l_s_matching[lecturer]
                ls_list.append(student)
                self.l_s_matching[lecturer] = ls_list
            else:
                ls_list = [student]
                self.l_s_matching[lecturer] = ls_list

            # for each successor p of pj on si ’s list
            # delete(si, p);
            successor = []
            for p in self.sp[student][0]:
                if self.sp[student][1][p] > self.sp[student][1][project]:
                    successor.append(p)
            # "delete (si, p);"
            for p in successor:
                if student in self.proj_rank[p].keys():
                    self.proj_rank[p].pop(student)
                s_preference_list = self.sp[student][0]
                s_preference_list.remove(p)
                self.sp[student][0] = s_preference_list

            if len(self.l_s_matching[lecturer]) < self.lp[lecturer][0]:
                self.l_queue.put(lecturer)

    def transform_m1_to_m(self):
        for s in self.s_p_matching:
            self.final_matching[s] = self.s_p_matching[s][:2]

    def show_matching(self):
        self.check_stability()
        if self.blockingpair:
            print("No Stable Matching")
        else:
            self.has_a_stable_matching = True
            res = dict()
            for student in self.sp:
                if student in self.s_p_matching.keys():
                    project = self.s_p_matching[student]
                else:
                    project = ''
                res[student] = project
                self.res[student] = project
            print(self.res)

    def update_worst_counter(self):
        for project in self.p_s_matching:
            students = self.p_s_matching[project]
            for student in students:
                self.project_wstcounter[project][1].append(self.init_proj_rank[project][student])
        for lecturer in self.l_s_matching:
            students = self.l_s_matching[lecturer]
            for student in students:
                self.lecturer_wstcounter[lecturer][1].append(self.init_lp_rank[lecturer][student])
        for project in self.init_plc:
            if self.project_wstcounter[project][1] != []:
                self.project_wstcounter[project][0] = max(self.project_wstcounter[project][1])
            if project not in self.p_s_matching.keys():
                self.p_s_matching[project] = []
        for lecturer in self.init_lp:
            if self.lecturer_wstcounter[lecturer][1] != []:
                self.lecturer_wstcounter[lecturer][0] = max(self.lecturer_wstcounter[lecturer][1])
            if lecturer not in self.l_s_matching.keys():
                self.l_s_matching[lecturer] = []
        # for student in self.init_sp:
        #     if student not in self.s_p_matching:
        #         self.s_p_matching[student] = ''

    def blockingpair1(self, project, lecturer):
        #  project and lecturer are both under-subscribed
        if self.init_plc[project][1] > len(self.p_s_matching[project]) and self.init_lp[lecturer][0] > len(
                self.l_s_matching[lecturer]):
            # print("type 1:, ", project)
            self.blockingpair = True

    def blockingpair2(self, student, project, lecturer, m):
        #  project is under-subscribed, lecturer is full and l_k prefers s_i to its worst student in M(l_k)
        if self.init_plc[project][1] > len(self.p_s_matching[project]) and self.init_lp[lecturer][0] == len(
                self.l_s_matching[lecturer]):
            matched_project = m[student]
            # check if the student is already matched to a project offered by l_k
            if matched_project != '':
                lec = self.init_plc[matched_project][0]
                if lec == lecturer:
                    self.blockingpair = True
            # check if s_i is in a position before the worst student assigned to l_k
            student_rank_Lk = self.init_lp_rank[lecturer][student]
            if student_rank_Lk < self.lecturer_wstcounter[lecturer][0]:
                # print("type 2b:, ", student, project)
                self.blockingpair = True

    def blockingpair3(self, student, project, lecturer):
        #  project is full and lecturer prefers s_i to the worst student assigned to M(p_j)
        if self.init_plc[project][1] == len(self.p_s_matching[project]):
            student_rank_Lkj = self.init_proj_rank[project][student]
            if student_rank_Lkj < self.project_wstcounter[project][0]:
                # print("type 3:, ", student, project, self.project_wstcounter[project][0], student_rank_Lkj)
                self.blockingpair = True

    def check_stability(self):
        self.update_worst_counter()
        m = self.s_p_matching
        # print("m: ", m)
        # print(self.project_wstcounter)
        # print(self.lecturer_wstcounter)
        # print(self.sp)
        # print(self.init_sp)
        for student in m:
            # if student s_i is not assigned in M, we check if it forms a blocking pair with all the projects in A(s_i).
            if m[student] == '':
                # # list of pj's wrt to s_i
                p = self.init_sp[student][0]
            else:
                matched_project = m[student]
                # find its rank on s_i's preference list A(s_i)
                rank_matched_project = self.init_sp[student][1][matched_project]
                p_list = self.init_sp[student][0]  # list of pj's wrt to s_i      # a copy of A(s_i)
                # we check all the projects that comes before the assigned project in A(s_i)
                p = p_list[:rank_matched_project]
            # print(student, p)

            for project in p:
                lecturer = self.init_plc[project][0]  # l_k

                self.blockingpair1(project, lecturer)
                if self.blockingpair:
                    # print("1")
                    break

                self.blockingpair2(student, project, lecturer, m)
                if self.blockingpair:
                    # print("2")
                    break

                self.blockingpair3(student, project, lecturer)
                if self.blockingpair:
                    # print("3")
                    # print(rank_matched_project, p, p_list)
                    break

            if self.blockingpair:
                break

# spal = SPA_L("input.txt")
# spal = SPA_L("instances_SPASLQP/instance398.txt")
# spal.spa_lecturer()
# print("")
# print("M': Matching in SPA_L:")
# spal.show_matching()
#
# spa.transform_m1_to_m()
# spal.check_stability()
# print("Project worst student counter:")
# print(spal.project_wstcounter)
# print("******* Is blocking pair?: *******")
# print(spal.blockingpair)
# print("M: Final Matching:")
# spa.show_matching(True)
# print("")