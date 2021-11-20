#%%
import enum
import json
from json import encoder

# from ultrasonic.ultrasonic_diagnosis.dataset import label
with open("annotation.json",'r') as f:
    info_dic = json.load(f)

#%%
'''
generate classification data only for echocardiogram
'''
echo_info_list = [item for item in info_dic if item['ustype'] == 'Echocardiogram']
echo_view_list = [item['view'] for item in echo_info_list]
echo_view  = set(echo_view_list)
echo_view_2_label = {views:label_index for label_index,views in enumerate(echo_view)}
echo_label_2_view = {label_index:views for views,label_index in echo_view_2_label.items()}
label_list = [echo_view_2_label[item['view']] for item in echo_info_list]
import collections
label_count = collections.Counter(label_list)
numdic = {echo_label_2_view[number]:value for number,value in label_count.items()}
print(numdic)
#%%

import numpy as np
X_train = []
X_test = []
y_train = []
y_test = []

for view in echo_view:
    temp_view_list = [item for item in echo_info_list if item['view'] == view]
    print(f'{view}:{len(temp_view_list)}')
    view_num = len(temp_view_list)
    random_series = np.random.permutation(view_num)
    split = int(view_num * 1 / 10 + 0.5)
    if view_num > 5:
        split += 1
    for index in random_series[:split]:
        X_test.append(temp_view_list[index])
        y_test.append(echo_view_2_label[temp_view_list[index]['view']])
    # have_test_data.append(species) if split > 0 else None
    for index in random_series[split:]:
        X_train.append(temp_view_list[index])
        y_train.append(echo_view_2_label[temp_view_list[index]['view']])

train_count = collections.Counter(y_train)
traindic = {echo_label_2_view[number]:value for number,value in train_count.items()}
print(traindic)
test_count = collections.Counter(y_test)
testdic = {echo_label_2_view[number]:value for number,value in test_count.items()}
print(testdic)
#%%
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(echo_info_list,label_list,test_size=0.1,stratify=label_list)

# %%
info_dic.__len__()
# %%
# dic_label = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RL': 7, 'LU': 8, 'LL': 9, 'RD': 10, 'LD': 11, 'RU': 12, 'RB': 13, 'LB': 14,  'RP': 15,'其他': 16}
# label_2_view =  {0: '胸骨旁短轴', 1: '胸骨旁左心室长轴', 2: '心尖四腔心', 3: '剑突下四腔心', 4: '剑突下下腔静脉长轴', 5: '剑下腔静脉短轴', 6: 'P', 7: 'U', 8: 'D', 9: 'B', 10: 'L', 11: '其他'}
# dic_label = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RP': 6, 'LU': 7, 'RU': 7, 'LD': 8, 'RD': 8, 'LB': 9, 'RB': 9, 'LL':10, 'RL': 10,'其他': 11, '大动脉短轴':11}
view_2_label_v2 = {'RP': 0, 'LU': 1, 'LD': 2, '胸骨旁短轴心尖': 3, 'RB': 4, 'LB': 5, '胸骨旁主动脉瓣短轴': 6, '剑突下四腔心': 7, '其他': 8, '剑下腔静脉短轴': 9, '胸骨旁左心室长轴': 10, 'RL': 11, '大动脉短轴': 12, '心尖四腔心': 13, '胸骨旁乳头肌平面': 14, 'RU': 15, 'RD': 16, '剑突下下腔静脉长轴': 17, '胸骨旁二尖瓣短轴': 18, 'LP': 19, '胸骨旁短轴': 20, 'LL': 21}
label_2_view_v2 = {0: 'RP', 1: 'LU', 2: 'LD', 3: '胸骨旁短轴心尖', 4: 'RB', 5: 'LB', 6: '胸骨旁主动脉瓣短轴', 7: '剑突下四腔心', 8: '其他', 9: '剑下腔静脉短轴', 10: '胸骨旁左心室长轴', 11: 'RL', 12: '大动脉短轴', 13: '心尖四腔心', 14: '胸骨旁乳头肌平面', 15: 'RU', 16: 'RD', 17: '剑突下下腔静脉长轴', 18: '胸骨旁二尖瓣短轴', 19: 'LP', 20: '胸骨旁短轴', 21: 'LL'}
#%%
# label_dic = [dic_label[item['view']] for item in info_dic]
view_list = set([item['view'] for item in info_dic if item['view']])
print(view_list)
view_2_label = {views:label_index for label_index,views in enumerate(view_list)}
label_2_view = {label_index:views for views,label_index in view_2_label.items()}
print(view_2_label,label_2_view)
#%%
label_dic = [view_2_label[item['view']] for item in info_dic]
print(label_dic,label_dic.__len__())
# %%
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(info_dic,label_dic,test_size=0.1)
#%%
# reverse_dic = {value:key for key,value in dic_label.items()}
# print(reverse_dic)
# %%
reverse_dic = label_2_view
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
with open("echotrain_annotation.json",'w',encoding='utf-8') as f:
    f.write(json.dumps(X_train,sort_keys=False,indent=4,separators=(",",": "),ensure_ascii=False)+"\n")
with open("echotest_annotation.json",'w',encoding='utf-8') as f:
    f.write(json.dumps(X_test,sort_keys=False,indent=4,separators=(",",": "),ensure_ascii=False)+"\n")
# %%
# dic_label = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RL': 7, 'LU': 8, 'LL': 9, 'RD': 10, 'LD': 11, 'RU': 12, 'RB': 13, 'LB': 14,  'RP': 15,'其他': 16}
# reverse_dic = {value:key for key,value in dic_label.items()}
import json
import collections
with open("echotrain_annotation.json",'r') as f:
    train_dic = json.load(f)
with open("echotest_annotation.json",'r') as f:
    test_dic = json.load(f)

train_label = [echo_view_2_label[train_itm['view']] for train_itm in train_dic]
test_label = [echo_view_2_label[test_itm['view']] for test_itm in test_dic]

train_count = collections.Counter(train_label)
traindic = {echo_label_2_view[number]:value for number,value in train_count.items()}
print(traindic)
test_count = collections.Counter(test_label)
testdic = {echo_label_2_view[number]:value for number,value in test_count.items()}
print(testdic)
# %%
