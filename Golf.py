import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.title('Dicks Sporting Goods Golf Department')

dbx = initializeToken(st.secrets.dropbox.access)

reinitialize = '''
toDBX(dbx,{'Barcode':[],'Brand':[],'Club Type':[],'Specifics':[]},st.secrets.filepath.barcode)
toDBX(dbx,{'Serial Code':[],'Barcode':[],'Status':[]},st.secrets.filepath.clubID)
'''

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)

col1,col2 = st.columns(2)
barcode = col1.text_input('Enter Barcode Number','',key = 'Barcode')

if barcode in barcodes['Barcode']:
  pos = barcodes['Barcode'].iloc[barcode]
  st.write(f"Barcode: {barcode}. Brand: {barcodes['Brand'][pos]}. Club Type: {barcodes['Club Type'][pos]}. Specifics: {barcodes['Specifics'][pos]}")
  club = col2.text_input('Enter Club ID Number','',key = 'ClubID')
  if club in clubID:
    ID = pd.DataFrame(clubID)
    ID = ID[ID['Barcode'] == barcode]
    ID = ID[ID['Serial Code'] == club]
    if ID.empty == True:
      barcodeMatch = -1
    else:
      barcodeMatch = ID.index.tolist()[0]
  else:
    barcodeMatch = -1
  if club in clubID and barcodeMatch != -1:
    st.write(f"This club is already in the system as: {barcodes['Brand'][pos]} {barcodes['Club Type'][pos] {barcodes['Specifics'][pos]}. Status: {clubID['Status'][barcodeMatch]]}")
    changeStatus = st.select_box('Select New Status for selected club:',['Sold','In Stock','Stolen','Return In Stock'])
    change = st.button('Confirm Status Change',key = 'Status Change')
    if change:
      clubID['Status'][barcodeMatch] = changeStatus
      toDBX(dbx,clubID,st.secrets.filepath.clubID)
       st.write(f'Club {club} status has been changed to {changeStatus}.')
  elif club == '':
    pass
  else:
    st.write(f'Club, {club), with barcode {barcode} is not in the system.')
    confirm = st.button('Confirm New Club Barcode and Club ID then submit to add club to system.',key = 'newclub')
    if confirm:
      clubID['Serial Code'].append(club)
      clubID['Barcode'].append(barcode)
      clubID['Status'].append('In Stock')
      toDBX(dbx,clubID,st.secrets.filepath.clubID)
      st.write(f'New club {clubID} has been added to the system')
elif barcode == '':
  pass
elif barcode == 'Display Data':
  df1 = pd.DataFrame(clubID)
  df2 = pd.DataFrame(barcodes)
  df = pd.merge(df1,df2)
  st.dataframe(df)
else:
  st.write(f'Barcode, {barcode}, is not in the system:')
  with st.form('New Barcode'):
    brand = st.select_box('Please select club brand:',['Callaway','Titelist','Taylor Made','Top Flight','Ping','Cobra','Adams'],key = 'Brand')
    type_ = st.select_box('Please select club type:',['Driver','Wood','Iron','Wedge','Putter'],key = 'Club Type')
    specifics = st.text_input('Please type specifics about the club:','',key = 'specifics')
    submit = st.form_submit_button('Submit')
  if submit:
    barcodes['Barcode'].append(barcode)
    barcodes['Brand'].append(brand)
    barcodes['Club Type'].append(type_)
    barcodes['Specifics'].append(specifics)
    toDBX(dbx,barcodes,st.secrets.filepath.barcodes)
    st.write(f'New barcode has been added to the system')
  
