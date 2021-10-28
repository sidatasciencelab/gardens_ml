import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import pandas as pd

@st.cache
def fetch_data():
    df = pd.read_csv('garden_trees.tsv', sep='\t')
    return df

df = fetch_data()
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=False)
gb.configure_pagination(paginationAutoPageSize=True)
gridOptions = gb.build()
grid_response = AgGrid(
    df, 
    gridOptions=gridOptions,
    height=500, 
    width='100%',
    return_mode='AS_INPUT',
    update_mode='SELECTION_CHANGED',
    fit_columns_on_grid_load=False,
    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    )

st.write(grid_response['selected_rows'])