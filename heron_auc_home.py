import pandas as pd
import io
import streamlit as st
import plotly.express as px
import re
import numpy as np
import math

st.title('Heron with Streamlit')

st.link_button("Return to Heron Home", "https://herondata.app")

# create separate excel sheets based on galnac
def parseSialicAcidFromString(proteinNameString):
    if re.search('^SA[0-9]', proteinNameString):
        return re.split('^SA[0-9]', proteinNameString, 1)[1]
    return proteinNameString

#upload file
uploaded_file = st.file_uploader("Choose a CSV")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

# begin grouping proteins by galnac numbers
    listOfGalNacs = df.to_dict('records')
    groupedSheetsByGalNac = {}
    memoizedUniqueFullProteinNameList = []


    for row in listOfGalNacs:
      dictForDataframe = {}
      proteinName = row["Protein Name"]

      dictForDataframe["Peptide"] = proteinName
      dictForDataframe["Replicate"] = row["Replicate Name"]
      if math.isnan(row["Total Area"]):
          
        dictForDataframe["Total Area"] = 0
     
      dictForDataframe["Total Area"] = row["Total Area"]
            
      parsedProteinName = parseSialicAcidFromString(proteinName)

      # add to sheet
      if parsedProteinName in groupedSheetsByGalNac.keys():
          groupedSheetsByGalNac[parsedProteinName] += [dictForDataframe]
      else: 
          groupedSheetsByGalNac[parsedProteinName] = []
          groupedSheetsByGalNac[parsedProteinName]  += [dictForDataframe]

 
   
    buffer = io.BytesIO()
  

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
          for k, v in groupedSheetsByGalNac.items():
              ddff = pd.DataFrame(v)
              dfff = pd.pivot_table(ddff, index=["Peptide"], columns=["Replicate"], aggfunc="sum", fill_value=0)

              dfff.to_excel(writer, sheet_name=k)
         



    st.download_button(
            label="Download",
            data=buffer,
            file_name="single-sheet.xlsx",
            mime="application/vnd.ms-excel"
        )

