def calculate_publicity(input_rank):
    score = -1.398e-07*input_rank**7 + 3.865e-07*input_rank**6 + 1.718e-05*input_rank**5 + 0.0001677*input_rank**4 - 0.0005896*input_rank**3 - 0.03269*input_rank**2 + 0.3475*input_rank**1 - 4.866e-15
    if score < 0:
        score = 0
    return score

def evaluate_authority(host_publicity, host_focus):
    if host_publicity == None:
        score_publicity = 0
    else:
        score_publicity = 1.5 * host_publicity

    if host_focus == None:
        score_focus = 0
    else:
        if host_publicity == None:
            weight = 0
        elif 1 - host_publicity > 0:
            weight = (host_publicity + 1) / 2
        else:
            weight = 1
        score_focus = weight * 3 * host_focus

    result = max(score_publicity, score_focus)
    return score_publicity, score_focus

# print(calculate_publicity(1))
# print(evaluate_authority(calculate_publicity(4),0.58))

def sql():
    import pandas as pd
    df = pd.read_excel('authority_mannual.xlsx')['host']
    values = df.values
    values_procc=[]
    # for value in values:
    #     values_procc.append('https://'+value)
    #     values_procc.append('https://'+value+'/')
    #     values_procc.append('http://'+value)
    #     values_procc.append('http://'+value+'/')
    # print(values_procc)
    for value in values:
        values_procc.append(value)
    print(values_procc)

def merge_feature():
    import pandas as pd
    import numpy as np

    df_baidurank=pd.read_csv('/Users/renyu/Desktop/dwd_sm_host_authority_feature_baidurank_tmp.csv')
    df_industry=pd.read_csv('/Users/renyu/Desktop/dwd_sm_host_authority_feature_industry_tmp.csv')
    df_official=pd.read_csv('/Users/renyu/Desktop/dwd_sm_host_authority_feature_official_tmp.csv')
    # print(df_official)

    #df_official中的url变成host形式
    df_official['host'] = df_official['url'].map(lambda x: x.split('//')[-1].split('/')[0])
    df_official = df_official.drop('url', axis=1)
    df_official=df_official[['host','certainty']]
    # print(df_official)
    df_official.to_csv('/Users/renyu/Desktop/dwd_sm_host_authority_feature_official_url2host_tmp.csv',index=False)

    #计算'max_certainty','mean_certainty','min_certainty'
    df_official_max = df_official[['host','certainty']].groupby(by='host',as_index=False).max()
    df_official_mean = df_official[['host','certainty']].groupby(by='host',as_index=False).mean()
    df_official_min = df_official[['host','certainty']].groupby(by='host',as_index=False).min()
    df_official_max_mean_certainty = pd.merge(df_official_max,df_official_mean,on='host')
    df_official_3certainty = pd.merge(df_official_max_mean_certainty,df_official_min,on='host')
    df_official_3certainty.columns=pd.Series(['host','max_certainty','mean_certainty','min_certainty'])
    df_official_3certainty.to_csv('/Users/renyu/Desktop/merge_outer_3certainty.csv',index=False)

    #根据host,合并三个df
    pd.merge(df_industry,df_baidurank,on='host').to_csv('/Users/renyu/Desktop/merge.csv',index=False)
    df_industry_baidu=pd.merge(df_industry,df_baidurank,on='host',how='outer')
    df_industry_baidu.to_csv('/Users/renyu/Desktop/merge_outer.csv',index=False)
    pd.merge(df_industry_baidu,df_official_3certainty,on='host',how='outer').to_csv('/Users/renyu/Desktop/merge_outer_3df.csv',index=False)

    #host_industry拆分出前6个行业及其置信度，即增加12列
    import json,itertools
    df_3df = pd.read_csv('/Users/renyu/Desktop/merge_outer_3df.csv')
    pre6_industry=[]
    industry_list=[ ([0]*len(df_3df)) for i in range(6)]
    industry_probability_list=[([0]*len(df_3df)) for i in range(6)]

    for i in range(len(df_3df)):
        try:
            dic=json.loads( df_3df['host_industry'][i])
            dic_sort = dict(sorted(dic.items(), key=lambda item: item[1],reverse=True))
            if len(dic_sort)>=6:
                pre6_industry.append(dict(itertools.islice(dic_sort.items(),0,6)))
                
            else:
                pre6_industry.append(dic_sort)
        except:
            pre6_industry.append('N')
            continue

        length=len(pre6_industry[i])
        dic_keys=list(dict(itertools.islice(dic_sort.items(),0,length)).keys())
        dic_values=list(dict(itertools.islice(dic_sort.items(),0,length)).values())

        for j in range(6):
            if j<length:
                # df_3df['industry_'+str(j+1)] = dic_keys[j]
                industry_list[j][i] = dic_keys[j]
                # df_3df['industry_'+str(j+1)+'_probability'] = dic_values[j]
                industry_probability_list[j][i] = dic_values[j]
            else:
                # df_3df['industry_'+str(j+1)] = 'NAN'
                # df_3df['industry_'+str(j+1)+'_probability'] = 'NAN'
                industry_list[j][i] = np.nan
                industry_probability_list[j][i]=np.nan


    # df_3df['pre6_industry']=pre6_industry
    
    for k in range(6):
        df_3df['industry_'+str(k+1)] = industry_list[k]
        df_3df['industry_'+str(k+1)+'_probability'] = industry_probability_list[k]

    # for j in range(6):
    #     try:
    #         df_3df['industry_'+str(j+1)] = df_3df['pre6_industry'].map(lambda x: list(x)[j])
    #     except:
    #         df_3df['industry_'+str(j+1)] = 'NAN'
    # for i in range(len(df_3df)):
    #     for j in range(6):
    #         try:
    #             df_3df['industry_'+str(j+1)+'_probability'] = list(df_3df['pre6_industry'][i].values())[j]
    #         except:
    #             df_3df['industry_'+str(j+1)+'_probability'] = 'NAN'
    df_3df = df_3df.drop('host_industry', axis=1)
    df_3df.to_csv("/Users/renyu/Desktop/merge_outer_3df_pre6.csv", index=False)
    
    print(df_3df['mean_certainty'][:10])
    print(df_3df['industry_4'][:10])

def get_score():
    import pandas as pd
    df_mannual=pd.read_excel('/Users/renyu/Desktop/authority_mannual.xlsx')
    df_feature=pd.read_csv('/Users/renyu/Desktop/merge_outer_3df_pre6.csv')
    
    merged = pd.merge(df_feature,df_mannual,on='host',how='outer')
    merged=merged.drop(['host_authority_score', 'diff','pre'], axis=1)
    merged.to_csv('/Users/renyu/Desktop/merge_outer_3df_pre6_score.csv',index=False)
    print(1)


# merge_feature()
get_score()