import pandas as pd
import numpy as np
import streamlit as st
from Dropbox_Setup import *

st.set_page_config(layout="wide")
st.title('Golf Club Inventory System')

dbx = initializeToken(st.secrets.dropbox.access)

barcodes = fromDBX(dbx,st.secrets.filepath.barcode)
clubID = fromDBX(dbx,st.secrets.filepath.clubID)

add,data,save = st.tabs(['Add, adjust, or check a club by barcode and serial code','Review Data','Save Data'])

def displaydataframe(dataframe:pd.DataFrame,rows = 1000):
  data.write(f'There are a total of {dataframe.shape[0]} results. Maximum of {rows} results on this page.')
  with data.container():
    c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = data.columns([1,2,2,2,2,2,2,2,2,2])
    c1.write('#')
    c2.write('Serial Code')
    c3.write('Barcode')
    c4.write('Status')
    c5.write('Brand')
    c6.write('Type')
    c7.write('Number')
    c8.write('Handedness')
    c9.write('Shaft Flex')
    c10.write('Specifics')
  row = 0
  for index in dataframe.index.tolist():
    if row < rows:
      with data.container():
        c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = data.columns([1,2,2,2,2,2,2,2,2,2])
        c1.write(str(index))
        c2.write(dataframe['Serial Code'][index])
        c3.write(dataframe['Barcode'][index])
        c4.write(dataframe['Status'][index])
        c5.write(dataframe['Brand'][index])
        c6.write(dataframe['Club Type'][index])
        c7.write(dataframe['Number'][index])
        c8.write(dataframe['Hand'][index])
        c9.write(dataframe['Shaft Flex'][index])
        c10.write(dataframe['Specifics'][index])
        row +=1
    elif row >= rows:
      break
      

col1,col2 = add.columns(2)
barcode = col1.text_input('Enter Barcode Number','',key = 'Barcode')
if barcode in barcodes['Barcode']:
  pos = barcodes['Barcode'].index(barcode)
  add.write(f"""
  Barcode: {barcode}. \n
  Brand: {barcodes['Brand'][pos]}. \n
  Club Type: {barcodes['Number'][pos]} {barcodes['Club Type'][pos]}. \n
  Specifics: {barcodes['Hand'][pos]} {barcodes['Shaft Flex'][pos]} {barcodes['Specifics'][pos]}""")
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
      st.experimental_rerun()
elif barcode == '':
  pass
else:
  add.write(f'Barcode, {barcode}, is not in the system:')
  brand = add.selectbox('Please select club brand:',['Callaway','Titleist','Taylor Made','Top Flight','Tommy Armour','Ping','Cobra','Adams','Other'],key = 'Brand')
  if brand == 'Other':
    brand = add.text_input('Please Enter Unlisted Brand Name:','',key='Other Brand')
  type_ = add.selectbox('Please select club type:',['Driver','Wood','Iron','Wedge','Putter'],key = 'Club Type')
  number = add.text_input('Please enter club number (ex: enter 7 for 7 Iron or 56 for 56 degree wedge):','', key = 'club number')
  hand = add.selectbox('Please select handedness:',['Right Hand','Left Hand'],key = 'hand')
  flex = add.selectbox('Please select the flex of the shaft:',['Regular','Stiff','Extra','Senior','Ladies'],key = 'felx')
  specifics = add.text_input('Please type specifics about the club:','',key = 'specifics')
  submit = add.button('Submit')
  if submit:
    barcodes['Barcode'].append(barcode)
    barcodes['Brand'].append(brand)
    barcodes['Club Type'].append(type_)
    barcodes['Specifics'].append(specifics)
    barcodes['Number'].append(number)
    barcodes['Hand'].append(hand)
    barcodes['Shaft Flex'].append(flex)
    toDBX(dbx,barcodes,st.secrets.filepath.barcode)
    add.write(f'New barcode has been added to the system')
    st.experimental_rerun()

action2 = data.selectbox('Would you like to:',['Review all clubs data','Search for clubs by barcode','Search for clubs by description','Search by club Serial Code','Delete a club from the system'],key = 'action2')
if action2 == 'Review all clubs data':
  displaydataframe(pd.merge(pd.DataFrame(clubID),pd.DataFrame(barcodes)))
elif action2 == 'Search for clubs by barcode':
  barcodedata = data.text_input('Enter Barcode:','',key = 'bc')
  SUBmit = data.button('Submit',key = 'by barcode')
  if SUBmit:
    if barcodedata == '':
      data.warning('Enter a valid barcode')
    elif barcodedata != '' and not(str(barcodedata) in barcodes['Barcode']):
      data.warning('This barcode is not in the system. Select the add club action to be able to collect data on this club.')
    elif str(barcodedata) in barcodes['Barcode']:
      df = pd.DataFrame(clubID)
      displaydata = df[df['Barcode'] == str(barcodedata)]
      displaydataframe(pd.merge(df,pd.DataFrame(barcodes)))
