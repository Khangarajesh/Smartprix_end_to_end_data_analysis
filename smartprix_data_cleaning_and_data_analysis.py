# -*- coding: utf-8 -*-
"""smartprix data cleaning and data analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i-uHVhyIXEWpfmezlM6nNJDtewrQ3kMP
"""

import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
import re
import seaborn as sns 
import plotly.express as px
import matplotlib.pyplot as plt

with open('smartprix.html', 'r', encoding  = 'utf-8') as f:
  html = f.read()
  
html

"""**Data Extraction Using Beautifulsoup**"""

soup = BeautifulSoup(html)

name = []
spec_scpre = []
img = []
sim = []
processor = []
storage = []
battery = []
display = []
camera = []
memmory = []
version = []
price = []
for i in soup.find_all('div', class_="sm-product has-tag has-features has-actions"):
  #extract name
  name.append(i.find('h2').text.strip())
  #extract spec score
  try:
    spec_scpre.append(i.find('div', class_= 'score rank-2-bg').find('b').text)
  except:
    spec_scpre.append(np.nan)
  #extract image link
  img.append(i.find('div', class_ = 'sm-img-wrap').find('img').get('src'))
  #extract sim info
  sim.append(i.find_all('li')[0].text)
  #extract processor
  processor.append(i.find_all('li')[1].text)
  #extract storage
  storage.append(i.find_all('li')[2].text)
  #extract battery power
  battery.append(i.find_all('li')[3].text)
  #dextract display info
  display.append(i.find_all('li')[4].text)
  #extract camera info 
  try:
    camera.append(i.find_all('li')[5].text)
  except:
    camera.append(np.nan)
  #extract memmory info
  try :
    memmory.append(i.find_all('li')[6].text)
  except:
    memmory.append(np.nan)
  #extract version info
  try:
    version.append(i.find_all('li')[7].text)
  except:
    version.append(np.nan)
  #extract price
  price.append(i.find('span', class_='price').text)

df = pd.DataFrame({
   'img':img, 
   'name':name,
   'price':price,
   'spec_scpre':spec_scpre,
   'sim':sim,
   'processor':processor,
   'storage':storage,
   'battery':battery,
   'display':display,
   'camera':camera,
   'memmory':memmory,
   'version':version

})

"""**Data Accessing**

This data contains information of smart phones and its detail which I have extracted from https://www.smartprix.com/mobiles.

**columns**


*   img : Smart phone image

*   name : Smart phone name

*   spec_scpre : Score given by smartprix. Higher the score better is the phone

*   sim : 3G, 4G, 5G support, VoLTE wifi, NFC ,IR blaster support 
*   processor : processor name, processing systems and clock speed (processing systems and clock speed are responsible for mobile performance


*   storage : RAM AND ROM information


*   battery : Batttery capacity and battery charging speed


*   display : Scrren size, screen resolution , refressh rate


*   camera : Rear camera and front camera mega pixle

*   memmory : Memorry card support and extention
*   version : Version of mobile ( Android, ios)


*   price : Mobile phone price
"""



"""**Data Accessing**

*Quality Issues*

*   name column contains name ,5G support and memmory information `validity`
*   OPPO written differently Oppo `consistency`
*   spec_score column contains null values `completeness`


*   Feature phones are present in a data `validity`(541, 570. 572, 576, 619, 621, 624,626,635, 644,660,661)
*   596, 629Ram not given `consistency`
*   Fast charging value not mention for some phones `consistency`
*   389 390 592 674row in camera column contains unwanted info `validity`
*   version column containing memmory card No FM Radio , Bluetooth  `validity`

*Tidiness Issues*


*   5g,NFC, IR BLASTER present in sim column , need to assign seperate column for each


*   processor name, processing systems and clock speed given in singlr processor column 
*   839, 932 shifted to right 
*  77, 110, 190, 275, 420, 511, 512, 596, 629, 730, 796 data shifted left


*   Ram Rom stored in single column
*   battery capacity and w fast charging in a same column
*   Display column contains Scrren size, screen resolution , refressh rate and display type in same column 
*   Front and rear camera present in a same a column
*   389 390 592 674, 280 shifted to right camera
*   7, 8, 12, 15 , 23 shifted left
*   Memmory card support and extension present in a same column

##Data Cleaning
"""

df.shape

