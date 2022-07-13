from Reduction import Reduction
from queue import Queue


class SPA:
    def __init__(self, filename):
        self.filename = filename
        r = Reduction(filename)
        self.students = r.students
        self.projects = r.projects
        self.lecturers = r.lecturers
        self.sp = r.sp
        self.plc = r.plc
        self.lp = r.lp
        self.lp_rank = r.lp_rank
        self.proj_rank = r.proj_rank
        self.s_queue = Queue()
        for student in self.sp:
            self.s_queue.put(student)

        # M' in I'
        self.s_p_matching = dict()
        self.p_s_matching = dict()
        self.l_s_matching = dict()

        # M in I
        self.final_matching = dict()

        # used for check stability
        self.init_sp = self.sp
        self.init_plc = self.plc
        self.init_lp = self.lp
        self.init_lp_rank = self.lp_rank
        self.init_proj_rank = self.proj_rank
        self.blockingpair = False
        self.project_wstcounter = {project: [0, []] for project in self.plc}
        self.lecturer_wstcounter = {lecturer: [0, []] for lecturer in self.lp}

    def spa_students(self):
        # while (some student si is free and si has a non-empty list) {
        while not self.s_queue.empty():
            student = self.s_queue.get()
            if not len(self.sp[student][0]):
                continue
            # pj = first project on si ’s list;
            project = self.sp[student][0][0]
            # lk = lecturer who offers pj ;
            lecturer = self.plc[project][0]

            # provisionally assign si to pj ;
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

            # if (pj is over-subscribed) {
            if len(self.p_s_matching[project]) > self.plc[project][1]:
                last_rank = -1
                # sr = worst student assigned to pj ;
                worst_s = ''
                for s in self.p_s_matching[project]:
                    if last_rank == -1:
                        last_rank = self.proj_rank[project][s]
                        worst_s = s
                        continue
                    if self.proj_rank[project][s] > last_rank:
                        worst_s = s
                        last_rank = self.proj_rank[project][s]
                # break provisional assignment between sr and pj ;
                self.s_p_matching.pop(worst_s)
                self.p_s_matching[project].remove(worst_s)
                self.l_s_matching[lecturer].remove(worst_s)
                self.s_queue.put(worst_s)
            # else if (lk is over-subscribed) {
            elif len(self.l_s_matching[lecturer]) > self.lp[lecturer][0]:
                last_rank = -1
                # sr = worst student assigned to lk ;
                worst_s = ''
                for s in self.l_s_matching[lecturer]:
                    if last_rank == -1:
                        last_rank = self.lp_rank[lecturer][s]
                        worst_s = s
                        continue
                    if self.lp_rank[lecturer][s] > last_rank:
                        worst_s = s
                        last_rank = self.lp_rank[lecturer][s]
                # pt = project assigned sr ;
                pt = self.s_p_matching[worst_s]
                # break provisional assignment between sr and pt ;
                self.s_p_matching.pop(worst_s)
                self.p_s_matching[pt].remove(worst_s)
                self.l_s_matching[lecturer].remove(worst_s)
                self.s_queue.put(worst_s)

            # if (pj is full) {
            if len(self.p_s_matching[project]) == self.plc[project][1]:
                # sr = worst student assigned to pj ;
                last_rank = -1
                for s in self.p_s_matching[project]:
                    if last_rank == -1:
                        last_rank = self.proj_rank[project][s]
                        continue
                    if self.proj_rank[project][s] > last_rank:
                        last_rank = self.proj_rank[project][s]
                # for (each successor st of sr on Ljk )
                #       delete (st , pj );
                successor = []
                for st in self.proj_rank[project]:
                    if self.proj_rank[project][st] > last_rank:
                        successor.append(st)
                # "delete (st, pj);"
                for st in successor:
                    if st in self.proj_rank[project].keys():
                        self.proj_rank[project].pop(st)
                    s_preference_list = self.sp[st][0]
                    s_preference_list.remove(project)
                    self.sp[st][0] = s_preference_list
            # if (lk is full) {
            if len(self.l_s_matching[lecturer]) == self.lp[lecturer][0]:
                # sr = worst student assigned to lk ;
                last_rank = -1
                for s in self.l_s_matching[lecturer]:
                    if last_rank == -1:
                        last_rank = self.lp_rank[lecturer][s]
                        continue
                    if self.lp_rank[lecturer][s] > last_rank:
                        last_rank = self.lp_rank[lecturer][s]
                # for (each successor st of sr on Lk )
                #       for (each project pu ∈ Pk ∩ At )
                #               delete (st , pu );
                for st in self.lp_rank[lecturer]:
                    if self.lp_rank[lecturer][st] > last_rank:
                        for pu in self.sp[st][0]:
                            # "delete (st, pu)"
                            if self.plc[pu][0] == lecturer:
                                if st in self.proj_rank[pu].keys():
                                    self.proj_rank[pu].pop(st)
                                s_preference_list = self.sp[st][0]
                                s_preference_list.remove(pu)
                                self.sp[st][0] = s_preference_list

    def show_matching(self, is_final_matching):
        if is_final_matching:
            print(self.final_matching)
        else:
            print(self.s_p_matching)

    def transform_m1_to_m(self):
        for s in self.s_p_matching:
            self.final_matching[s] = self.s_p_matching[s][:2]

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
        for lecturer in self.init_lp:
            if self.lecturer_wstcounter[lecturer][1] != []:
                self.lecturer_wstcounter[lecturer][0] = max(self.lecturer_wstcounter[lecturer][1])

    def blockingpair1(self, project, lecturer):
        #  project and lecturer are both under-subscribed
        if self.init_plc[project][1] > len(self.p_s_matching[project]) and self.init_lp[lecturer][0] > len(
                self.l_s_matching[project]):
            # print("type 1:, ", project)
            self.blockingpair = True

    def blockingpair2(self, student, project, lecturer, m):
        #  project is under-subscribed, lecturer is full and l_k prefers s_i to its worst student in M(l_k)
        if self.init_plc[project][1] > len(self.p_s_matching[project]) and self.init_lp[lecturer][0] == len(
                self.l_s_matching[project]):
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
                # print("type 3:, ", student, project, self.project_wstcounter[project][0])
                self.blockingpair = True

    def check_stability(self):
        self.update_worst_counter()
        m = self.s_p_matching
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

            for project in p:
                lecturer = self.init_plc[project][0]  # l_k

                self.blockingpair1(project, lecturer)
                if self.blockingpair:
                    print("1")
                    break

                self.blockingpair2(student, project, lecturer, m)
                if self.blockingpair:
                    print("2")
                    break

                self.blockingpair3(student, project, lecturer)
                if self.blockingpair:
                    print("3")
                    break

            if self.blockingpair:
                break


spa = SPA("input.txt")
spa.spa_students()
print("")
print("M': Matching in SPA:")
spa.show_matching(False)

spa.transform_m1_to_m()
spa.check_stability()
print("Project worst student counter:")
print(spa.project_wstcounter)
print("******* Is blocking pair?: *******")
print(spa.blockingpair)
# print("M: Final Matching:")
# spa.show_matching(True)
print("")
