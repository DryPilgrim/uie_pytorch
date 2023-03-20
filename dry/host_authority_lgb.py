g=None
class A(object):
    def __init__(self,sex):
        self.name = "zhang"
        self.sex = sex
 
 
    def get_name(self):
        return self.name + self.sex
 
 
class B(A):
    def __init__(self,sex,age):
        super(B,self).__init__(sex)
        self.age = age
        self.school='xxx'
        global g
    def p(self,tmp):
        # g=2
        print(tmp+g)
def find_min():
    """
    用代码实现如下功能：给定一个list，找出其中的一个数，使得这个数到其他所有数到距离之和最小
    """

def main():
    global g
    g=4
    b = B("男",12)
    b.p(2)

def find_inv_score():
    import pandas as pd
    df = pd.read_csv('dry/inv_auc.csv')
    df.columns=['inv_score', 'auc', 'random_state_val','random_state_test']
    inv_h = df.sort_values(by='inv_score')[len(df)-1:len(df)]
    inv_m = df.sort_values(by='inv_score')[(len(df))//2:len(df)//2+1]
    inv_l = df.sort_values(by='inv_score')[0:1]
    print(inv_h)
    print(inv_m)
    print(inv_l)

def get_site():
    import pandas as pd
    import json, os

    """
    q: 0113 0214 0913 1223
    d: 1108
    n: 1208 1010 
    """

    # 合并
    if os.path.exists('/Users/renyu/Documents/权威性标注数据/.DS_store'):
        os.remove('/Users/renyu/Documents/权威性标注数据/.DS_store')
    dirs = [os.listdir('/Users/renyu/Documents/权威性标注数据/')[5]]

    frames = []
    for i,dir in enumerate(dirs):
        df = pd.read_excel('/Users/renyu/Documents/权威性标注数据/'+dir)
        if dir in ['权威性标注-0118.xlsx']:
            frames.append(df[['Url','打分']].rename(columns={"Url": "host", "打分": "authority_score"}))
        if dir in ['权威性标注-0113.xlsx','权威性标注-0214.xlsx','权威性标注-0913.xlsx','权威性标注-1223.xlsx']:
            frames.append(df[['Url','权威性打分']].rename(columns={"Url": "host", "权威性打分": "authority_score"}))
    df_merged = pd.concat(frames).reset_index(drop=True)
    print('----->\n',df_merged[:5])

    #url->host
    for i in range(len(df_merged)):
        # print(df_merged['host'][i])
        aa=df_merged['host'][i].split('//')
        bb=aa[-1].split('/')[0]
        cc=bb.split('/')[0]
        df_merged['host'][i]=cc
    print('----->\n',df_merged[:5])
    df_merged = df_merged.dropna()

    # authority_score  去非数值数据
    df_digit = df_merged[~df_merged['authority_score'].map(lambda x:any([u'\u4e00' <= i <= u'\u9fff' for i in str(x)]))]
    print('----->\n',df_digit[:5])

    # authority_score  求平均&去重
    df_new = df_digit.groupby('host').authority_score.mean().reset_index()
    df_new = df_new.drop_duplicates('host', keep='first')

    #和训练集对比查重
    
    df_new.to_csv('/Users/renyu/Documents/test_raw_0214.csv', index=False)

def test():
    import pandas as pd

    df = pd.DataFrame({
    'brand': ['Yum Yum', 'Yum Yum', 'Indomie', 'Indomie', 'Indomie'],
    'rating': [4, 4, 3.5, 15, 5]
    })

    df_new = df.groupby('brand').rating.mean().reset_index()
    df_new = df_new.drop_duplicates('brand', keep='first')
    print(df_new)

def acc():
    import pandas as pd

    data = pd.read_excel('dry/authority_score_diff.xlsx').drop(columns=['host'])
    print(data)
    # data = data[data['label'] != '/']
    # print(data)
    label = data['label']
    name = data.columns.values
    for c in name:
        # print(data[c])
        cnt=0
        print(c)
        if c == 'label':
            continue
        for i in range(len(data)):
            if data[c][i]<=0 and data['label'][i]==0:
                pass
            elif (data['label'][i]-data[c][i]>=0.5 or data['label'][i]-data[c][i]<=-0.5):
                cnt+=1
        print('----:',cnt)

def get_site_new():
    import pandas as pd
    import json, os

    """
    2 权威站点、领域相关大站
    1 领域相关小站、多领域大站
    0 多领域小站、无法判断站点领域、领域突兀站点
    """

    # read excel
    if os.path.exists('/Users/renyu/Documents/优质评测/.DS_store'):
        os.remove('/Users/renyu/Documents/优质评测/.DS_store')
    dirs = os.listdir('/Users/renyu/Documents/优质评测/')
    # dirs = [dirs[0]]
    frames = []
    for i,dir in enumerate(dirs):
        df = pd.read_excel('/Users/renyu/Documents/优质评测/'+dir, sheet_name='数据')
        frames.append(df[['RawUrl','权威性打分']].rename(columns={"RawUrl": "host", "权威性打分": "authority_score"}))
    df_merged = pd.concat(frames).reset_index(drop=True)
    print('----->\n',df_merged[:5])

    #url->host
    for i in range(len(df_merged)):
        # print(df_merged['host'][i])
        aa=df_merged['host'][i].split('//')
        bb=aa[-1].split('/')[0]
        # cc=bb.split('/')[0]
        df_merged['host'][i]=bb
    print('----->\n',df_merged[:5])

    # dropna & delete reduntant fields
    df_no_na = df_merged.dropna()
    df_clean = df_no_na[df_no_na['authority_score'].str.contains('抛弃') == False]
    df_clean = df_clean[df_clean['authority_score'].str.contains('作者') == False]
    df_clean = df_clean[df_clean['authority_score'].str.contains('大V') == False]

    # authority_score  map to 2/1/0
    df_clean['authority_score'] = df_clean['authority_score'].apply(lambda x: 2 if x in ['权威站点','领域相关大站'] else ( 1 if x in ['领域相关小站','多领域大站'] else 0))

    # authority_score  求平均&去重
    df_new = df_clean.groupby('host').authority_score.mean().reset_index()
    df_new = df_new.drop_duplicates('host', keep='first')

    #和训练集对比查重
    
    df_new.to_csv('/Users/renyu/Documents/test_raw_0320_new.csv', index=False)

def inv_score():
    import pandas as pd

    df = pd.read_excel('dry/authority_score_diff_0320.xlsx')
    vals_label = list(zip(df['gt'],df['label']))
    vals_label.sort()
    vals_pred = list(zip(df['gt'],df['label_pre']))
    vals_pred.sort()
    cnt_lable=0
    cnt_pred=0
    cnt_lable_=0
    cnt_pred_=0
    print(vals_label[0][0])
    
    for i in range(len(vals_label)-1):
        if vals_label[i][1] < vals_label[i+1][1]:
            cnt_lable += 1
        if vals_label[i][1] > vals_label[i+1][1]:
            cnt_lable_ += 1
        if vals_pred[i][1] < vals_pred[i+1][1]:
            cnt_pred+=1
        if vals_pred[i][1] > vals_pred[i+1][1]:
            cnt_pred_+=1
    print(cnt_lable/cnt_lable_,cnt_pred/cnt_pred_)

def get_subset():
    import pandas as pd

    df_all = pd.read_csv('/Users/renyu/Documents/test_raw_0320_all_fields.csv').reset_index(drop=True)
    df_sub = pd.read_csv('/Users/renyu/Documents/test_raw_0320_new.csv').reset_index(drop=True)
    df_new=pd.DataFrame(columns=df_all.columns.values)

    # for i in range(len(df_sub)):
    #     if df_sub.loc[i,'host'] in df_all['host'].values:
    df_new = df_all[df_all['host'].isin(df_sub['host'].values)]
    df_new.to_csv('/Users/renyu/Documents/test_raw_0320_new_all_fields.csv',index=False)

# get_site()
# test()
# acc()
get_site_new()
# inv_score()
# get_subset()