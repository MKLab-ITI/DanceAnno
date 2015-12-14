

def convertData_and_Save(fhandler, anns, Fs):


    temp_svl = '\
<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE sonic-visualiser>\n\
<sv>\n\
  <data>\n\
    <model id="3" name="description" sampleRate="Fs_pos" start="start_pos" end="end_pos" type="sparse" dimensions="1" resolution="1" notifyOnAdd="true" dataset="2" />\n\
    <dataset id="2" dimensions="1">\n\
TEMP_POS\
    </dataset>\n\
  </data>\n\
  <display>\n\
    <layer id="1" type="timeinstants" name="Time Instants &lt;2&gt;" model="3"  plotStyle="0" colourName="Orange" colour="#ff9632" darkBackground="false" />\n\
  </display>\n\
</sv>'

    temp_svl = temp_svl.replace('Fs_pos',str(Fs))
    temp_svl = temp_svl.replace("start_pos",str(anns[0][0]))
    temp_svl = temp_svl.replace("end_pos",str(anns[-1][0]))

    all_data = ''
    for i in range(len(anns)):
        all_data = all_data + '\t\t<point frame="'+ str(anns[i][0]) +'" label="'+ anns[i][1] + '" />\n'

    temp_svl = temp_svl.replace("TEMP_POS",all_data)
    fhandler.write(temp_svl)
    return