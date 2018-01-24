import string

def main():
    maxFileNumber = 8
    republicanFile = "RC_2017-11_Republican_TD.txt"
    democratFile = "RC_2017-11_Democrat_TD.txt"

    MINIMUM_SCORE = 20
    
    democratFile   = open(democratFile, 'w')                    # Open both files to write TD to
    republicanFile = open(republicanFile, 'w')
    
    for fileNumber in range(0, maxFileNumber + 1):              # Opens all 8 files in order to get data from
        inputFile      = open("outputFile%d.txt" % fileNumber , 'r')

        lines          = inputFile.readlines()                  # Reads all the lines at once to avoid accessing file too often
        comments       = {}                                     # because accessing files from the drive is slower than ram
        dataFound1     = 0
        dataFound2     = 0

        for line in lines:
            if line.find("\"subreddit\":\"democrats\"") != -1:       # In democratic subreddit
                score = findScore(line)
                if int(score) > MINIMUM_SCORE:                      # Checks for minimum score
                    dataFound1 += 1
                    body = formatLine(findBody(line))               # Gets and formats the comment
                    democratFile.write(body)
            elif line.find("\"subreddit\":\"Republican\"") != -1:   # In republican subreddit
                score = findScore(line)
                if int(score) > MINIMUM_SCORE:                      # Checks for minimum score
                    dataFound2 += 1
                    body = formatLine(findBody(line))               # Gets and formats body
                    republicanFile.write(body)
            else:
                continue
        inputFile.close()
        print("Finished outputFile%d with %d D and %d R data points" % (fileNumber, dataFound1, dataFound2))
    democratFile.close()
    republicanFile.close()

def formatLine(line):
    while line.find("\\t") != -1:
        pos = line.find("\\t")
        line = line.replace(line[pos:pos+2], "")
    while line.find("\\n") != -1:
        pos = line.find("\\n")
        line = line.replace(line[pos:pos+2], "")
    while line.find("\\\\") != -1:
        pos = line.find("\\\\")
        line = line.replace(line[pos:pos+2], "")
    while line.find("\\\"") != -1:
        pos = line.find("\\\"")
        line = line.replace(line[pos:pos+2], "")
    while line.find("\\u") != -1:
        pos = line.find("\\u")
        line = line.replace(line[pos:pos+6], "")
    while line.find("\\r") != -1:
        pos = line.find("\\r")
        line = line.replace(line[pos:pos+2], "")
    while line.find("[deleted]") != -1:
        pos = line.find("[deleted]")
        line = line.replace(line[pos:pos+9], "")
    return line
        

# Takes in a line and returns the value to write to the file
def findScore(line):
    scoreStartPos = line.find("\"score\":") + 8   # Skips past '"score":'
    scoreEndPos = scoreStartPos + 5 if scoreStartPos + 5 < len(line) else len(line)              
    for i in range(scoreStartPos, scoreStartPos+5):
        if line[i] == ',' or line[i] == '}':      # Reach the end of the number
            scoreEndPos = i
            break
    return line[scoreStartPos:scoreEndPos] + '\n'

# Takes in a line and returns the comment to write
def findBody(line):
    bodyStartPos = line.find("\"body\":") + 8
    bodyEndPos = 0
    subStr = line[bodyStartPos:len(line)]
    bodyEndPos = bodyStartPos + subStr.find("\",\"")
        
    return line[bodyStartPos:bodyEndPos] + '\n\n'
    
main()
