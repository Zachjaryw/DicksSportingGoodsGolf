import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.title('Dicks Sporting Goods Golf Department')

dbx = initializeToken(st.secrets.dropbox.access)

toDBX(dbx,{'Barcode':[],'Brand':[],'Club Type':[],'Specifics':[]},st.secrets.filepath.barcode)
toDBX(dbx,{'Serial Code':[],'Barcode':[],'Status':[]},st.secrets.filepath.clubID)

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)

