import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.title('Golf Club Inventory System')

dbx = initializeToken(st.secrets.dropbox.access)

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)

action = st.selectbox('Select action:',['Add, adjust, or check a club by barcode and serial code','Review Data','Reset Data'],key = 'action')

if action == 'Add, adjust, or check a club by barcode and serial code':
  col1,col2 = st.columns(2)
  barcode = col1.text_input('Enter Barcode Number','',key = 'Barcode')
  if barcode in barcodes['Barcode']:
    pos = barcodes['Barcode'].index(barcode)
    st.write(f"""
    Barcode: {barcode}. \n
    Brand: {barcodes['Brand'][pos]}. \n
    Club Type: {barcodes['Number'][pos]} {barcodes['Club Type'][pos]}. \n
    Specifics: {barcodes['Specifics'][pos]}""")
    club = col2.text_input('Enter Club ID Number','',key = 'ClubID')
    if club in clubID['Serial Code']:
      ID = pd.DataFrame(clubID)
      ID = ID[ID['Barcode'] == str(barcode)]
      ID = ID[ID['Serial Code'] == str(club)]
      if ID.empty == True:
        barcodeMatch = -1
      else:
        barcodeMatch = ID.index.tolist()[0]
    else:
      barcodeMatch = -1
    if club in clubID['Serial Code'] and barcodeMatch != -1:
      st.write(f"This club is in the system as status: {clubID['Status'][barcodeMatch]}")
      changeStatus = st.selectbox('Select New Status for selected club:',['Sold','In Stock','Stolen','Return In Stock'])
      change = st.button('Confirm Status Change',key = 'Status Change')
      if change:
        clubID['Status'][barcodeMatch] = changeStatus
        toDBX(dbx,clubID,st.secrets.filepath.clubID)
        st.write(f'Club {club} status has been changed to {changeStatus}.')
    elif club == "":
      pass
    else:
      st.write(f'Club, {club}, with barcode {barcode} is not in the system.')
      confirm = st.button('Confirm New Club Barcode and Club ID then submit to add club to system.',key = 'newclub')
      if confirm:
        clubID['Serial Code'].append(club)
        clubID['Barcode'].append(barcode)
        clubID['Status'].append('In Stock')
        toDBX(dbx,clubID,st.secrets.filepath.clubID)
        st.write(f'New club {club} has been added to the system')
  elif barcode == '':
    pass
  else:
    st.write(f'Barcode, {barcode}, is not in the system:')
    with st.form('New Barcode'):
      brand = st.selectbox('Please select club brand:',['Callaway','Titleist','Taylor Made','Top Flight','Ping','Cobra','Adams','Other'],key = 'Brand')
      if brand == 'Other':
        brand = st.text_input('Please Enter Unlisted Brand Name:','',key='Other Brand')
      type_ = st.selectbox('Please select club type:',['Driver','Wood','Iron','Wedge','Putter'],key = 'Club Type')
      number = st.text_entry('Please enter club number (ex: enter 7 for 7 Iron or 56 for 56 degree wedge):','', key = 'club number')
      specifics = st.text_input('Please type specifics about the club:','',key = 'specifics')
      submit = st.form_submit_button('Submit')
    if submit:
      barcodes['Barcode'].append(barcode)
      barcodes['Brand'].append(brand)
      barcodes['Club Type'].append(type_)
      barcodes['Specifics'].append(specifics)
      barcodes['Number'].append(number)
      toDBX(dbx,barcodes,st.secrets.filepath.barcode)
      st.write(f'New barcode has been added to the system')
elif action == 'Reset Data':
  reset = st.button('Press to confirm data reset.')
  if reset:
    toDBX(dbx,{'Barcode':[],'Brand':[],'Club Type':[],'Number':[],'Specifics':[]},st.secrets.filepath.barcode)
    toDBX(dbx,{'Serial Code':[],'Barcode':[],'Status':[]},st.secrets.filepath.clubID)
elif action == 'Review Data':
  df1 = pd.DataFrame(clubID)
  df2 = pd.DataFrame(barcodes)
  df = pd.merge(df1,df2)
  action2 = st.selectbox('Would you like to:',['Review all clubs data','Review data for a particular club type by barcode','Review data for a particular club type by description'],key = 'action2')
  if action2 == 'Review all clubs data':
    st.dataframe(df)
  elif action2 == 'Review data for a particular club type by barcode':
    barcodedata = st.text_entry('Enter Barcode:','',key = 'bc')
    if barcodedata != '':
      pass
    elif barcodedata != '' and not(str(barcodedata) in barcodes['Barcode']):
      st.warning('This barcode is not in the system. Select the add club action to be able to collect data on this club.')
    elif str(barcodedata) in barcodes['Barcode']:
      displaydata = df[df['Barcode'] == str(barcode)]
      st.dataframe(displaydata)
  elif action2 == 'Review data for a particular club type by description':
    clubbrand = st.selectbox('Please select club brand:',['Callaway','Titleist','Taylor Made','Top Flight','Ping','Cobra','Adams','Other'],key = 'clubBrand')
    if clubbrand == 'Other':
      clubbrand = st.text_input('Please Enter Unlisted Brand Name:','',key='clubOther Brand')
      
      
