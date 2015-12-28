import dianping_u_crawler_main

begin_ID = 56644299
end_ID = 60000000
step = 7000

def Process(N):
    try:
        dianping_u_crawler_main.getInRange(N, end_ID, step)
        S = open("../status.txt", "w")
        S.write("finished\n")
        S.close()
    except:
        file = open("../status.txt")
        num = int(file.read())
        file.close()
        Process(num + 14000)

Process(begin_ID)

