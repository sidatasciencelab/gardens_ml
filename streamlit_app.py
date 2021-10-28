import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import pandas as pd

st.markdown('## SI Gardens Tree Annotator')

query_params = st.experimental_get_query_params()
if 'tree_id' in query_params:
    tree_id = query_params['tree_id'][0]
else:
    tree_id = 'SG-2011-0516A'

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

if len(grid_response['selected_rows']):
    selected_tree = grid_response['selected_rows'][0]

else:
    selected_tree = {
        "accession_number": "2011-1257A",
        "scientific_name": "Prunus subhirtella 'Pendula'",
        "common_name": "Weeping Higan Cherry",
        "building": "NASM",
        "life_form": "Deciduous tree",
        "media_count": 4
        }

tree_col1, tree_col2 = st.columns(2)
with tree_col1:
    st.image('https://ids.si.edu/ids/deliveryService/id/SG-2011-1257A-WIN1-HL/500')
    st.write('Tree ID in Winter')
with tree_col2:
    st.write(selected_tree)

with st.form('annotation'):
    question_col1, question_col2 = st.columns(2)

    with question_col1:
        evergreen = st.radio('Question 1',
                            ['Deciduous','Evergreen','Unclear'],
                            index=2,
                            help='or broadleaf vs conifer??')

        pruning = st.radio('Question 2',
                            ['Natural pruning system',
                            'Topiary pruning system',
                            'Specialty pruning system',
                            'Unclear'],
                            index=3,
                            help='Details on Question 2')

        stem = st.radio('Question 3',
                            ['Single-stem',
                            'Multistem',
                            'Clump',
                            'Shrub',
                            'Unclear'],
                            index=4,
                            help='Details on Question 3')

    with question_col2:
        branched = st.radio('Question 4',
                            ['Low-branched',
                            'High-branched',
                            'Unclear'],
                            index=2,
                            help='Details on Question 4')

        tree_form = st.radio('Question 5',
                            ['Central leader form',
                            'Less commonly-defined pruning form',
                            'Unmanaged form',
                            'Unclear'],
                            index=3,
                            help='Details on Question 5')
        annotator = st.radio('Who is annotating?',
                             ['Courtney','Jake','Kayleigh'])
    submitted = st.form_submit_button('Submit Annotation')

st.sidebar.markdown('## Annotation Progress')

st.sidebar.markdown('*458* of *1,702* trees annotated')
st.sidebar.progress((458/1702))