elif action2 == 'Search for clubs by description':
  data.write('Please refine down to your search criteria. Anything left blank will not be filtered.')
  cbrand = data.selectbox('Please select club brand:',['All','Callaway','Titleist','Taylor Made','Top Flight','Tommy Armour','Ping','Cobra','Adams','Other'],key = 'cBrand')
  if cbrand == 'Other':
    cbrand = data.text_input('Please Enter Unlisted Brand Name:','',key='cOther Brand')
  ctype_ = data.selectbox('Please select club type:',['All','Driver','Wood','Iron','Wedge','Putter'],key = 'cClub Type')
  cnumber = data.text_input('Please enter club number (ex: enter 7 for 7 Iron or 56 for 56 degree wedge):','', key = 'cclub number')
  chand = data.selectbox('Please select club handedness:',['All','Right Hand','Left Hand'],key = 'handc')
  cflex = data.selectbox('Please select shaft flex:',['All','Regular','Stiff','Extra','Senior','Ladies'],key = 'cflex')
  cstatus = data.selectbox('Please select club status:',['All','In Stock','Sold','Stolen','Return In Stock'],key = 'cstatus')
  dc1,dc2 = data.columns([7,1])
  dc1.write('')
  rows = dc2.selectbox('How many results',[10,25,50,100])
  csubmit = data.button('Submit',key = 'csubmitbutton')
  if csubmit:
    displaydata = pd.DataFrame(barcodes)
    df2 = pd.DataFrame(clubID)
    if cbrand != 'All':
      displaydata = displaydata[displaydata['Brand'] == cbrand]
    if ctype_ != 'All':
      displaydata = displaydata[displaydata['Club Type'] == ctype_]
    if chand != 'All':
      displaydata = displaydata[displaydata['Hand'] == chand]
    if cflex != 'All':
      displaydata = displaydata[displaydata['Shaft Flex'] == cflex]
    if cstatus != 'All':
      df2 = df2[df2['Status'] == cstatus]
    if cnumber != '':
      displaydata = displaydata[displaydata['Number'] == str(cnumber)]
    displaydata = pd.merge(df2,displaydata)
    if displaydata.empty == True:
      data.warning('There are no clubs that fit this criteria')
    else:
      displaydataframe(displaydata,rows)
elif action2 == 'Search by club Serial Code':
  serialnumber = data.text_input('Enter serial number:','',key = 'serialnumber')
  if data.button('Submit',key = 'submitrefine'):
    displaydata = pd.DataFrame(clubID)
    displaydata = df[df['Serial Code'] == str(serialnumber)]
    if displaydata.empty == True:
      data.warning('There are no clubs that fit this criteria')
    else:
      displaydataframe(pd.merge(displaydata,pd.DataFrame(barcodes)))
elif action2 == 'Delete a club from the system':
  removeclubbarcode = data.text_input('Enter the barcode for the club you would like to delete','',key = 'remove1')
  removeclubID = data.text_input('Enter the serial number for the club you would like to delete','',key = 'remove2')
  df = pd.DataFrame(clubID)
  df = df[df['Barcode'] == removeclubbarcode]
  df = df[df['Serial Code'] == removeclubID]
  if not(df.empty) and df.shape[0] == 1:
    removedf = pd.DataFrame(clubID)
    if data.button('Confirm club removal',key = 'removeclub'):
      removedf.drop(df.index[0],inplace = True)
      a = removedf['Serial Code'].values.tolist()
      b = removedf['Barcode'].values.tolist()
      c = removedf['Status'].values.tolist()
      club = {'Serial Code':a,'Barcode':b,'Status':c}
      toDBX(dbx,club,st.secrets.filepath.clubID)
      data.write('Club has been removed from the system')
      st.experimental_rerun()
      
savedata = save.button('Save full dataset in data storage',key = 'savedata')
if savedata:
  toDBX(dbx,pd.merge(pd.DataFrame(clubID),pd.DataFrame(barcodes)).to_dict(),st.secrets.filepath.saveFile)
  save.write('File has been saved to local data storage.')

  
datareset = '''
toDBX(dbx,{'Barcode':[],'Brand':[],'Club Type':[],'Number':[],'Hand':[],'Shaft Flex':[],'Specifics':[]},st.secrets.filepath.barcode)
toDBX(dbx,{'Serial Code':[],'Barcode':[],'Status':[]},st.secrets.filepath.clubID)
'''
