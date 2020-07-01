"""Simple script to determine files with odd number of calibration levels for internal investigation
of old data

Searches through all CSV files in a folder of the instrument output format and builds a list of the ones with
unusual number of calibration levels"""

import os, csv, re

directory = '/run/media/orthogonalstar/22A4-D43B/Raw/'
oddFiles = []

for filename in os.listdir(directory):
    if filename.endswith('.csv') and not re.search('a7', filename, re.IGNORECASE):
        filePath = os.path.join(directory, filename)
        calLim = 4
        time = None
        if re.search('t', filename, re.IGNORECASE):
            calLim = 6
        with open(filePath) as f:
            reader = csv.reader(f)
            data = list(reader)

            calLevels = []
            for row in range(0, len(data)):
                if re.search('^\d$', data[row][6]):
                    calLevels.append(int(data[row][6]))
                    time = data[row][4]
            if len(calLevels) > 0:
                max = calLevels[0]
                for i in range(1, len(calLevels)):
                    if calLevels[i] > max:
                        max = calLevels[i]
            else:
                max = 0

            totalLevels = max

        if totalLevels > calLim:
            oddFiles.append([filename, totalLevels, time])

files = open('oddFiles.csv', 'w')
myWriter = csv.writer(files, delimiter=',')
myWriter.writerow(['File Names', '#Cal lvl', 'EPT'])
for file in oddFiles:
    myWriter.writerow(file)