df.head()

df.to_excel('smartprix.xlsx')

#chacking name column
#df['name'].str.split().str.get(0).value_counts()

df['index'] = np.array(range(2,962))
df.set_index('index',inplace =True)

"""##Remove Feature phone

after observing the data i found that most of the feature phones has price below 3400. So we will remove them from our data.
"""

df.loc[[541,570,572,576,619,621,624,626,635,644,660,661], : ]

df['price'] = df['price'].str.replace('???', '').str.replace(',', '').astype('int')

df[df['price'].between(3000,3400)]
pd.set_option('display.max_rows', 500)

df = df[df['price'] > 3400]

df.head(2)
df.shape

df = df[~df['sim'].isin(['Single Sim, 3G, 4G, Wi-Fi, HDMI', 'Dual Sim', 'Dual Sim, 3G, 4G, VoLTE', 'Dual Sim, 3G, 4G'])]
df.shape

df.to_excel('smart.xlsx')

"""##Define
`name` 
1.   replace 5G with '' using replace 
2.   replace (storage info ) with '' using regex

`sim`
1.   Create different column for 5G NFC AND IR Blaster using apply function

`memmory and version`


1.  shifted columns acordingly using shift metode




"""



"""## Column shifting"""

#77, 110, 190, 275, 420, 511, 512, 596, 629, 730, 796
#389 390 592 674, 280
#7, 8, 12, 15 , 23
#839,932

df.loc[[7, 8, 12, 15 , 23, 77, 110, 190, 275, 280, 389, 390, 420, 511, 512, 592, 596, 629, 730, 796, 839, 932], 'name':]

# memmory column containing android word shifte to =>right
temp_df = df[df['memmory'].str.contains('Android')]
x = temp_df.iloc[:,10:].shift(1, axis = 1).values
df.loc[temp_df.index, temp_df.columns[10:]] = x

# memmory column containing iOS word shifte to =>right
temp_df1 = df[~df['memmory'].isna()]
temp_df1 = temp_df1[temp_df1['memmory'].str.contains('iOS')]
x1 = temp_df1.iloc[:,-5:].shift(1, axis = 1).values
df.loc[temp_df1.index, temp_df1.columns[-5:]] = x1

# memmory column containing camera word shifte to <= left
temp_df2 = df[~df['memmory'].isna()]
temp_df2 = temp_df2[temp_df2['memmory'].str.contains('Camera')]
temp_df2 = temp_df2[~temp_df2['camera'].str.contains('Dual Display')].iloc[:, 5:].shift(-1, axis = 1)
df.loc[temp_df2.index, temp_df2.columns] = temp_df2.values

# memmory column containing camera word shifte to <= left
temp_df3 = df[~df['memmory'].isna()]
temp_df3 = temp_df3[temp_df3['memmory'].str.contains('Camera')]
temp_df3 = temp_df3.loc[:, ['camera', 'memmory']].shift(-1, axis = 1)
df.loc[temp_df3.index, temp_df3.columns] = temp_df3.values

#shift => to right by 1 ('processor','storage', 'memmory', 'version')
temp_df_ps_mv = df[df['memmory'] == 'iOS v13']
temp_df_ps_mv = temp_df_ps_mv.loc[:, ['processor','storage', 'memmory', 'version']].shift(1, axis = 1)
df.loc[temp_df_ps_mv.index, temp_df_ps_mv.columns] = temp_df_ps_mv.values

# shift to<= left version to memmory value shift
temp_df_ver_mem = df[~df['version'].isna()]
temp_df_ver_mem = temp_df_ver_mem[temp_df_ver_mem['version'].str.contains('Memory')]
temp_df_ver_mem = temp_df_ver_mem.iloc[:, -2:].shift(-1, axis = 1)
df.loc[temp_df_ver_mem.index, temp_df_ver_mem.columns] = temp_df_ver_mem.values

df[df['camera'] == 'Memory Card Supported, upto 256???GB']

#camera column containing memmory shift right =>
temp_df_c = df[~df['camera'].isna()]
temp_df_c = temp_df_c[temp_df_c['camera'].str.contains('Memory')]
temp_df_c = temp_df_c.iloc[:, 5:-1].shift(1, axis = 1)
df.loc[temp_df_c.index, temp_df_c.columns] = temp_df_c.values

df.shape



"""##Name """

