#coding=utf-8
import math
#求解DCG
def getDCG(rels):
    dcg = rels[0]
    i = 2
    for rel in rels[1:]:
        dcg = dcg +rel/ math.log(i,2)
        i = i + 1
    return dcg
	
def getDCGa(rels):
    dcg = rels[0]
    i = 2
    for rel in rels[1:]:
        dcg = dcg + (pow(2, rel)-1) / math.log(i+1,2)
        i = i + 1
    return dcg
	
#求解IDCG
def realgetIDCG(rels):
    rels.sort()
    rels.reverse()
    return getDCG(rels)
#主函数
if __name__ == "__main__":
    scores = [5, 4, 3, 1, 2]  # 每条搜索结果的人工标注打分
    dcg = getDCG(scores)
    print "dcg =",dcg
    idcg = realgetIDCG(scores)
    print "idcg =",idcg
    print "ndcg =",dcg/idcg