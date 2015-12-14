

def convertData_and_Save(fhandler, annfinal):

    for row in annfinal:
        fhandler.write( str(row[0]) + ' \'' + row[1]  + '\' \'' + row[2] + '\'\n')
