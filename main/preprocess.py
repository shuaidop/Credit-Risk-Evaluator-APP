import pickle
import pandas as pd
import numpy as np
def f_importances(coef, names, model):
    imp = coef
    
    imp,names = zip(*sorted(zip(imp,names)))
    imp=list(imp)
    names=list(names)
    if model=="LR" or model =="SVM":
        imp=imp[:3]+imp[-3:]
        names=names[:3]+names[-3:]
    else:
        imp=imp[-6:]
        names=names[-6:]
    dic={}
    for i in range(len(names)):
        dic[names[i]]=imp[i]
    dic=str(dic)
    print(dic)
    comment="Some important features with their coefficient: "+dic
    return comment

    
def preprocess(data, model_name):
    data=np.array(data).reshape(1,-1)
    col=['ExternalRiskEstimate', 'MSinceOldestTradeOpen',
       'MSinceMostRecentTradeOpen', 'AverageMInFile', 'NumSatisfactoryTrades',
       'NumTrades60Ever2DerogPubRec', 'NumTrades90Ever2DerogPubRec',
       'PercentTradesNeverDelq', 'MSinceMostRecentDelq',
       'MaxDelq2PublicRecLast12M', 'MaxDelqEver', 'NumTotalTrades',
       'NumTradesOpeninLast12M', 'PercentInstallTrades',
       'MSinceMostRecentInqexcl7days', 'NumInqLast6M', 'NumInqLast6Mexcl7days',
       'NetFractionRevolvingBurden', 'NetFractionInstallBurden',
       'NumRevolvingTradesWBalance', 'NumInstallTradesWBalance',
       'NumBank2NatlTradesWHighUtilization', 'PercentTradesWBalance']
    data_raw=pd.DataFrame(data, columns=col)
    data_raw2=data_raw.replace(-9, np.nan)
    data_raw2=data_raw2.replace(-8, np.nan)
    data_raw2=data_raw2.replace(-7, np.nan)
    ## store those index
    missing_entry_index=data_raw2.loc[data_raw2.NumInqLast6M.isna()==True,].index
    data_raw2=data_raw2.drop(missing_entry_index, axis=0)
    data_raw2=data_raw2.reset_index(drop=True)
    data_raw2=data_raw2.drop("MSinceMostRecentDelq", axis=1)
    data_raw=data_raw2
    
    data_raw.MaxDelq2PublicRecLast12M=data_raw.MaxDelq2PublicRecLast12M.replace(6,5)
    data_raw.MaxDelq2PublicRecLast12M=data_raw.MaxDelq2PublicRecLast12M.replace(9,8)
    MaxDelq2PublicRecLast12M_encoder = pickle.load(open("../models/cat_MaxDelq2PublicRecLast12M_encoder.sav", 'rb'))
    cat_MaxDelq2PublicRecLast12M = MaxDelq2PublicRecLast12M_encoder.transform(np.array(data_raw.MaxDelq2PublicRecLast12M).reshape(-1,1)) # fit_transform expects matrix and housing_cat_encoded is a vector; reshape transforms the vector into a matrix
    type_name=['derogatory_comment','120_days_delinquent','90_days_delinquent','60_days_delinquent',
           '30_days_delinquent', 'unknown_delinquent', 'current_never_delinquent','other']
    cat_MaxDelq2PublicRecLast12M=pd.DataFrame(cat_MaxDelq2PublicRecLast12M.toarray(), columns=type_name)
    
    MaxDelqEver_encoder=pickle.load(open("../models/cat_MaxDelqEver_encoder.sav", 'rb'))
    cat_MaxDelqEver = MaxDelqEver_encoder.transform(np.array(data_raw.MaxDelqEver).reshape(-1,1)) # fit_transform expects matrix and housing_cat_encoded is a vector; reshape transforms the vector into a matrix
    type_name2=['derogatory_comment','120_days_delinquent','90_days_delinquent','60_days_delinquent',
           '30_days_delinquent', 'unknown_delinquent', 'current_never_delinquent']
    cat_MaxDelqEver=pd.DataFrame(cat_MaxDelqEver.toarray(), columns=type_name2)
    data_raw=data_raw.drop(['MaxDelqEver','MaxDelq2PublicRecLast12M'], axis=1)
    
    imputer=pickle.load(open('../models/fill_na_imputer.sav','rb'))
    X = imputer.transform(data_raw.iloc[:,:]) # transform all numerical values in data frame (returns matrix without labels)
    data_raw_num = pd.DataFrame(X, columns=data_raw.columns) # add labels
    data_raw.iloc[:,:]=data_raw_num
    
    scaler=pickle.load(open('../models/MinMaxScaler.sav', 'rb'))
    scaled_values = scaler.transform(np.array(data_raw.iloc[0,:]).reshape(1,-1))
    data_trans=pd.DataFrame(scaled_values, columns=data_raw.columns)
    total_df=pd.concat([data_trans, cat_MaxDelq2PublicRecLast12M, cat_MaxDelqEver], axis=1, join_axes=[data_raw.index])
    
    model=pickle.load(open("../models/finalized_model.sav", 'rb'))
    output=model[model_name].predict(total_df)
    # output=str(output)
    
    ## using KNN to interpret model if KNN output is the same as the current model output
    KNN_output=model['KNN'].predict(total_df)
    
    train_set=pickle.load(open("../models/Train.sav", 'rb'))
    
    i=model_name
    features_names = list(total_df.columns)
    comment3=''
    if i=="LR" or i =="SVM":
        imp = model[i].coef_[0]
        comment3=f_importances(imp, features_names, i)
    elif i=="RF" or i=="Boosting" or i=="Tree" :
        comment3=f_importances(model[i].feature_importances_, features_names, i)
    
    
    
    out=''
    if output==1:
        out='Good'
    else:
        out='Bad'

    if KNN_output==output:
        comment1="The model "+model_name+" predicts same output as KNN model. The prediction is: "+out
        comment2=comment3
        return (comment1, comment2)
    else:
        distance, indice=model['KNN'].kneighbors(total_df)
        train_set.loc[indice[0],]
        target=train_set.RiskPerformance.loc[indice[0],]
        print(target.values)
        print(KNN_output)
        print(output)
        comment2="The distance to neighbors with risk performance is "+ str(tuple(distance[0]))+" with target value "+ str(tuple(target.values))
        comment1="Current model predicts different output as KNN model. Try different model for precision. The prediction is: "+out
        return (comment1,comment2)
        