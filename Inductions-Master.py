import pandas as pd
from pyfiglet import Figlet
from dateutil.relativedelta import relativedelta
import time
import datetime as dt

f = Figlet(font='doom')
print(f.renderText('Inductions Data'))

df = pd.read_excel('//ntserver5/generalDB/WorkforceDB/Inductions/New Master July 2019.xlsx', sheet_name="Master")

month = input('What month are you focusing on? <format = MM/YYYY>')
month_start = pd.to_datetime(month)
month_end = month_start + relativedelta(months=1)
print(month_start)
print(month_end)

print(df['Induction End Date'].head(15))
print(len(df))
df = df[(df['Induction End Date'] >= month_start) & (df['Induction End Date'] < month_end)]
print(len(df))
print(df['COMPLETED WITHIN TIMEFRAME'].value_counts(dropna=False))
df['COMPLETED WITHIN TIMEFRAME'] = df['COMPLETED WITHIN TIMEFRAME'].str.upper()
df['COMPLETED WITHIN TIMEFRAME'] = df['COMPLETED WITHIN TIMEFRAME'].fillna('Z')
piv = pd.pivot_table(df, values='Number', index=['Area','Sector/Division','HCSW'], columns='COMPLETED WITHIN TIMEFRAME',
                     aggfunc = lambda x:len(x.unique()))
totals = piv.sum().values
df1 = piv.groupby(level=[0,1]).sum()
df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                      df1.index.get_level_values(1)+' Total',
                                      len(df1.index) * ['']])
print(df1)
df2 = piv.groupby(level=0).sum()
df2.index = pd.MultiIndex.from_arrays([df2.index.values + ' Total',
                                       len(df2.index) * [''],
                                       len(df2.index) * ['']])
print(df2)
piv = pd.concat([piv, df1, df2]).sort_index(level=[0])
print(piv)

piv.loc[('GGC Total', '', '')] = totals
print(piv)

#piv.index=['Not Completed on Time', 'Completed on time', 'Induction Outstanding']
piv.reset_index(inplace=True)
piv = piv.rename(columns={'N':'Not completed on time', 'Y':'Completed on time', 'Z':'Induction outstanding'})
print(piv.columns)
piv = piv.fillna(0)
piv['Total'] = piv['Completed on time'] + piv['Not completed on time'] + piv['Induction outstanding']
piv['% Compliance'] = (piv['Completed on time'] + piv['Not completed on time']) / piv['Total'] * 100




piv.to_excel('//ntserver5/generalDB/WorkforceDB/Inductions/current-stats-'+dt.datetime.today().strftime('%d-%m-%y')+'.xlsx', index=False)
print('Your file is available at '+'W:/Inductions/current-stats-'+dt.datetime.today().strftime('%d-%m-%y')+'.xlsx')
input("Press enter to quit")

#To build - pyinstaller -F --add-data "C:/Users/furnida286/PycharmProjects/inductions/venv/Lib/site-packages/pyfiglet/fonts;./pyfiglet/fonts" Inductions-Master.py --onefile --distpath "W:/Inductions"
