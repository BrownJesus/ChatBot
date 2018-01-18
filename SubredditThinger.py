readFile  = "RC_2009-03"
writeFile = "RC_2009-03_Republican.txt"

def main():
    fileOpen  = open(readFile, 'r')
    fileWrite = open(writeFile, 'w')

    lines    = fileOpen.readlines()
    comments = {}

    for line in lines:
        if line.find("\"subreddit\":\"politics\"") != -1: # In politics subreddit
            # fileWrite.write(findScore(line))
            fileWrite.write(findBody(line))
        else:
            continue

    fileOpen.close()
    fileWrite.close()

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
