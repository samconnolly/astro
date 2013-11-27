import numpy as np
john = ['3', '1', 15,6]
jane = ['4', '2', 10,7]
dave = ['5', '3', 12,8]
students = np.vstack((john,jane,dave))
#answer = sorted(students, key=lambda student: student[2])   # sort by age
print students#, answer
