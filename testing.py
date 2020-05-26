userList = ["userA", "userB", "userC", "userD"]
userDict = {}

for i in userList:
    userDict[i] = []
userDict["control"] = 0

sample1 = ["userA", "userB", "userD"]
sample2 = ["userA", "userB"]
sample3 = ["userA", "userC", "userD"]
sample4 = ["userA", "userD"]
sample5 = ["userC"]
sample6 = ["userD", "userA"]
sample7 = ["userA", "userC"]
sample8 = ["userA", "userD", "Unknown"]



samples = [sample1, sample2, sample3, sample4, sample5, sample6, sample7, sample8]



for i in samples:

    


print(userDict)


minuteFrame = {}

for i in userList:
    minuteFrame[i] = []

for i in userList:
    value = sum(userDict[i])/userDict["control"]
    boolVal = False
    if value >= 0.3:
        boolVal = True
    minuteFrame[i] = [boolVal, value]
print(minuteFrame)
# print(userDict)