from ReadInstance import ReadInstance


class Reduction:
    def __init__(self, filename):
        self.filename = filename
        r = ReadInstance()
        r.read_file(self.filename)

        self.students = r.students
        self.projects = r.projects
        self.lecturers = r.lecturers

        self.sp = dict()
        self.plc = dict()
        self.lp = dict()
        self.lp_rank = dict()
        self.proj_rank = dict()
        self.p_status = dict()
        # 1 : quota == 0
        # 2 : quota > 0, capacity == quota
        # 3 : quota > 0, capacity > quota
        self.l_status = dict()

        for i in range(self.projects):
            project = 'p' + str(i + 1)
            lecturer = r.plc[project][0]
            capacity = r.plc[project][1]
            quota = r.plc[project][2]
            if quota > 0:
                self.p_status[project] = 2
                self.l_status[lecturer] = 2
                self.plc[project + '2'] = [lecturer + '2', quota]
                if capacity - quota > 0:
                    self.p_status[project] = 3
                    self.plc[project + '1'] = [lecturer + '1', capacity - quota]
            else:
                self.p_status[project] = 1
                self.plc[project + '1'] = [lecturer + '1', capacity]

        for i in range(self.students):
            student = 's' + str(i + 1)
            preference_list = []
            for project in r.sp[student][0]:
                if self.p_status[project] == 1:
                    preference_list.append(project + '1')
                elif self.p_status[project] == 2:
                    preference_list.append(project + '2')
                elif self.p_status[project] == 3:
                    preference_list.append(project + '2')
                    preference_list.append(project + '1')
            length = len(preference_list)
            rank = {preference_list[i]: i for i in range(length)}
            self.sp[student] = [preference_list, rank]

        for i in range(self.lecturers):
            lecturer = 'l' + str(i + 1)
            lecturer_preference_list = []
            # print(r.lp[lecturer][1])
            if self.l_status.get(lecturer) == 2:
                capacity = 0
                old_capacity = r.lp[lecturer][0]
                for student in r.lp[lecturer][1]:
                    for project in self.sp[student][0]:
                        if self.plc[project][0][0:2] == lecturer and self.plc[project][0][2] == '2':
                            lecturer_preference_list.append(student)
                            break
                length = len(lecturer_preference_list)
                self.lp_rank[lecturer + '2'] = {lecturer_preference_list[i]: i for i in range(length)}

                for project in self.plc:
                    if self.plc[project][0][0:2] == lecturer and self.plc[project][0][2] == '2':
                        capacity += self.plc[project][1]
                self.lp[lecturer + '2'] = [capacity, self.lp_rank[lecturer + '2']]

                d = {}
                for project in self.plc:
                    if self.plc[project][0] == lecturer + '2':
                        d[project] = []
                        for student in lecturer_preference_list:
                            if project in self.sp[student][0]:
                                d[project].append(student)
                        length = len(d[project])
                        self.proj_rank[project] = {d[project][i]: i for i in range(length)}

                if old_capacity - capacity > 0:
                    lecturer_preference_list = r.lp[lecturer][1]
                    length = len(lecturer_preference_list)
                    self.lp_rank[lecturer + '1'] = {lecturer_preference_list[i]: i for i in range(length)}
                    self.lp[lecturer + '1'] = [old_capacity - capacity, self.lp_rank[lecturer + '1']]

                    d = {}
                    for project in self.plc:
                        if self.plc[project][0] == lecturer + '1':
                            d[project] = []
                            for student in lecturer_preference_list:
                                if project in self.sp[student][0]:
                                    d[project].append(student)
                            length = len(d[project])
                            self.proj_rank[project] = {d[project][i]: i for i in range(length)}
                else:
                    for project in list(self.plc.keys()):
                        if self.plc[project][0] == lecturer + '1':
                            self.plc.pop(project)
                            for student in self.sp:
                                if project in self.sp[student][0]:
                                    self.sp[student][0].remove(project)
                                    self.sp[student][1].pop(project)
            else:
                capacity = r.lp[lecturer][0]
                lecturer_preference_list = r.lp[lecturer][1]
                length = len(lecturer_preference_list)
                self.lp_rank[lecturer + '1'] = {lecturer_preference_list[i]: i for i in range(length)}
                self.lp[lecturer + '1'] = [capacity, self.lp_rank[lecturer + '1']]
                d = {}
                for project in self.plc:
                    if self.plc[project][0] == lecturer + '1':
                        d[project] = []
                        for student in lecturer_preference_list:
                            if project in self.sp[student][0]:
                                d[project].append(student)
                        length = len(d[project])
                        self.proj_rank[project] = {d[project][i]: i for i in range(length)}

        for student in self.sp:
            preference_list = self.sp[student][0]
            length = len(preference_list)
            rank = {preference_list[i]: i for i in range(length)}
            self.sp[student] = [preference_list, rank]


filename = "input.txt"
r = Reduction(filename)
print("Student_Project:")
print(r.sp)
print("Project_lecturer:")
print(r.plc)
print("Lecturer_project:")
print(r.lp)
print("Lecturer_project_rank:")
print(r.lp_rank)
print("project_rank:")
print(r.proj_rank)
