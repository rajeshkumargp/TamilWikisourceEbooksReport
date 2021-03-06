# -*- coding: utf-8 -*-
import sqlite3
import wget

sqlite_file_Url  = "http://tools.wmflabs.org/wsexport/logs.sqlite"
sqlite_file = wget.download(sqlite_file_Url) 

#sqlite_file = 'logs.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

query = "SELECT TITLE,FORMAT,COUNT(*) as DWDCNT FROM CREATION where lang='ta' GROUP BY TITLE,FORMAT  ;"


outfile= open("report.csv","w")

aBookDetail = {}

allFormats = ["atom","epub","epub-2","epub-3","htmlz","mobi","odt","pdf",
            "pdf-a4","pdf-a5","pdf-a6","pdf-letter","rtf","txt","xhtml"]

aBookDetail["title"] = None
aCSVLine = "Title"
for aFormat in allFormats:
    aBookDetail[aFormat] = 0

aCSVLine = aCSVLine + ',' + ','.join([ aform 
                   for aform in allFormats]) + "\n"

outfile.write(aCSVLine)

c.execute(query)

ReportList = c.fetchall()
conn.close()

i = 1

for aline in ReportList: 
    booktitle,bookformat,bookcount = aline
    booktitle = booktitle.replace(",","")
    # Reading Very First Line and populating Dictionary
    if aBookDetail["title"] == None :
       
       aBookDetail["title"] = booktitle
       aBookDetail[bookformat] = bookcount
    #Reading Same book detail and populating Dictionary  
    elif aBookDetail["title"] ==  booktitle :
       aBookDetail[bookformat] = bookcount
    #Reading Differnt Book,Processing Dict Contents and Write to File
    else:
       aCSVLine = aBookDetail["title"]
       aCSVLine = aCSVLine + ',' + ','.join([ str(aBookDetail[aform]) 
                   for aform in allFormats]) + "\n"
       # Write to a File
       #print(aCSVLine.encode('utf-8'))
       outfile.write(str(aCSVLine.encode('utf-8'))) 

       for aFormat in allFormats:
           aBookDetail[aFormat] = 0 
       aBookDetail["title"] = booktitle
       aBookDetail[bookformat] = bookcount
  
aCSVLine = aBookDetail["title"]
aCSVLine = aCSVLine +',' + ','.join([str(aBookDetail[aform]) 
             for aform in allFormats])+"\n"

# Writing Last Book Details
#print(aCSVLine)
outfile.write(str(aCSVLine.encode('utf-8')))
outfile.close()
