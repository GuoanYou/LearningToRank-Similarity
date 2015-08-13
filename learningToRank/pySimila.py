#coding=utf-8
import re
import math
from itertools import combinations
#保存结果到文件
def save(filename, contents):
	fh = open(filename, 'a')
	fh.write(contents+'\n')
	fh.write('\n')
	fh.close()

#获取真实值与预测值rank
def get_data(file_name=None):
	file_object = open(file_name,'r')
	lis=[]
	for line in file_object:
		s1 = re.sub('[^a-zA-Z0-9,.]',"",line)
		s2 = s1.split(",")
		#print s2[0]
		lis.append(int(s2[0]))
	return lis

#common求交集，来求覆盖率
def common(list1,list2):
	tmp =  [val for val in list1 if val in list2]
	return tmp

#kendall版本1，貌似是错的。
def cal_kendall_tau(list_1 , list_2):  
    length = len(list_1)  
    if length != len(list_2):  
        return -1  
    set_1 = set()  
    set_2 = set()  
    for i in range(length):  
        for j in range(i+1,length):  
            set_1.add( (list_1[i],list_1[j]) )  
            set_2.add( (list_2[i],list_2[j]) )  
    count = len(set_1 & set_2)  
    return float(count)*2 / ((length-1)*length)  

#pearson版本1
def pearson(x,y):
	n=len(x)
	vals=range(n)
# Simple sums
	sumx=sum([float(x[i]) for i in vals])
	sumy=sum([float(y[i]) for i in vals])
# Sum up the squares
	sumxSq=sum([x[i]**2.0 for i in vals])
	sumySq=sum([y[i]**2.0 for i in vals])
# Sum up the products
	pSum=sum([x[i]*y[i] for i in vals])
# Calculate Pearson score
	num=pSum-(sumx*sumy/n)
	den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
	if den==0: 
		return 0
	r=num/den
	return r

#Spearman algorithm 版本1
def spearman(x, y):
    assert len(x) == len(y) > 0
    q = lambda n: map(lambda val: sorted(n).index(val) + 1, n)
    d = sum(map(lambda x, y: (x - y) ** 2, q(x), q(y)))
    return 1.0 - 6.0 * d / float(len(x) * (len(y) ** 2 - 1.0))

fgx="---------------------------------------------"

#--------------------分割线，下面其他版本代码乱入-----------------------------"

#Pearson algorithm版本2.和版本1输出的结果一样。
def pearson(x, y):
    assert len(x) == len(y) > 0
    q = lambda n: len(n) * sum(map(lambda i: i ** 2, n)) - (sum(n) ** 2)
    return (len(x) * sum(map(lambda a: a[0] * a[1], zip(x, y))) - sum(x) * sum(y)) / math.sqrt(q(x) * q(y))

#Kendall algorithm版本2
def kendall(x, y):
    assert len(x) == len(y) > 0
    c = 0 #concordant count
    d = 0 #discordant count
    t = 0 #tied count
    for (i, j) in combinations(xrange(len(x)), 2):
        s = (x[i] - x[j]) * (y[i] - y[j])
        if s:
            c += 1
            d += 1
            if s > 0:
                t += 1
            elif s < 0:
                t -= 1
        else:
            if x[i] - x[j]:
                c += 1
            elif y[i] - y[j]:
                d += 1
    return t / math.sqrt(c * d)

#tau版本3，和版本2求得结果一样。
def tau(values1, values2, get_pairs=False):
	""" Computes Kendall's tau rank correlation coefficient for two	lists of observations with no ties
		
		Parameters:
			values1:	list of observations
			values2:	list of observations
			get_pairs:	set True to return the number of concordant and discordant pairs instead of tau
	"""
	concordant_pairs = 0
	discordant_pairs = 0
	zipped_vals = list(zip(values1, values2))
	for i, o1 in enumerate(zipped_vals):
		for o2 in zipped_vals[i+1:]:
			if pair_is_concordant(o1, o2):
				concordant_pairs += 1
			if pair_is_disconcordant(o1, o2):
				discordant_pairs += 1
	
	n = len(zipped_vals)
	tau = float(concordant_pairs - discordant_pairs) / (0.5 * n * (n - 1))
	if get_pairs:
		return (concordant_pairs, discordant_pairs)
	else:
		return tau
def pair_is_concordant(o1, o2):
	return (o1[0] > o2[0] and o1[1] > o2[1]) or (o1[0] < o2[0] and o1[1] < o2[1])

def pair_is_disconcordant(o1, o2):
	return (o1[0] > o2[0] and o1[1] < o2[1]) or (o1[0] < o2[0] and o1[1] > o2[1])

#读取数据
list1= get_data("savetest_y.txt")
list2= get_data("savetest_hy.txt")

#打印Top5，10，15数据
print list1[0:5]
print list2[0:5]
print list1[0:10]
print list2[0:10]
print list1[0:15]
print list2[0:15]

#求解覆盖率
tmp5  =  common(list1[0:5],list2[0:5])
tmp10 =  common(list1[0:10],list2[0:10])
tmp15 =  common(list1[0:15],list2[0:15])
c5=len(tmp5)/5.0
c10=len(tmp10)/10.0
c15=len(tmp15)/15.0


#保存覆盖率
c5 = 'Coverage of Top5   : %s' % c5
c10= 'Coverage of Top10  : %s' % c10
c15= 'Coverage of Top15  : %s' % c15
save("Similarity.txt",c5)
save("Similarity.txt",c10)
save("Similarity.txt",c15)

save("Similarity.txt",fgx)
#保存Kendall
tau5= "Kendall's tau 5 = %s" % tau(list1[0:5],list2[0:5])
tau10= "Kendall's tau 10 = %s" % tau(list1[0:10],list2[0:10])
tau15= "Kendall's tau 15 = %s" %tau(list1[0:15],list2[0:15])
save("Similarity.txt",tau5)
save("Similarity.txt",tau10)
save("Similarity.txt",tau15)

save("Similarity.txt",fgx)
#保存Pearson
p5="pearson 5 :  %s "   % pearson(list1[0:5],list2[0:5])
p10="pearson 10 : %s "   %pearson(list1[0:10],list2[0:10])
p15="pearson 15 : %s "   %pearson(list1[0:15],list2[0:15])
save("Similarity.txt",p5)
save("Similarity.txt",p10)
save("Similarity.txt",p15)

save("Similarity.txt",fgx)
#保存Spearman
s5= "spearman 5 : %s" %spearman(list1[0:5],list2[0:5])
s10= "spearman 10 : %s" %spearman(list1[0:10],list2[0:10])
s15= "spearman 15 : %s" %spearman(list1[0:15],list2[0:15])
save("Similarity.txt",s5)
save("Similarity.txt",s10)
save("Similarity.txt",s15)