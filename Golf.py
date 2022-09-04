import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.title('Dicks Sporting Goods Golf Department')

dbx = initializeToken(st.secrets.dropbox.access)

toDBX(dbx,st.secrets.filepath.barcode,{'Barcode':[],
                          'Brand':[],
                          'Club Type':[],
                          'Specifics':[]})
toDBX(dbx,st.secrets.filepath.clubID,{'Serial Code':[],
                                     'Barcode':[],
                                     'Status':[]})

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)
