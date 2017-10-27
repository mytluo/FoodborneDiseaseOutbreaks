
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd

# http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
state_codes = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'Washington DC',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

   
def get_tables_from_html(html_doc):
    """
    Return a list of table tag references from the html document
    for the table we're interested in parsing.
    """
    html = BeautifulSoup(html_doc, 'html.parser')
    return html.find("table", class_="wikitable sortable collapsible collapsed")

def parse_table(table):
    """
    Parse a table into a Pandas DataFrame using a schema reflecting the columns we're 
    interested in.
    """
    st_heads = table.find_all("th")
    states = [] 
    for s in st_heads:
        try:
            states.append(state_codes[s.text])
        except:
            states.append("Year")

    rows = table.find_all("tr")
    rows = rows[1:]
    for i, r in enumerate(rows):
            temp = "".join(r.text).strip().replace(",", "").replace("n/a", "-1")
            rows[i] = map(int, temp.split("\n"))
    
    popdat = {x: [] for x in states}
    for r in rows:
        if r[0] > 1997: # interested in years 1998-2015 only
            for dat, head in zip(r, states):
                popdat[head].append(dat)
        else:
            continue

    # We have all our data, so return a Pandas frame
    return pd.DataFrame.from_dict(popdat)
        


