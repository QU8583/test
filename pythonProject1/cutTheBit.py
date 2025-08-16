#获得秒数



def save_sec(filen):
  filname = filen
  file = open(filname,'r',encoding='utf-8')
  line = file.readlines()
  for i in range(len(line)-1):
    line[i] = line[i].strip('\n')
  file.close()
  at = [] #切割好的
  z = [] #工具人
  for i in range(len(line)):
    z = line[i].split(",")
    for i in range(len(z)):
      at.append(z[i])
  #筛选出秒数,就是各个音符相互前后之间的间隔一秒为1000
  s = [int(x) for x in at if int(x)>2]
  return s


#获得位置
def save_line(filen):
  filname = filen
  file = open(filname,'r',encoding='utf-8')
  line = file.readlines()
  for i in range(len(line)-1):
    line[i] = line[i].strip('\n')
  file.close()
  at = [] #切割好的
  z = [] #工具人
  for i in range(len(line)):
    z = line[i].split(",")
    for i in range(len(z)):
      at.append(z[i])
  #筛选出位置，因为只有两栏，所以直接小于等于二即可
  sit = [int(x) for x in at if int(x)<=2]
  return sit