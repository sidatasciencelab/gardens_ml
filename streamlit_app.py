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
    image_df = pd.read_csv('garden_edan_image_data.tsv', sep='\t')
    return df, image_df

df, image_df = fetch_data()

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
    search_id = f'SG-{selected_tree["accession_number"]}'
    selected_images = image_df[image_df['object_id'] == search_id]['ids_id'].tolist()

else:
    selected_tree = {
        "accession_number": "2011-1257A",
        "scientific_name": "Prunus subhirtella 'Pendula'",
        "common_name": "Weeping Higan Cherry",
        "building": "NASM",
        "life_form": "Deciduous tree",
        "media_count": 4
        }
    selected_images = []
    im_to_show = 'SG-2011-1257A-WIN1-HL'

tree_col1, tree_col2 = st.columns(2)
with tree_col2:
    st.write(selected_tree)
    if len(selected_images) > 0:
        im_to_show = st.radio('Image to show',
                              selected_images,
                               index=0)
with tree_col1:
    image_url = f'https://ids.si.edu/ids/deliveryService/id/{im_to_show}/500'
    st.image(image_url)
    st.write(im_to_show)

evergreen = st.radio('Is the tree deciduous or evergreen?',
                    ['Deciduous','Evergreen','Unclear'],
                    index=2,
                    help='or broadleaf vs conifer??')

pruning = st.radio('What type of pruning system is employed?',
                    ['Natural pruning system',
                    'Topiary pruning system',
                    'Specialty pruning system',
                    'Unclear'],
                    index=3,
                    help='Details on Question 2')

if pruning == 'Natural pruning system':
    stem = st.radio('What form is this tree?',
                        ['Single-stem',
                        'Multistem',
                        'Clump',
                        'Shrub',
                        'Unclear'],
                        index=4,
                    help='(generally initially trained to this form in the nursery)')
    if stem == 'Single-stem':
        tree_form = st.radio('Which training system is used?',
                            ['Managed - central leader form',
                             'Managed - other system',
                            'Unmanaged',
                            'Unclear'],
                            index=3,
                            help='Details on Question 5')

    branched = st.radio('Is the tree high-branched or low-branched?',
                        ['Low-branched',
                        'High-branched',
                        'Unclear'],
                        index=2,
                        help='Details on Question 4')
elif pruning == 'Topiary pruning system':
    hedge = st.radio('Is tree managed as hedge or individual specimen?',
                            ['Hedge',
                             'Individual',
                            'Unclear'],
                            index=2)
elif pruning == 'Specialty pruning system':
    specialty_pruning = st.radio('Which specialty pruning system is used?',
                        [' Pollarding',
                        ' Espalier (none currently present)',
                        'Pleeching (none currently present)',
                        'Unclear'],
                        index=3)

annotator = st.radio('Who is annotating?',
                        ['Courtney','Jake','Kayleigh'])

st.sidebar.markdown('## Annotation Progress')

st.sidebar.markdown('*458* of *1,702* trees annotated')
st.sidebar.progress((458/1702))
