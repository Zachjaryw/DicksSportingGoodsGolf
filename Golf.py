import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.set_page_config(layout="wide")
st.title('Golf Club Inventory System')

dbx = initializeToken(st.secrets.dropbox.access)

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)

add,data,reset = st.tabs(['Add, adjust, or check a club by barcode and serial code','Review Data','Reset Data'])

def displaydataframe(dataframe:pd.DataFrame):
  with data.container():
    c1,c2,c3,c4,c5,c6,c7,c8 = data.columns([1,2,2,2,2,2,2,4])
    c1.write('#')
    c2.write('Serial Code')
    c3.write('Barcode')
    c4.write('Status')
    c5.write('Brand')
    c6.write('Type')
    c7.write('Number')
    c8.write('Specifics')
  for index in dataframe.index.tolist():
    with data.container():
      c1,c2,c3,c4,c5,c6,c7,c8 = data.columns([1,2,2,2,2,2,2,4])
      c1.write(str(index))
      c2.write(dataframe['Serial Code'][index])
      c3.write(dataframe['Barcode'][index])
      c4.write(dataframe['Status'][index])
      c5.write(dataframe['Brand'][index])
      c6.write(dataframe['Club Type'][index])
      c7.write(dataframe['Number'][index])
      c8.write(dataframe['Specifics'][index])

col1,col2 = add.columns(2)
barcode = col1.text_input('Enter Barcode Number','',key = 'Barcode')
if barcode in barcodes['Barcode']:
  pos = barcodes['Barcode'].index(barcode)
  add.write(f"""
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
    add.write(f"This club is in the system as status: {clubID['Status'][barcodeMatch]}")
    changeStatus = add.selectbox('Select New Status for selected club:',['Sold','In Stock','Stolen','Return In Stock'])
    change = add.button('Confirm Status Change',key = 'Status Change')
    if change:
      clubID['Status'][barcodeMatch] = changeStatus
      toDBX(dbx,clubID,st.secrets.filepath.clubID)
      add.write(f'Club {club} status has been changed to {changeStatus}.')
  elif club == "":
    pass
  else:
    add.write(f'Club, {club}, with barcode {barcode} is not in the system.')
    confirm = add.button('Confirm New Club Barcode and Club ID then submit to add club to system.',key = 'newclub')
    if confirm:
      clubID['Serial Code'].append(club)
      clubID['Barcode'].append(barcode)
      clubID['Status'].append('In Stock')
      toDBX(dbx,clubID,st.secrets.filepath.clubID)
      add.write(f'New club {club} has been added to the system')
      add.experimental_rerun()
elif barcode == '':
  pass
else:
  add.write(f'Barcode, {barcode}, is not in the system:')
  with add.form('New Barcode'):
    brand = add.selectbox('Please select club brand:',['Callaway','Titleist','Taylor Made','Top Flight','Ping','Cobra','Adams','Other'],key = 'Brand')
    if brand == 'Other':
      brand = add.text_input('Please Enter Unlisted Brand Name:','',key='Other Brand')
    type_ = add.selectbox('Please select club type:',['Driver','Wood','Iron','Wedge','Putter'],key = 'Club Type')
    number = add.text_input('Please enter club number (ex: enter 7 for 7 Iron or 56 for 56 degree wedge):','', key = 'club number')
    specifics = add.text_input('Please type specifics about the club:','',key = 'specifics')
    submit = add.form_submit_button('Submit')
  if submit:
    barcodes['Barcode'].append(barcode)
    barcodes['Brand'].append(brand)
    barcodes['Club Type'].append(type_)
    barcodes['Specifics'].append(specifics)
    barcodes['Number'].append(number)
    toDBX(dbx,barcodes,st.secrets.filepath.barcode)
    add.write(f'New barcode has been added to the system')
    add.experimental_rerun()

reset = reset.button('Press to confirm data reset.')
if reset:
  toDBX(dbx,{'Barcode':[],'Brand':[],'Club Type':[],'Number':[],'Specifics':[]},st.secrets.filepath.barcode)
  toDBX(dbx,{'Serial Code':[],'Barcode':[],'Status':[]},st.secrets.filepath.clubID)

df1 = pd.DataFrame(clubID)
df2 = pd.DataFrame(barcodes)
df = pd.merge(df1,df2)
action2 = data.selectbox('Would you like to:',['Review all clubs data','Search for clubs by barcode','Search for clubs by description','Search by club Serial Code'],key = 'action2')
if action2 == 'Review all clubs data':
  displaydataframe(df)
elif action2 == 'Search for clubs by barcode':
  barcodedata = data.text_input('Enter Barcode:','',key = 'bc')
  SUBmit = data.button('Submit',key = 'by barcode')
  if SUBmit:
    if barcodedata == '':
      data.warning('Enter a valid barcode')
    elif barcodedata != '' and not(str(barcodedata) in barcodes['Barcode']):
      data.warning('This barcode is not in the system. Select the add club action to be able to collect data on this club.')
    elif str(barcodedata) in barcodes['Barcode']:
      displaydata = df[df['Barcode'] == str(barcodedata)]
      displaydataframe(displaydata)
elif action2 == 'Search for clubs by description':
  with data.form('New Barcode'):
    data.write('Please refine down to your search criteria. Anything left blank will not be filtered.')
    cbrand = data.selectbox('Please select club brand:',['All','Callaway','Titleist','Taylor Made','Top Flight','Ping','Cobra','Adams','Other'],key = 'cBrand')
    if cbrand == 'Other':
      cbrand = data.text_input('Please Enter Unlisted Brand Name:','',key='cOther Brand')
    ctype_ = data.selectbox('Please select club type:',['All','Driver','Wood','Iron','Wedge','Putter'],key = 'cClub Type')
    cnumber = data.text_input('Please enter club number (ex: enter 7 for 7 Iron or 56 for 56 degree wedge):','', key = 'cclub number')
    csubmit = data.form_submit_button('Submit')
  if csubmit:
    displaydata = df.copy()
    if cbrand != 'All':
      displaydata = displaydata[displaydata['Brand'] == cbrand]
    if ctype_ != 'All':
      displaydata = displaydata[displaydata['Club Type'] == ctype_]
    if cnumber != '':
      displaydata = displaydata[displaydata['Number'] == str(cnumber)]
    if displaydata.empty == True:
      data.warning('There are no clubs that fit this criteria')
    else:
      displaydataframe(displaydata)
elif action2 == 'Search by club Serial Code':
  serialnumber = data.text_input('Enter serial number:','',key = 'serialnumber')
  if data.button('Submit',key = 'submitrefine'):
    displaydata = df[df['Serial Code'] == str(serialnumber)]
    if displaydata.empty == True:
      data.warning('There are no clubs that fit this criteria')
    else:
      displaydataframe(displaydata)

