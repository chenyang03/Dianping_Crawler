import dianping_u_crawler_main

begin_ID = 210000
end_ID = 300000
step = 10000

def Process(N):
    try:
        dianping_u_crawler_main.getInRange(N, end_ID, step)
        S = open("./status.txt", "w")
        S.write("finished\n")
        S.close()
    except:
        file = open("./status.txt")
        num = int(file.read())
        file.close()
        Process(num + step)

Process(begin_ID)

