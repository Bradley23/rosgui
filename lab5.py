# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% q1 

#below are all of the listed import modules that Dr. Boldin uses.
import os
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


#%% q2 

un = [4.0, 4.1, 3.9, 3.8, 3.8]
print(un)

s1 = pd.Series(un)
print(s1)

#%% q3 

s1 = pd.Series(un)
s1.name = ('Unrate')

#there are a ton of freq aliases that I didnt know about
#m is for month
#but you can also use b (business day), w (week), q (quarter)
s1.index = pd.date_range(start = '01-1-2019',periods = 5,freq = 'm')

print(s1)

#%% q4

#there is a typo in this question of the lab. lfp has 6 values while k has 5
#i assumed there was a typo and used the last number that Dr. Boldin used
#which is 74.5

df = pd.DataFrame(s1)
k = [1,2,3,4,5]
lfp = [75,75.2,75.1,75.5,74.5]

df['Month'] = k
df['Labor Force Participation Rate'] = lfp


print(df)


#%% q5

s1.plot()

plt.savefig('s1_plot')

#%% q6

df.rename(columns = {'Unrate':'Un','Labor Force Participation Rate':"Lfp"},inplace = True)

print(df)

#%% q7

#we need to compute employment percent

emppct = (1 - df['Un']/100)*(df['Lfp']/100)
df['Emppct'] = emppct
print(df)


#%%q8
date1 = dt.date(2019,4,30)
print(df.loc[[date1],['Un','Lfp']])



#%%q9

df.describe()


#%%q10

#print(df.loc[[date1],['Un']])
df.loc[[date1],['Un']] = 100
print(df)



#%%set the value of "un" back to 3.8 --> remove the 100 replacement value
#print(df.loc[[date1],['Un']])
df.loc[[date1],['Un']] = 3.8
print(df)

#%%q1
c = ["Un","Lfp"]
date1 = dt.date(2019,2,28)
date2 = dt.date(2019,3,31)
print(df.loc[date1:date2,c])

#%%q12
#the command he shows in the lecture plots months which is basically worthless
df.plot(subplots = True, figsize = (10,20))
plt.savefig('withmonths')

#this command does not
fig,axs = plt.subplots(3,figsize = (10,20), sharex = True, sharey = False)
axs[0].plot(df["Un"])
axs[0].set(ylabel = "Unemployment Rate")
axs[1].plot(df["Lfp"])
axs[1].set(ylabel = "Laborforce Participation Rate")
axs[2].plot(df["Emppct"])
axs[2].set(ylabel = "Employment Percentage")
plt.savefig('withoutmonths')

#%%q13
print(df)

df.to_csv("lab5.csv")


#%%q14

df2 = pd.read_csv("lab5.csv", index_col=0)
#df2 = df2.iloc[:,1:]
print(df)
print(df2)

#%%q15
quit()




