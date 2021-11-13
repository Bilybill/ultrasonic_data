#%%
import numpy as np
import cv2
import os

def get_frames(filename, n_frames, use_roi = False, mask = None):
    frames = []
    v_cap = cv2.VideoCapture(filename)
    v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    assert v_len != 0
    frame_list= np.linspace(0, v_len-1, n_frames, dtype=np.int16)
    # print(frame_list,len(frame_list))
    assert v_cap.isOpened()
    
    for fn in range(v_len):
        success, frame = v_cap.read()
        if success is False:
            continue
        if (fn in frame_list):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if use_roi:
                frame = Maskframe(frame,mask)
                # x,y,width,height = use_roi
                # frame = frame[y:y+height,x:x+width]
            frames.append(frame)
    # if v_len < n_frames:     
    while(len(frames)<n_frames):
        # print(len(frames))
        frames.append(frame)
    v_cap.release()
    return frames, v_len

def Maskframe(frame,mask):
    h,w,_ = frame.shape
    use_mask = mask[str(h)+"_"+str(w)]
    masked_frame = cv2.bitwise_and(frame,frame,mask=use_mask)
    return masked_frame

def getdirfrompath(path,getfullpath=False):
    dir_path = os.listdir(path)
    res = []
    for item in dir_path:
        if os.path.isdir(os.path.join(path,item)):
            res.append(item) if not getfullpath else res.append(os.path.join(path,item))
    return res

def getfilewithtype(path,filetype,getfullpath=False):
    dir_path = os.listdir(path)
    res = []
    for item in dir_path:
        if item.lower().endswith(filetype.lower()):
            res.append(item) if not getfullpath else res.append(os.path.join(path,item))
    return res

def getfilelistwithtype(srcpath,filetype='.mp4',getfullpath=True):
    src_file_list = getfilewithtype(srcpath,filetype,getfullpath)
    subdir_list = getdirfrompath(srcpath)
    # print(subdir_list)
    if len(subdir_list) > 0:
        for subdir in subdir_list:
            src_file_list += getfilelistwithtype(os.path.join(srcpath,subdir),filetype,getfullpath)
    return src_file_list

#%%
def store_frames(frames,path2store):
    for ii,frame in enumerate(frames):
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        path2img = os.path.join(path2store, "frame"+str(ii)+".jpg")
        cv2.imwrite(path2img, frame)

def GetMaskThroughFile(filepath):
    return cv2.imread(filepath,cv2.IMREAD_UNCHANGED)

def savevideo2frame(save_root = "./"):
    # video_list = getfilelistwithtype("../data")
    mask1 = GetMaskThroughFile("mask.png")
    mask2 = GetMaskThroughFile("mask910_1260.png")
    mask = {
        "480_640":mask1,
        "910_1260":mask2
    }
    prefix = '../../data'
    topclses = getdirfrompath(prefix)
    numcount = 0
    for topcls in topclses:
        subcls = getdirfrompath(os.path.join(prefix,topcls))
        for clsvideo in subcls:
            video_file = getfilewithtype(os.path.join(prefix,topcls,clsvideo),filetype=".mp4")
            for video in video_file:
                basevideoname = video.replace(os.path.splitext(video)[-1],"")
                save_path = os.path.join(save_root,topcls,clsvideo,basevideoname)
                os.makedirs(save_path,exist_ok=True)
                frames,_ = get_frames(os.path.join(prefix,topcls,clsvideo,video),n_frames=36,use_roi=True,mask=mask)
                store_frames(frames,save_path)
                numcount += 1
    print(f'total data number : {numcount}')
savevideo2frame(save_root = '../../frame_data')


# %%
import json
def getannotation(dst="./"):
    info = []
    topcls = getdirfrompath(dst)
    for topc in topcls:
        subclses = getdirfrompath(os.path.join(dst,topc))
        for subcls in subclses:
            data_names = getdirfrompath(os.path.join(dst,topc,subcls))
            for data_name in data_names:
                data_path = os.path.join(dst,topc,subcls,data_name)
                info.append(
                    {
                        "file_path":os.path.join(topc,subcls,data_name),
                        "view":subcls,
                        "ustype":topc
                    }
                )
    return info

info = getannotation(dst = '../../frame_data')
info
# %%
info.__len__()
# %%
with open("annotation.json",'w',encoding='utf-8') as f:
    f.write(json.dumps(info,sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False)+"\n")
# %%
def getlabel(dst="./"):
    toplabel = {}
    sublabel = {}
    topcls = getdirfrompath(dst)
    xunhuan = 0
    fit_idx = 0
    first = True
    for topidx,topc in enumerate(topcls):
        subclses = getdirfrompath(os.path.join(dst,topc))
        toplabel.update({
            topc:topidx
        })
        for subidx,subcls in enumerate(subclses):
            if subcls in ['胸骨旁短轴','胸骨旁主动脉瓣短轴','胸骨旁乳头肌平面','胸骨旁二尖瓣短轴']:
                subcls = "胸骨旁短轴"
                fit_idx = subidx if first else fit_idx
                if first:
                    first = False
            else:
                fit_idx = fit_idx + 1
            sublabel.update(
                {
                    subcls:fit_idx+xunhuan
                }
            )
        xunhuan += subidx+1
    return toplabel,sublabel

toplabel,sublabel = getlabel(dst = '../../frame_data')
print(toplabel)
print(sublabel)
#%%
with open('label.txt','a+') as f:
    f.write(str(toplabel))
with open('label.txt','a+') as f:
    f.write(str(sublabel))

# %%
import json
with open("annotation.json",'r') as f:
    info_dic = json.load(f)
    info_dic
# %%
info_dic.__len__()
# %%
# video_list = getfilelistwithtype("../data")
# #%%
# video_list
# # %%
# from tqdm import tqdm
# video_info = []
# for video in tqdm(video_list):
#     v_cap = cv2.VideoCapture(video)
#     # 分辨率-宽
#     width = int(v_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     # 分辨率-高
#     height = int(v_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     v_cap.release()
#     shape = (height,width)
#     video_info.append({
#         "shape":shape,
#         "name":os.path.basename(video)
#     })
#     # if shape not in video_shape:
#         # video_shape.append(shape)

# video_info
# # %%
# from tqdm import tqdm
# video_len = []
# length = []
# for video in tqdm(video_list):
#     v_cap = cv2.VideoCapture(video)
#     v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     # 分辨率-宽
#     # width = int(v_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     # # 分辨率-高
#     # height = int(v_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     v_cap.release()
#     length.append(v_len)
#     # shape = (height,width)
#     video_len.append({
#         "len":v_len,
#         "name":os.path.basename(video)
#     })
#     # if shape not in video_shape:
#         # video_shape.append(shape)
#%%
dic1 = {'胸骨旁二尖瓣短轴': 0,'胸骨旁短轴心尖': 0,'胸骨旁主动脉瓣短轴': 0,'胸骨旁乳头肌平面': 0, '胸骨旁短轴': 0,'胸骨旁左心室长轴': 1,'心尖四腔心': 2,'剑突下四腔心': 3,'剑突下下腔静脉长轴': 4,'剑下腔静脉短轴': 5,'LP': 6, 'RL': 7, 'LU': 8, 'LL': 9, 'RD': 10, 'LD': 11, 'RU': 12, 'RB': 13, 'LB': 14,  'RP': 15,'其他': 16}
dic2 = {values:key for key,values in dic1.items()}
print(dic2)
# %%
with open("label.txt",'a+') as f:
    f.write(str(dic2))
# %%
