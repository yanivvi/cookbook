import pandas as pd
import streamlit as st

with open('raw_data.csv', 'r') as f:
    data = pd.read_csv(f)

selected_supermarket = st.selectbox('Select Supermarket', ['Carrefour', 'Victory', 'Shufersal'])


def supermarket_search(search_term):
    if selected_supermarket == 'Carrefour':
        url = 'https://www.carrefour.co.il/search/'
    elif selected_supermarket == 'Victory':
        url = 'https://www.victoryonline.co.il/search/'
    elif selected_supermarket == 'Shufersal':
        url = 'https://www.shufersal.co.il/online/he/search?text='
    else:
        raise ValueError('Invalid supermarket')
    
    search_url = url + search_term
    return search_url

def recepie():
    st.title('recepies')
    recepie = st.selectbox('Select Recepie',set(data.recipe_name))

    recepie_data = data[data.recipe_name == recepie]
    sections = set(recepie_data["section id"].unique())
    for section in sections:
        section_data = recepie_data[recepie_data["section id"] == section]
        cols = ["ingrediant_qty", "ingrediant_name", "measure_unit"]
        
        section_data['full_name'] = section_data[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        section_data['item_url'] = section_data['ingrediant_name'].apply(lambda x: supermarket_search(x))
        st.header(str(section_data["section_name"].values[0]))
        for i in section_data.index:
            hyperlink = f'[buy]({section_data.loc[i, "item_url"].replace(" ","%20")})'
            st.write(section_data.loc[i, "full_name"], hyperlink)

    st.header("הוראות")
    for section in sections:
        st.write(str(section_data["instructions"].values[0]))

if __name__ == '__main__':
    recepie()
