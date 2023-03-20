# !pip install --upgrade pip
# !pip install numpy==1.9.0
import pandas as pd
import sys
sys.path.append("/ProjectRoot/quark_max_compute/ability/host_quality/dl/authority_score")
df = pd.read_csv("data/train_final.csv")
df = df.sample(frac=1)
data = df
print(data, type(data))

#取出各个分段
df_0 = data[data.host_rank==0]
df_0_025 = data[(data.host_rank>0) & (data.host_rank<=0.25)]
df_025_05 = data[(data.host_rank>0.25) & (data.host_rank<=0.5)]
df_05_075 = data[(data.host_rank>0.5) & (data.host_rank<=0.75)]
df_075_1 = data[(data.host_rank>0.75) & (data.host_rank<=1)]
df_1_5 = data[(data.host_rank>1) & (data.host_rank<=5)]
df_5_10 = data[(data.host_rank>5) & (data.host_rank<=10)]
frames=[df_0,df_0_025,df_025_05,df_05_075,df_075_1,df_1_5,df_5_10]
# df_merged = pd.concat(frames)
# print(df_merged)
our_ratio = [len(frame)/len(df_merged) for frame in frames ]
print('======>our_ratio_before:\n',our_ratio)
print('000000:',len(df_0))

# 逼近全量分布
real_ratio=[0.6718, 0.2321, 0.421, 0.0170, 0.0102, 0.0262, 0.005]
total_num = len(df_0)/real_ratio[0]
if total_num*real_ratio[1]<len(df_0_025):
    df_0_025 = df_0_025[:round(total_num*real_ratio[1])]
if total_num*real_ratio[2]<len(df_0_025):
    df_025_05 = df_025_05[:round(total_num*real_ratio[2])]
if total_num*real_ratio[3]<len(df_0_025):
    df_05_075 = df_05_075[:round(total_num*real_ratio[3])]
if total_num*real_ratio[4]<len(df_0_025):
    df_075_1 = df_075_1[:round(total_num*real_ratio[4])]
if total_num*real_ratio[5]<len(df_0_025):
    df_1_5 = df_1_5[:round(total_num*real_ratio[5])]
if total_num*real_ratio[6]<len(df_0_025):
    df_5_10 = df_5_10[:round(total_num*real_ratio[6])]

frames=[df_0,df_0_025,df_025_05,df_05_075,df_075_1,df_1_5,df_5_10]
df_merged = pd.concat(frames)
print(df_merged)

our_ratio_after = [len(frame)/len(df_merged) for frame in frames ]
print('======>our_ratio_after:\n',our_ratio_after)
