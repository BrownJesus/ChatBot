import string

readFile  = "RC_2009-03"
writeFile = "RC_2009-03_Republican.txt"

MINIMUM_SCORE = 5

def main():
    fileOpen  = open(readFile, 'r')
    fileWrite = open(writeFile, 'w')

    lines    = fileOpen.readlines()
    comments = {}

    dataFound = 0

    for line in lines:
        if line.find("\"subreddit\":\"politics\"") != -1: # In politics subreddit
            score = findScore(line)
            if int(score) > MINIMUM_SCORE:
                dataFound += 1
                body = formatLine(findBody(line))
                fileWrite.write(body)
        else:
            continue

    fileOpen.close()
    fileWrite.close()
    print(str(dataFound) + " valid comments with a score of more than " + str(MINIMUM_SCORE) + " found!")

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
