from data import Data
from naivebayes import NaiveBayes
from maxapost import MaxAPost
from confmat import ConfMat

#filename = "ds/weatherNominalTr.txt"
filename = "ds/titanicTr.txt"
## filename = "ds/cmcTr.txt"

d = Data(filename,75)
d.report()

pr = NaiveBayes(d)
#pr = MaxAPost(d)
pr.train()

cm = ConfMat(pr.clsscnts)
for (v,c_true) in d.test_set:
        c_pred = pr.predict(v)[0]
        #print v, c_pred, "( true class:", c_true, ")"
        cm.mat[c_pred,c_true] += 1

pr.show()
cm.report()        
