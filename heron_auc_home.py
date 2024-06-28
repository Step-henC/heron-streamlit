import pandas as pd
import io
import streamlit as st
import re
import math

st.title('Heron Data with Streamlit')
st.logo("https://www.herondata.app/static/media/heronLogo.f08c51755ccf14a6b90f.jpg", link="https://herondata.app", icon_image=None)


st.link_button("Return to Heron Home", "https://herondata.app")

# create separate excel sheets based on galnac
def parseSialicAcidFromString(proteinNameString):
    if re.search('^SA[0-9]', proteinNameString):
        return re.split('^SA[0-9]', proteinNameString, 1)[1]
    return proteinNameString

#upload file
uploaded_file = st.file_uploader("Choose a CSV")
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, encoding_errors="ignore")
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
              dfRaw = pd.DataFrame(v)
              dfPivot = pd.pivot_table(dfRaw, index=["Peptide"], values="Total Area", columns=["Replicate"], aggfunc="sum", fill_value=0, margins=True, margins_name="Summed Total Area")
              max_rows = dfPivot.shape[0]
              max_cols = dfPivot.shape[1]

              # cannot "apply" to dfpivot cuz marings Sum column washes out percentages
              dfPercentages = pd.pivot_table(dfRaw, index=["Peptide"], values="Total Area", columns=["Replicate"], aggfunc="sum", fill_value=0).apply(lambda x: x*100/sum(x))

              dfAvgOfPercentages = dfPercentages.T.groupby(lambda x: re.split('_\\d$', x)[0]).mean().T
              dfAvgOfPercentagesRowStart = max_rows+max_rows+10
              avgTableColCount = dfAvgOfPercentages.shape[1]

              dfPivot.to_excel(writer, sheet_name=k)
              dfPercentages.to_excel(writer, sheet_name=k, startrow=max_rows+5, startcol=0)
              dfAvgOfPercentages.to_excel(writer, sheet_name=k, startrow=max_rows+max_rows+10)
             

              worksheet = writer.sheets[k]
              workbook = writer.book

              worksheet.write(max_rows+4, 0, "Percent Relative Abundance (area/total area for peaks considered * 100)")
              worksheet.write(max_rows+max_rows+9,0, "Replicate Average % Relative Abundance")

              colValIterator = 1
              for series_name, _ in dfAvgOfPercentages.items():
                  
                chart = workbook.add_chart({'type': 'pie'})

                chart.add_series({
                  "name": series_name,
                  "categories": [k, dfAvgOfPercentagesRowStart+1, 0, dfAvgOfPercentagesRowStart+max_rows-1, 0],
                  "values": [k, dfAvgOfPercentagesRowStart+1, colValIterator, dfAvgOfPercentagesRowStart+max_rows-1, colValIterator],
              })

                worksheet.insert_chart("H"+str(colValIterator+5), chart)
                colValIterator += 1
         



    st.download_button(
            label="Download",
            data=buffer,
            file_name="single-sheet.xlsx",
            mime="application/vnd.ms-excel",
        )


st.image("https://www.herondata.app/static/media/heronLogo.f08c51755ccf14a6b90f.jpg", caption=None)