#Cleaning name column 
df['name'] = df['name'].str.replace('5G', '')

df['name'] = df['name'].apply( lambda x: re.sub("\(.*?\)","",x))

#creating seperate column for 5g,Nfc , IR_blaster, and total_sim
df['5G'] = df['sim'].apply(lambda x:1 if '5G' in x else 0)
df['NFC'] = df['sim'].apply(lambda x:1 if 'NFC' in x else 0)
df['IR_blaster'] = df['sim'].apply(lambda x:1 if 'IR Blaster' in x else 0)
df['total_sim'] = df['sim'].apply(lambda x:2 if 'Dual' in x else 1)

df.drop('sim', axis =1, inplace =True)

df['total_sim'].value_counts()

"""##storage"""



df['storage'] = df['storage'].str.split(',')

#seperate ram and rom 
df['ram'] = df['storage'].apply(lambda x: x[0] if 'inbuilt' not in x[0] else 0)
df['rom'] = df['storage'].apply(lambda x: x[-1])
df.drop('storage', axis = 1, inplace = True)

df['ram'].value_counts()

#RAM
#cleaning ram column (completeness and validity issue)
df['ram'] = df['ram'].str.replace('GB RAM', '')
df.loc[[317,627,667], 'ram'] = '4'   #iphone se3 models has ram 4 gb for all 16, 64 and  256 gb phones
df.loc[353, 'ram'] = '12'     #Huawei Mate 50 RS Porsche Design has ram 12 gb
df['ram'] = df['ram'].astype('int')



#ROM
df['rom'] = df['rom'].str.strip().str.extract('(\d+)').astype('int')  #new learning
df['rom'] = df['rom'].apply(lambda x:1024 if x== 1 else x)

df['rom'].value_counts()

"""##battery"""

#seperating battery capacity and fast charging column
df['battery'] = df['battery'].str.split('with')
df['battery_cap'] = df['battery'].str.get(0)
df['fast_charging'] = df['battery'].str.get(1)

df.drop('battery', axis = 1, inplace = True)

#battery capacity
df['battery_cap'] = df['battery_cap'].str.extract('(\d+)')

#fast charging
df['fast_charging'] = df['fast_charging'].str.strip().str.findall(r'\d{2,3}')

# 1 for has Fastcharging value 0 for only Fastcharging and -1 for nan values
def fast_charging_track(item):
  if type(item) == list:
    if len(item) == 1:
      return item[0]
    else:
      return 0
  else:
    return -1

df['fast_charging'] = df['fast_charging'].apply(fast_charging_track)



"""##display"""

df['display'] = df['display'].str.split(',')

df['screen_size'] = df['display'].str.get(0)

df['resolution'] = df['display'].str.get(1).str.split('px').str.get(0)

df['refresh_rate'] = df['display'].str.get(2).str.split('Hz').str.get(0)

df['display_type'] = df['display'].str.get(2).str.split('Hz').str.get(1)

#display type cleaning
df['display_type'].isnull().sum()

temp_display_t = df[df['display_type'].isna()]
df.loc[temp_display_t.index, 'display_type'] = temp_display_t['display'].str.get(1).str.split('px').str.get(1).values

df['display_type'].isnull().sum()

df['display_type'] = df['display_type'].str.replace(' Display with', '')

#scree size cleaning
df['screen_size'] = df['screen_size'].str.split().str.get(0).astype(float)
df['screen_size'].value_counts()

#refresh rate cleaning
df['refresh_rate'] = df['refresh_rate'].apply(lambda x: 60 if pd.isna(x) else x)
df['refresh_rate'] = df['refresh_rate'].str.strip().astype(float)
df['refresh_rate'].value_counts()

df.drop('display', axis = 1 , inplace = True)



"""##camera"""

df['rear_camera'] = df['camera'].str.split('&').str.get(0)
df['front_camera'] = df['camera'].str.split('&').str.get(1)

df[df['front_camera'].isna()]

def camera_extractor(text):
  if 'Dual' in text:
    return 2
  elif 'Triple' in text:
    return 3
  elif 'Quad' in text:
    return 4
  elif 'missing' in text:
    return 'missing'
  else:
    return 1

df['num_rear_camera'] = df['rear_camera'].apply(camera_extractor)
df['primary_rear_camera'] = df['rear_camera'].str.strip().str[:5].str.extract("(\d+)").astype(float)

