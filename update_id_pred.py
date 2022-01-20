# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import datetime

filename = '/home/titu/Public/2020/devops-plan-v4.csv'
outputFile = 'out.csv'

inputDateFormat = '%d/%m/%y'
outputDateFormat = '%d-%b-%Y'

def read_input_file(filename):
    
    header = []
    inputCsvList = []
    idDict = {}

    with open(filename) as fh:
        csvr = csv.reader(fh)
        header = next(csvr)
        
        id_index = header.index('ID')
        header[id_index] = 'Task ID'
        
        pred_index = header.index('Predecessors')
        rowCount = 0
        for row in csvr:
            #print(row)
            if row:
                rowCount += 1
                idDict[row[id_index]] = rowCount
                inputCsvList.append(row)
            else:
                break
    #print('header: ', header)        
    
    return (header, inputCsvList, idDict, id_index, pred_index)

def replace_id_pred(header, input_csv_list, id_dict, id_index, pred_index):
    
    #print('id dict: {}'.format(id_dict))
    #print('id_index = {}, pred_index = {}'.format(id_index, pred_index))
    
    outputCsvList = []
    for row in input_csv_list:
        #print('row: {}'.format(row))
        #print('id: {}, predId: {}'.format(row[id_index], row[pred_index]))
        newId = id_dict[row[id_index]]
        row[id_index] = newId
        
        if row[pred_index]:
            newPredId = id_dict[row[pred_index]]
            row[pred_index] = newPredId
        
        outputCsvList.append(row)
        
    return(outputCsvList)

def replace_date_fields(header, input_csv_list):
    
    startDateIndex = header.index('Begin date')
    endDateIndex = header.index('End date')
    #durationIndex = header.index('Duration')
    outputCsvList = []
    
    for row in input_csv_list:
        #print('OLD begin date: {}, end date: {}'.format(row[startDateIndex], row[endDateIndex]))
        oldStartDate = datetime.datetime.strptime(row[startDateIndex], inputDateFormat)
        newStartDate = oldStartDate.strftime(outputDateFormat)
        row[startDateIndex] = newStartDate
        
        oldEndDate = datetime.datetime.strptime(row[endDateIndex], inputDateFormat)
        newEndDate = oldEndDate.strftime(outputDateFormat)
        row[endDateIndex] = newEndDate
        #print('NEW begin date: {}, end date: {}'.format(row[startDateIndex], row[endDateIndex]))
        #print('duration: {}, rounded: {}, calc dur: {}, rounded: {}'.format(int(row[durationIndex])/5.0, round(int(row[durationIndex])/5.0, 0), (oldEndDate - oldStartDate).days/7.0, round(((oldEndDate - oldStartDate).days/7.0), 0)))
        outputCsvList.append(row)
        
    return outputCsvList

def write_to_csv(output_list, out_filename):
    
    with open(out_filename, 'w') as fh:
        csvw = csv.writer(fh)
        csvw.writerows(output_list)
        print('Output file created: {}'.format(out_filename))
    

def main():
    
    header, inputCsvList, idDict, idIndex, predIndex = read_input_file(filename)
    outputCsvList = replace_id_pred(header, inputCsvList, idDict, idIndex, predIndex)
    outputCsvList = replace_date_fields(header, outputCsvList)
    
    if outputCsvList:
        outputCsvList.insert(0, header)
        write_to_csv(outputCsvList, outputFile)
        
main()
