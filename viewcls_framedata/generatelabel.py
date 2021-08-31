#%%
import json
from json import encoder
with open("annotation.json",'r') as f:
    info_dic = json.load(f)
# %%
info_dic.__len__()
# %%
dic_label = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RL': 7, 'LU': 8, 'LL': 9, 'RD': 10, 'LD': 11, 'RU': 12, 'RB': 13, 'LB': 14,  'RP': 15,'其他': 16}
# %%
info_dic
#%%
label_dic = [dic_label[item['view']] for item in info_dic]
print(label_dic,label_dic.__len__())
# %%
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(info_dic,label_dic,test_size=0.1,stratify=label_dic)
#%%
reverse_dic = {value:key for key,value in dic_label.items()}
print(reverse_dic)
# %%
import collections
train_count = collections.Counter(y_train)
dic = {reverse_dic[number]:value for number,value in train_count.items()}
print(dic)
test_count = collections.Counter(y_test)
testdic = {reverse_dic[number]:value for number,value in test_count.items()}
print(testdic)
label_count = collections.Counter(label_dic)
labeldic = {reverse_dic[number]:value for number,value in label_count.items()}
print(labeldic)
# %%
print(dic.__len__(),len(testdic),len(labeldic))
# %%
labeldic.keys()-testdic.keys()
# %%
import json
import collections
with open("train_annotation.json",'a+',encoding='utf-8') as f:
    f.write(json.dumps(X_train,sort_keys=False,indent=4,separators=(",",": "),ensure_ascii=False)+"\n")
with open("test_annotation.json",'a+',encoding='utf-8') as f:
    f.write(json.dumps(X_test,sort_keys=False,indent=4,separators=(",",": "),ensure_ascii=False)+"\n")
# %%
dic_label = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RL': 7, 'LU': 8, 'LL': 9, 'RD': 10, 'LD': 11, 'RU': 12, 'RB': 13, 'LB': 14,  'RP': 15,'其他': 16}
reverse_dic = {value:key for key,value in dic_label.items()}
import json
import collections
with open("train_annotation.json",'r') as f:
    train_dic = json.load(f)
with open("test_annotation.json",'r') as f:
    test_dic = json.load(f)

train_label = [dic_label[train_itm['view']] for train_itm in train_dic]
test_label = [dic_label[test_itm['view']] for test_itm in test_dic]

train_count = collections.Counter(train_label)
traindic = {reverse_dic[number]:value for number,value in train_count.items()}
print(traindic)
test_count = collections.Counter(test_label)
testdic = {reverse_dic[number]:value for number,value in test_count.items()}
print(testdic)
# %%