df['front_camera'].value_counts()
df['front_camera'] = df['front_camera'].fillna('missing')
df['num_front_camera']  = df['front_camera'].apply(camera_extractor)
df['primary_front_camera'] = df['front_camera'].str.strip().str[:5].str.extract("(\d+)").astype(float)

df['primary_rear_camera'].value_counts()

df.drop('camera', axis = 1, inplace = True)

"""##memmory"""

df['memmory_support'] = df['memmory'].str.split(',').str.get(0)
df['memmory_extenion'] = df['memmory'].str.split(',').str.get(1)

df['memmory_support'].value_counts()

#since all mobile which has nan value in memmory suport column does not support memmory 
df['memmory_support'] = df['memmory_support'].fillna('Memory Card Not Supported')
df['memmory_support'].isna().sum()

df['memmory_support_10'] = df['memmory_support'].apply(lambda x:0 if 'Not' in x else 1)

if 'Not' in 'Not supported':
  print('hey ')



df['memmory_extenion'] = df['memmory_extenion'].str.extract('(\d+)')
#since phones which does not support memmory card can not extende memmory

df.iloc[: , -3:].head(10)

df.drop('memmory', axis = 1, inplace = True)

"""##processor"""

#df['processor'].str.split(',').value_counts()

pd.set_option('display.max_columns', 500)
df.head(2)

#seperate processor_name, core and clock_speed columns
df['processor_name'] = df['processor'].str.split(',').str.get(0)
df['core'] = df['processor'].str.split(',').str.get(1)
df['clock_speed'] = df['processor'].str.split(',').str.get(2)

#shifting to right =>
t_df = df[['processor_name', 'core', 'clock_speed']]
t_df = t_df[~t_df['processor_name'].isna()]
t_df = t_df[t_df['processor_name'].str.contains('Core')].shift(1, axis = 1)
df.loc[t_df.index, t_df.columns] = t_df.values

#processor_brand
df['processor_name'] = df['processor_name'].str.strip()
processor_brand = df['processor_name'].str.split().str.get(0).str.lower()
df.insert(27,'processor_brand', processor_brand)





#cleaning core column
temp_core = df[~df['core'].isna()]
temp_core = temp_core['core'].str.strip().str.split().apply(lambda x: ' '.join(x[:2]))
df.loc[temp_core.index, 'core'] = temp_core.values

#clock_speed
df['clock_speed'] = df['clock_speed'].str.strip()

df.drop('processor', axis = 1, inplace =True)

#create mobile brand
brand = df['name'].str.strip().str.split().str.get(0).str.lower()
df.insert(2, 'brand', brand)

df.drop(['memmory_support','rear_camera', 'front_camera'], axis = 1, inplace =True)

df['display_type'].value_counts()

df.head(10)

"""#Brand

Top 10 brands in terms of number of product
"""

df.groupby('brand')['name'].count().sort_values(ascending = False).head(10).plot(kind = 'barh')

df['brand'].isnull().sum()

"""#Price

Conclusion


*   Data is positivly skew
*   Outliers are present in data (because of brands like apple) 
*   Most of the phones have price below 25000
*   Huawei Mate 50 RS Porsche Design this phone is an outlier its price is too high because of its design and not because of any other mobile specification so we will not consider this phone


"""

df['price'].describe()

"""outliers treatment in price column"""

df[df['price']>200000]

"""Huawei Mate 50 RS Porsche Design this phone is an outlier its price is too high because of its design and not because of any other mobile specification so we will not consider this phone"""

df = df[df['price']<200000]
df['price'].isnull().sum()

df['price'].plot(kind = 'hist', bins = 20)

df['price'].plot(kind = 'kde')

df['price'].skew()

df['price'].plot(kind = 'box')

"""#Spec_score
Conclusion


*   Data is almost normally distributed
*   9% of data is missing
*   Because this column depends upon almost all the other column we will fill missing values of this column using knn imputer


"""

df['spec_scpre'] = df['spec_scpre'].astype(float)
df['spec_scpre'].describe()

df['spec_scpre'].plot(kind = 'kde')

df['spec_scpre'].skew()

df['spec_scpre'].isna().sum()/df.shape[0]*100

df['spec_scpre'].plot(kind = 'box')

df.head()

