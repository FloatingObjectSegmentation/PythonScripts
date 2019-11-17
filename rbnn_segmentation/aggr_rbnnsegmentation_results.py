import pylab as pl

rbnnres = {
    '3': {'TN': 743230532, 'FP': 4666544, 'TP': 381186, 'FN': 62825},
    '4': {'TN': 743609245, 'FP': 4287831, 'TP': 369689, 'FN': 74322},
    '5': {'TN': 743879566, 'FP': 4017510, 'TP': 360211, 'FN': 83800},
    '6': {'TN': 743929163, 'FP': 3967913, 'TP': 351116, 'FN': 92895},
    '7': {'TN': 743939925, 'FP': 3957151, 'TP': 341496, 'FN': 102515},
    '8': {'TN': 743962278, 'FP': 3934798, 'TP': 328299, 'FN': 115712},
    '10': {'TN': 743972970, 'FP': 3924106, 'TP': 305923, 'FN': 138088}
}
spgraphres = {
    'TN': 156829362,
    'FP': 6146459,
    'TP': 114684,
    'FN': 29142
}

def computevals(cm):
    recall = cm['TP'] / (cm['TP'] + cm['FN'])
    fpr = cm['FP'] / (cm['FP'] + cm['TN'])
    precision = cm['TP'] / (cm['TP'] + cm['FP'])
    print(recall, fpr)
    return precision, recall, fpr



### COMPUTE ROC GRAPH

rbnntpr, rbnnfpr = [0.0], [0.0]
for k in rbnnres.keys():
    print('rbnn' + k)
    _, tpr, fpr = computevals(rbnnres[k])
    rbnntpr.append(tpr)
    rbnnfpr.append(fpr)
rbnnfpr.append(1.0)
rbnntpr.append(1.0)

lst = [(x,y) for x,y in zip(rbnnfpr, rbnntpr)]
lst.sort(key=lambda x: x[1])
rbnnfpr = [x[0] for x in lst]
rbnntpr = [x[1] for x in lst]

print('SPGraph')
_, tpr, fpr = computevals(spgraphres)


pl.figure(1)
pl.xlim(0, 0.04)
pl.ylim(0, 1)
pl.xlabel('FPR')
pl.ylabel('TPR')
pl.title('Comparison of RBNN and SPGraph on a ROC plot')
pl.plot(rbnnfpr, rbnntpr, 'b-', label='RBNN')
pl.plot([fpr], [tpr], 'ro', label='SPGraph')
pl.legend(loc='upper right')
pl.show()

# COMPUTE SHARES OF EACH
def normalize(dic):
    all = dic['TN'] + dic['TP'] + dic['FP'] + dic['FN']
    dic['TN'] = "{:.6f}".format(dic['TN'] / all)
    dic['TP'] = "{:.6f}".format(dic['TP'] / all)
    dic['FP'] = "{:.6f}".format(dic['FP'] / all)
    dic['FN'] = "{:.6f}".format(dic['FN'] / all)
    str = dic['TN'] + ' & ' + dic['FP'] + ' & ' + dic['FN'] + ' & ' + dic['TP']
    str += '\n\\hline'
    return str

for k in rbnnres.keys():
    print(normalize(rbnnres[k]))
print(normalize(spgraphres))
    
