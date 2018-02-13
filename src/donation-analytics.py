import pandas as pd
import os
import sys
itcontFile = sys.argv[1]
percentileFile = sys.argv[2]
repeatdonorsFile = sys.argv[3]
# Neeed columns for the analysis
Needed = [0, 7, 10, 13, 14, 15]
NeededListArray = []
df = pd.DataFrame()
repeat_df = pd.DataFrame()
outputFile = open(repeatdonorsFile,'w')
percentileFile = open(percentileFile ,'r')
percentile = float(percentileFile.read())/100.0
with  open(itcontFile,'r') as inputFile:
    for line in inputFile: 
        Line = line.split('|')
        CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = [Line[i] for i in Needed]   
        if not OTHER_ID and NAME and len(ZIP_CODE) > 5 and TRANSACTION_DT and TRANSACTION_AMT:
            ZIP_CODE = ZIP_CODE[0:5]
            TRANSACTION_DT = TRANSACTION_DT[-4:]
            data = pd.DataFrame([[CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, int(TRANSACTION_AMT)]],
                      columns=['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT'])
            df = df.append(data)
            id = ( (df['NAME'].astype(str).str.contains(NAME))  &  
                (df['ZIP_CODE'].astype(str).str.contains(ZIP_CODE)))
               
            if(sum(id)>1):
                repeat_df = repeat_df.append(data)
                repeat_df_now = pd.DataFrame()
                id =  ( repeat_df['CMTE_ID'].astype(str).str.contains(CMTE_ID) &
                        repeat_df['ZIP_CODE'].astype(str).str.contains(ZIP_CODE) &
                        repeat_df['TRANSACTION_DT'].astype(str).str.contains(TRANSACTION_DT) )              
                repeat_df_now = repeat_df.loc[id]
                donationPercentile  = repeat_df['TRANSACTION_AMT'].quantile(percentile,interpolation='nearest')  
                cumulativeAmount = repeat_df['TRANSACTION_AMT'].sum()
                transactionCount  = repeat_df['TRANSACTION_AMT'].count()
                outputFile.write('%s|%s|%s|%s|%s|%s\n' % (CMTE_ID, ZIP_CODE, TRANSACTION_DT,  
                                                donationPercentile, cumulativeAmount, transactionCount))
outputFile.close()                 
inputFile.close()
percentileFile.close()
