class ReadInstance:
    def __init__(self):
        self.students = 0  # keeps track of number of students
        self.projects = 0  # keeps track of number of projects
        self.lecturers = 0  # keeps track of number of lecturers
        self.sp = dict()  # {student: [ordered_preference_list, dictionary pointing each project to its rank]}
        self.plc = dict()  # {project: [lecturer, project_capacity, project_lower_quotas]}
        self.lp = dict()  # {lecturer; [lecturer_capacity, ordered_preference_list_Lk, dictionary pointing each project to Lkj]}
        self.lp_rank = dict()  # {lecturer: a dictionary pointing each student to her rank in Lk}
        self.proj_rank = dict()  # {project: a dictionary pointing each student to her rank in Lkj}

    # reads the SPA-SLQp instance
    def read_file(self, filename):
        with open(filename) as t:
            t = t.readlines()
        entry1 = t[0].rstrip(' \n').split(' ')
        # entry1 = list(map(int, entry1)) #converts each element to an integer
        self.students, self.projects, self.lecturers = int(entry1[0]), int(entry1[1]), int(entry1[2])

        # -------------------------------------------------------------------------------------------------------------------
        #  we build the student's dictionary

        for i in range(1, self.students + 1):
            entry = t[i].rstrip(' \n').split(' ')
            student = 's' + str(entry[0])
            preferencelist = ['p' + str(k) for k in entry[1:]]
            length = len(preferencelist)
            rank = {preferencelist[i]: i for i in
                    range(length)}  # store the index of each project on each student's preference list
            self.sp[student] = [preferencelist, rank]
            # -------------------------------------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------------------------------------
        #  we build the projects's dictionary

        for i in range(self.students + 1, self.students + 1 + self.projects):
            entry = t[i].rstrip(' \n').split(' ')
            # project = [lecturer, project_capacity_yet_to_be_filled, full(project) = False, keep track of students that was rejected from project]
            # length of the preferred students for p_j according to l_k to be appended when we have more information..
            self.plc['p' + str(entry[0])] = ['l' + str(entry[3]), int(entry[1]), int(entry[2])]
            # self.plc['p' + str(entry[0])] = ['l' + str(entry[3]), int(entry[1])]
        # -------------------------------------------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------------------------------------------
        #  we build the lecturer's dictionary

        for i in range(self.students + 1 + self.projects, self.students + 1 + self.projects + self.lecturers):
            entry = t[i].rstrip(' \n').split(' ')
            lecturer = 'l' + str(entry[0])

            lecturerpreferencelist = ['s' + str(k) for k in entry[2:]]
            length = len(lecturerpreferencelist)
            self.lp_rank[lecturer] = {lecturerpreferencelist[i]: i for i in
                                      range(length)}  # stores rank of each student in L_k

            # -------------------------------------------------------------------------------------------------------------------
            #  another useful dictionary is created here and attached to the lecturer's dictionary - L_k_j
            #  the lecturer's ranked preference list according to each project they offer
            d = {}
            for project in self.plc:
                if self.plc[project][0] == lecturer:
                    d[project] = []
                    for student in lecturerpreferencelist:
                        if project in self.sp[student][0]:
                            d[project].append(student)
                    length = len(d[project])
                    self.proj_rank[project] = {d[project][i]: i for i in
                                               range(length)}  # stores rank of each student in L_k_j

            length = len(lecturerpreferencelist)
            # lecturer = [lecturer_capacity, lecturerpreferencelist, d]
            self.lp[lecturer] = [int(entry[1]), lecturerpreferencelist, d]
            # -------------------------------------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------------------------


# s = ReadInstance()
# filename = "input.txt"
# s = ReadInstance()
# filename = "instances_SPASLQP/instance398.txt"
# s.read_file(filename)
# print("Student_Project:")
# print(s.sp)
# print("Project_lecturer:")
# print(s.plc)
# print("Lecturer_project:")
# print(s.lp)
# print("Lecturer_project_rank:")
# print(s.lp_rank)
# print("project_rank:")
# print(s.proj_rank)
# print()
