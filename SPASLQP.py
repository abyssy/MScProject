from SPA import SPA
from ReadInstance import ReadInstance


class SPASLQP:
    def __init__(self, filename):
        self.filename = filename
        spa = SPA(self.filename)
        spa.spa_students()
        spa.transform_m1_to_m()
        r = ReadInstance()
        r.read_file(self.filename)

        self.sp = r.sp
        self.plc = r.plc
        self.lp = r.lp
        self.lp_rank = r.lp_rank
        self.proj_rank = r.proj_rank

        self.m = spa.final_matching
        self.blockingpair = False
        self.is_feasible = True
        self.project_wstcounter = {project: [0, []] for project in self.plc}
        self.lecturer_wstcounter = {lecturer: [0, []] for lecturer in self.lp}
        self.project_cnt = {project: 0 for project in self.plc}
        self.lecturer_cnt = {lecturer: 0 for lecturer in self.lp}

        self.spa_sp = spa.sp
        self.spa_plc = spa.plc
        self.spa_lp = spa.lp
        self.l_s_matching = spa.l_s_matching

    def update_worst_counter(self):
        for student in self.m:
            project = self.m[student]
            lecturer = self.plc[project][0]
            self.project_wstcounter[project][1].append(self.proj_rank[project][student])
            self.lecturer_wstcounter[lecturer][1].append(self.lp_rank[lecturer][student])
            self.project_cnt[project] += 1
            self.lecturer_cnt[lecturer] += 1
        for project in self.plc:
            if self.project_wstcounter[project][1]:
                self.project_wstcounter[project][0] = max(self.project_wstcounter[project][1])
        for lecturer in self.lp:
            if self.lecturer_wstcounter[lecturer][1]:
                self.lecturer_wstcounter[lecturer][0] = max(self.lecturer_wstcounter[lecturer][1])

    def blockingpair1(self, project, lecturer):
        #  project and lecturer are both under-subscribed
        if self.plc[project][1] < self.project_cnt[project] and self.lp[lecturer][0] < self.lecturer_cnt[project]:
            # print("type 1:, ", project)
            self.blockingpair = True

    def blockingpair2(self, student, project, lecturer, m):
        #  project is under-subscribed, lecturer is full and l_k prefers s_i to its worst student in M(l_k)
        if self.plc[project][1] < self.project_cnt[project] and self.lp[lecturer][0] == self.lecturer_cnt[project]:
            matched_project = m[student]
            # check if the student is already matched to a project offered by l_k
            if matched_project != '':
                lec = self.plc[matched_project][0]
                if lec == lecturer:
                    self.blockingpair = True
            # check if s_i is in a position before the worst student assigned to l_k
            student_rank_Lk = self.lp_rank[lecturer][student]
            if student_rank_Lk < self.lecturer_wstcounter[lecturer][0]:
                # print("type 2b:, ", student, project)
                self.blockingpair = True

    def blockingpair3(self, student, project, lecturer):
        #  project is full and lecturer prefers s_i to the worst student assigned to M(p_j)
        if self.plc[project][1] == self.project_cnt[project]:
            student_rank_Lkj = self.proj_rank[project][student]
            if student_rank_Lkj < self.project_wstcounter[project][0]:
                # print("type 3:, ", student, project, self.project_wstcounter[project][0])
                self.blockingpair = True

    def check_stability(self):
        self.update_worst_counter()
        m = self.m
        for student in m:
            # if student s_i is not assigned in M, we check if it forms a blocking pair with all the projects in A(s_i).
            if m[student] == '':
                # # list of pj's wrt to s_i
                p = self.sp[student][0]
            else:
                matched_project = m[student]
                # find its rank on s_i's preference list A(s_i)
                rank_matched_project = self.sp[student][1][matched_project]
                p_list = self.sp[student][0]  # list of pj's wrt to s_i      # a copy of A(s_i)
                # we check all the projects that comes before the assigned project in A(s_i)
                p = p_list[:rank_matched_project]

            for project in p:
                lecturer = self.plc[project][0]  # l_k

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

    def algorithm_for_SPASLQ(self):
        # if M is stable in I then
        if not self.blockingpair:
            for lecturer in self.spa_lp:
                if lecturer[2] == '2':
                    if self.spa_lp[lecturer][0] != len(self.l_s_matching[lecturer]):
                        self.is_feasible = False
                        break


s = SPASLQP("input.txt")
s.check_stability()
print("Matching in SPASLQP:")
print(s.m)
print("Project worst student counter:")
print(s.project_wstcounter)
print("******* Is blocking pair?: *******")
print(s.blockingpair)
print("******* Is feasible?: *******")
print(s.is_feasible)