"""#Version
*  94%  of the mobile phones have os android
*  only 1 phone has different os so we will remove them
*  since all the phones version that have missing values have operating system android we will fill them with android
"""

df['version'].isna().sum()

def version_cat(name):

  if 'Android' in name:
    return 'Android'
  elif 'iOS' in name:
    return 'iOS'
  else:
    return 'Others'

os = df[~df['version'].isna()]['version'].apply(version_cat)
df.loc[os.index, 'version'] = os.values

df['version'].value_counts()

#Removing phone whos os is Others
df = df[df['version'] != 'Others']

df['version'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['version'].isnull().sum()

df[df['version'].isna()]

"""###since all the phones version that have missing values have operating system android we will fill them with android"""

df['version'].fillna('Android', inplace = True)

df['version'].isna().sum()

"""#5G 
35% phones are 5G inabled
"""

df['5G'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['5G'].isna().sum()



"""#NFC
26% phones have NFC technology
"""

df['NFC'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['NFC'].isna().sum()

"""#IR_Blaster

* Only 14% phones have ir blaster and most of the chinese phones have ir_blaster feature
"""

df['IR_blaster'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df[df['IR_blaster'] == 1]['brand'].value_counts()

df['IR_blaster'].isna().sum()

"""#Total sim
Since 99% phones have dual sim, there is no point to keep this column for analysis.we will drop this column
"""

df['total_sim'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df.drop('total_sim', axis = 1, inplace = True)

"""#Ram
*  80% of the phones in a market have ram 4,8 or6 GB
"""

df['ram'].value_counts().plot(kind = 'bar')

df['ram'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['ram'].isna().sum()

"""#Rom
*  42% of the phones in a market have a rom of 128 GB

*  There are phones in a market who are giving an option to extend internal storage upto 1024 gb
"""

df['rom'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['rom'].isna().sum()



"""#Battery capacity
*  Data is almost normally distributed
*  Most of the phones have battery capacity between 4500 - 5000
*  Battery cap of iphone 12 series and SE  is missing so we will fill them with avg battcap of iphone 12 which is 2886 and for SE 2018
"""

df['battery_cap'] = df['battery_cap'].astype(float)

df['battery_cap'].plot(kind = 'hist', bins = 20)

df['battery_cap'].plot(kind = 'kde')

df['battery_cap'].skew()

df['battery_cap'].describe()

df['battery_cap'].plot(kind = 'box')

df[df['battery_cap']>8000]

temp_df = df[df['brand'] == 'apple']
temp_df['name'] = temp_df['name'].str.strip()
temp_df[temp_df['battery_cap'].isna()]['name'].value_counts().sort_index()

temp_df.groupby('name')['battery_cap'].mean()

#avg battery cap of ihone 12 series is 2886 and se has batt cap 2018
df['name'] = df['name'].str.strip()
index_ = df[df['name'].str.contains('Apple iPhone 12')].index
df.loc[index_, 'battery_cap'] = 2886

index_ = df[df['battery_cap'].isna()].index
df.loc[index_, 'battery_cap'] = 2018

df['battery_cap'].isna().sum()

"""#Fast charging
Data is positively skewed

Almost 74% of the phones in a market have fastcharging feature

Data has outliers but this outiers are really exists
"""

fastcharg_ava = df['fast_charging'].apply(lambda x:0 if x == -1 else 1 )
df.insert(12 , 'fastcharg_ava', fastcharg_ava)

df['fastcharg_ava'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['fast_charging'] = df['fast_charging'].astype(int)
df[df['fast_charging']!=-1]['fast_charging'].describe()#plot(kind = 'hist', bins = 20)

df['fast_charging'].plot(kind = 'hist', bins = 20)

df['fast_charging'].skew()

df[df['fast_charging'] == 180]

df[df['fast_charging']!=-1]['fast_charging'].plot(kind = 'box')

df['fast_charging'].isna().sum()

"""#Screen size
Data is negetively skewed

Data has outliers but thise values are real and can be use to distinguish the phones like samsung flip which has special feature of fliping screen,This will help in analysis 
"""

df['screen_size'].describe()

df['screen_size'].plot(kind = 'kde')

df['screen_size'].skew()

df['screen_size'].plot(kind = 'box')

df['screen_size'].isna().sum()

"""#Resolution
we can create new column of ppi using screen size and resolution 
"""

screen_width = df['resolution'].apply(lambda x: x.split('x')[0])
screen_height = df['resolution'].apply(lambda x: x.split('x')[1])

df.insert(14, 'screen_width', screen_width)
df.insert(15, 'screen_height', screen_height)



"""###Refresh Rate
more than 50% values are absent in data

after checking all the models specification on google i found that refresh rate of all the phones who has a missing value in refresh rate column is 60Hz
"""

df['refresh_rate'].isna().sum()/df.shape[0]*100

df['refresh_rate'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

pd.crosstab(df['refresh_rate'], df['brand'], normalize = 'columns')*100

#df[df['refresh_rate'].isna()]['name'].value_counts()

"""since almost all the phones have reresh rate 60Hz we will fill missing values with 60 Hz"""

df['refresh_rate'].fillna(60,inplace = True)

df['refresh_rate'].isna().sum()

df['refresh_rate'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

"""#Display Type
Most of the phones have display tipe either Punch Hole or Water Drop Notch
"""

df['display_type'] = df['display_type'].str.strip()
df['display_type'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['display_type'].isna().sum()

"""#num_rear_camera
almost 47% mobile phones have 3 camera in the rear
"""

df['num_rear_camera'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['num_rear_camera'].isna().sum()

"""#primary_rear_camera
*  25% mobile has 50mp camera in rear
"""

df['primary_rear_camera'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df[df['primary_rear_camera'] == 200]

df['primary_rear_camera'].isna().sum()

"""#num_front_camera
* 97% phones have single camera at front 
"""

df['num_front_camera'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['num_front_camera'] = df['num_front_camera'].replace('missing', 0).astype(int)
df['num_front_camera'].value_counts()

"""#primary_front_camera
most of the phones have front camera of 16, 8 and 5 mega pixle

one missing value itel A23s as it does not have front camera so we will replave nan with 0
"""

df['primary_front_camera'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['primary_front_camera'].value_counts()

df['primary_front_camera'].fillna(0, inplace =True)
df['primary_front_camera'].isna().sum()

"""#memmory_extenion
 

*   almost 32% of data is missing
*   in missing data some phones do not have memmory slot and some phones have.
*   so phoens who have memmory slot need to be fill with proper value using knn imputer
*   and remaining will be zero
*   after performing above steps missing values are 8%


"""

df['memmory_extenion'] = df['memmory_extenion'].astype(float)

df['memmory_extenion'] = df['memmory_extenion'].replace(1, 1024).replace(2, 2048)

df['memmory_extenion'].value_counts()

df['memmory_extenion'].isna().sum()/df.shape[0]*100

#replacing missing values with zero where memmory support is not available
temp_df1 = df[df['memmory_extenion'].isna()]
index_ = temp_df1[temp_df1['memmory_support_10'] == 0].index
df.loc[index_, 'memmory_extenion'] = 0

df[df['name'] == 'Xiaomi Mi 11 Lite NE']

df['memmory_extenion'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

"""#memmory_support_10"""

df['memmory_support_10'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['memmory_support_10'].isna().sum()

"""#processor_brand
*  Most of the processor brands in a phone are snapdragaon and mediatek
*  3.3% of data is missing
*  after researching on google i found that, all the phones that have missing values in processor brand  are using mediatek 
processor except itel and apple who is using unisoc and bionic respectively
"""

df['processor_brand'].value_counts()

def processor_name(name):
  if name == 'qualcomm':
    return 'snapdragon'
  elif name == 'tiger' or name == 'sc9863a' or name == 'sprd' or name == 'spreadtrum':
    return 'unisoc'
  elif name == 'a13':
    return 'bionic'
  elif name == 'mt' or name == 'helio' or name == 'dimensity':
    return 'mediatek'
  else:
    return name

df['processor_brand'].apply(processor_name).value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['processor_brand'].isna().sum()/df.shape[0]*100

df['processor_brand'].isna().sum()

df[df['processor_brand'].isna()]['name'].value_counts()

"""after researching on google i found that, all the phones are using mediatek 
processor except itel, it is using unisoc processor
"""



temp_df2 = df[df['processor_brand'].isna()]

def pbrand_fillna(name):
  if name == 'itel':
    return 'unisoc'
  elif name == 'apple':
    return 'bionic'
  else:
    return 'mediatek'

temp_df2['brand'] = temp_df2['brand'].apply(pbrand_fillna)
df.loc[temp_df2.index, 'processor_brand'] = np.array(temp_df2['brand'])

df['processor_brand'].apply(processor_name).value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df['processor_brand'].isna().sum()

"""#Core
*  Most of the phones have octa core processor
*  Missing values are present in a data we will fill them with knn imputation 
"""

df['core'] = df['core'].replace('Octa Core', 8).replace('Quad Core', 4).replace('Hexa Core', 6)

df['core'].value_counts().plot(kind = 'pie', autopct = '%0.1f%%')

df[df['core'].isna()]

"""#clock_speed
*  outliers are present in a data(this mainly includes iphone whos clock speed is greater rhan 3)
*  Most of the phones have clock speed between 2 - 2.4
"""

df['clock_speed'] = df['clock_speed'].str.replace('???GHz Processor', '').str.strip().astype(float)

df['clock_speed'].describe()

df['clock_speed'].plot(kind = 'hist', bins = 20)

df['clock_speed'].plot(kind = 'kde')

df['clock_speed'].skew()

df['clock_speed'].plot(kind = 'box')

df[df['clock_speed']>3.0]['brand'].value_counts()

"""#Conclusions from univariate analysis

*  realme, xiaomi, samsung, vivo and oppo have more than 50 products in the market
*  Most of the phones have price below 25000
*  94%  of the mobile phones have os android
*  35% phones are 5G inabled
*  26% phones have NFC technology
* Only 14% phones have ir blaster and most of the chinese phones have ir_blaster feature
*  80% of the phones in a market have ram 4,8 or6 GB
*  42% of the phones in a market have a rom of 128 GB
*  Most of the phones have battery capacity between 4500 - 5000
*  Almost 74% of the phones in a market have fastcharging feature
*  More than 50% of the phones have refresh rate 60Hz
*  Most of the phones have display tipe either Punch Hole or Water Drop Notch
*  Almost 47% mobile phones have 3 camera in the rear
*  25% mobile has 50mp camera in rear
*  most of the phones have front camera of 16, 8 and 5 mega pixle
*  Most of the processor brands in a phone are snapdragaon and mediatek
*  90% of the phones have octa core processor
*  Most of the phones have clock speed between 2 - 2.4

#Bivariate analysis

Lets create a heatmap and see how our output column(i.e price) is corelated with other column
"""

plt.figure(figsize = (30,12))
sns.heatmap(df.corr(), annot = True, linewidths = 0.1 )



"""##Price and spec_score
*  we can see that all the high end phones and phones which have price more than average have spec_score above 74
*  and all the phones abovr spec_score 85 have price more than 25000(avg price)

> Indented block


"""

plt.figure(figsize = (15,10))
sns.scatterplot(data = df, x = 'spec_scpre', y = 'price')
plt.axhline(y = df['price'].mean(), color = 'red')
plt.axvline(x = 74, color = 'red')
plt.grid()

df['price'].mean()

"""##Price and 5G
*  we can see that phones that supporting 5G are costlier and have a avg price of 40000
"""

sns.barplot(data = df, x = '5G', y = 'price')
plt.grid()



"""##Price and NFC
Phones which has NFC support have avg price more than 50000which is higher than 5G phones
"""

sns.barplot(data = df, x = 'NFC', y = 'price')
plt.grid()

"""#Price and RAM 
*  Price is higly dependent on RAM.As RAM increases price of the phone also increses
*  Phones having ram 6 or more than 6 have avg price above 25000
"""

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'ram', y = 'price')

"""#Price and ROM
* As ROM increses price increses
* Mobile phones having rom 256 or above 256 are higher end phones and their avg price is more than 50k
"""

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'rom', y = 'price')

"""##Price and fast charging
*  Having fast charging tech puts mobilr price bit higer side
"""

sns.barplot(data = df, x = 'fastcharg_ava', y = 'price')

plt.figure(figsize = (12,10))
df.groupby('fast_charging')['price'].mean().plot(kind = 'bar')

"""##Price and refresh rate 
higer end phones have refresh rate more than 90
"""

sns.barplot(data = df, x = 'refresh_rate', y = 'price')
plt.grid()

"""##Price and camera 
seems like price does not depend much on camera mp
"""

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'primary_front_camera', y = 'price')
plt.grid()

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'primary_rear_camera', y = 'price')
plt.grid()

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'num_rear_camera', y = 'price')
plt.grid()

"""#Price and memmory_support_10
Apperently phone which does not have memory extention are higher end phones(may be becaause of iphone)
"""

plt.figure(figsize = (12,10))
sns.barplot(data = df, x = 'memmory_support_10', y = 'price')
plt.grid()



"""#Price and clock speed
Phones having clock speed above 2.5 have average price more than 20k
"""

plt.figure(figsize = (12,10))
temp = df.groupby('clock_speed')['price'].mean()
sns.barplot(data = df, x = temp.index, y = temp.values)
plt.grid()

"""#Price and brand

apple, sony has very high avg price (above 80000)
"""

plt.figure(figsize = (20,10))
temp_series = df.groupby('brand')['price'].mean().sort_values(ascending = False)
sns.barplot( x = temp_series.values, y = temp_series.index, orient='h')
plt.grid()

"""##Price and display type
small notch and large notch display type have avg price more than 60k
"""

sns.barplot(data = df, x = 'display_type', y = 'price')
plt.xticks(rotation = 'vertical')

"""##Price and processor brand

mobile phone which has the processor of bionic and google are highr end phones 

budget phones have processor of kirin, unisoc or mediatek
"""

df['processor_brand1'] = df['processor_brand'].apply(processor_name)

sns.barplot(data = df, x = 'price', y = 'processor_brand1', orient = 'h')

"""#Conclusions from bivariate analysis
*  we can see that all the high end phones and phones which have price more than average have spec_score above 74
*  and all the phones abovr spec_score 85 have price more than 25000(avg price)
*  we can see that phones that supporting 5G are costlier and have a avg price of 40000
*  Phones which has NFC support have avg price more than 50000which is higher than 5G phones
*  Price is higly dependent on RAM.As RAM increases price of the phone also increses
*  Phones having ram 6 or more than 6 have avg price above 25000
* As ROM increses price increses
* Mobile phones having rom 256 or above 256 are higher end phones and their avg price is more than 50k
*  Having fast charging tech puts mobilr price bit higer side
*higer end phones have refresh rate more than 90
*  Phones having clock speed above 2.5 have average price more than 20k
*  apple, sony has very high avg price (above 80000)
*  small notch and large notch display type have avg price more than 60k
*  mobile phone which has the processor of bionic and google are highr end phones 
*  budget phones have processor of kirin, unisoc or mediatek
##It is important to consider brand column while doing machine learning because mobile price is very highly dependent on mobile brand

#Multivariate analysis

we can see from the heatmap spec score depends on many other columns, we will fill missing values of spec score using knn imputer

#Missing value imputation
"""

df['screen_width'] = df['screen_width'].astype(int)
df['screen_height'] = df['screen_height'].astype(int)
df['screen_size'] = df['screen_size'].astype(int)

x_df = df.select_dtypes(include = ['int64', 'float64'])#.drop('price', axis = 1)

x_df.head()

from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors = 5)

x_df_values = imputer.fit_transform(x_df)

y_df = pd.DataFrame(x_df_values, columns  = x_df.columns)

#y_df['price'] = df['price']

y_df.corr()['price'].reset_index().merge(df.corr()['price'].reset_index(), on = 'index')

y_df['name'] = df['name']

"""*  mobile phone spec score is highly dependent on ram & rom
*  some brands like apple are charging more because of high internal storage
"""

px.scatter(y_df, x = 'spec_scpre', y = 'price', color = 'ram', size = 'rom', hover_name ='name', symbol ='5G', title = 'price and spec_score according to ram and rom')

"""#Feature Engieering
craeting new columns pixle per inch (ppi)
"""

def ppi(width, height, size):
  return round(((width**2 + height**2)**0.5)/size, 2)

y_df['ppi'] = y_df.apply(lambda x: ppi(x['screen_width'], x['screen_height'], x['screen_size']), axis = 1)

y_df.drop(['screen_width', 'screen_height', 'screen_size'], axis = 1, inplace = True)

y_df['display_type'] = df['display_type']

y_df['ppi'].describe()

y_df['ppi'].plot(kind = 'hist', bins = 20)

"""## most of the phones have ppi in either 300 and 450"""

