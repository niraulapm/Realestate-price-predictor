import pandas as pd 

data = pd.read_json('data.json')


price = data['price'].str.extract(r'(?P<price>\d+,\d+,\d+)')



price['price'] = price['price'].str.replace(',','')

area = data['area'].str.extract(r'(?P<area>\d+?.\d+)(?P<area_unit>[a-zA-Z]+)')

location = data['location'].str.extract(r'(?P<city>\w+).?-.?(?P<ward>\d+),.(?P<location>\w+)')

refined_data = pd.DataFrame()

refined_data['location'] = location['location']

refined_data['city'] = location['city']

refined_data['ward'] = location['ward']

refined_data['area'] = area['area']

refined_data['area_unit'] = area['area_unit']

refined_data['price'] = price['price']

refined_data['bathroom'] = data['bathroom']

refined_data['bedroom'] = data['bedroom']

refined_data['area'] = refined_data['area'].str.replace(',','')

def title(x):
    house_words = ['Home','House']
    land_words = ['Land','land']
    house = any(word in x for word in house_words)
    land = any(word in x for word in land_words)
    if house:
        return "House"
    elif land:
        return "Land"
    else:
        return "other"
 
property_type = data['title'].apply(title)
refined_data['property_type'] = property_type

refined_data['area_unit'].unique()

def same_unit(x):
    if x['area_unit'] == 'Dhur':
        x['area'] = float(x['area'])*16.93
    elif x['area_unit'] == 'AAna':
        x['area'] = float(x['area'])*31.80
    elif x['area_unit'] == 'Ropani':
        x['area'] = float(x['area'])*508.72
    elif x['area_unit'] == 'kaththa':
        x['area'] = float(x['area'])*338.63
    elif x['area_unit'] == 'bigha':
        x['area'] = float(x['area'])*6772.63
    elif x['area_unit'] == 'Sqft':
        x['area'] = float(x['area'])*0.09290304
    else:
        x['area'] = None
    return x['area']


refined_data['area'] = refined_data[['area','area_unit']].apply(same_unit,axis=1)

refined_data.drop('area_unit', axis=1, inplace=True)
refined_data.to_csv('refined_data.csv')