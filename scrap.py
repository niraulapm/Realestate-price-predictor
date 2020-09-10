
from bs4 import BeautifulSoup


def get_data(url):
    """Returns scrapped real state data from html file"""

    url = open(url)
    soup = BeautifulSoup(url, 'html.parser')
    soup = soup.find_all(
        "div", {"class": "wpl_property_listing_list_view_container"})
    soup = soup[0].find_all('div', {"class": "wpl-column"})
    for item in soup:
        data = {}
        data["title"] = item.div.a.get('title')
        data["location"] = item.find(
            'div', {"class": "wpl_prp_listing_location"}).get_text()
        data["price"] = item.find(
            'div', {'class': 'price_box'}).span.get('content')
        bedroom = item.find('div', {'class': 'bedroom'})
        if bedroom == None:
            data["bedroom"] = None
        else:
            data["bedroom"] = bedroom.find(
                'span', {'class': 'value'}).get_text()
        bathroom = item.find('div', {'class': 'bathroom'})
        if bathroom == None:
            data["bathroom"] = None
        else:
            data["bathroom"] = bathroom.find(
                'span', {'class': 'value'}).get_text()
        area = item.find('div', {'class': 'built_up_area'})
        if area == None:
            data["area"] = None
        else:
            data["area"] = area.get_text()

        all_data.append(data)
    return all_data



if __name__ == "__main__":
    import json

    urls = ['./htmls/kathmandu/kathmandu1.html','./htmls/kathmandu/kathmandu2.html',
    './htmls/kathmandu/kathmandu3.html','./htmls/lalitpur/lalitpur1.html',
    './htmls/bhaktapur/bhaktapur1.html','./htmls/bharatpur/bharatpur.html',
    './htmls/bharatpur/bharatpur2.html','./htmls/pokhara/pokhara1.html']
    
    all_data = []
    for url in urls:
        get_data(url)
    
    with open('data.json','w') as outfile:
        json.dump(all_data, outfile)