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
        self.p_status = r.p_status
        self.l_status = r.l_status
        self.s_queue = Queue()
        for student in self.sp:
            self.s_queue.put(student)

        # M' in I'
        self.s_p_matching = dict()
        self.p_s_matching = dict()
        self.l_s_matching = dict()

        # M in I
        self.final_matching = dict()

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


spa = SPA("input.txt")
spa.spa_students()
print("")
print("M': Result matching:")
spa.show_matching(False)
spa.transform_m1_to_m()
spa.show_matching(True)
