from BeautifulSoup import BeautifulSoup
import urllib2

weblink = "http://www.cs.hioa.no/~haugerud/disk/"
checker = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ"
setLetter = ord('A')
setNumber = 0
frames = []
RScript = open("RstudioScript.txt", 'w')

def crawl(weblink, depth):
    global setLetter
    global setNumber
    global frames
    frameFragment = []
    depth += 1
    pageOfFiles = urllib2.urlopen(weblink)
    soup = BeautifulSoup(pageOfFiles)
    for link in soup.findAll('a'):
        if link.get('href')[0] in checker:
            if depth < 2:
                crawl(weblink + link.get('href'), depth)
            else:  
                frameFragment.append(chr(setLetter)+str(setNumber) + ',')              
                RScript.write(chr(setLetter)+str(setNumber) + '=scan("' + weblink + link.get('href') + '")' + '\n')
                setLetter += 1
                
               
    setLetter = ord('A')
    setNumber += 1 
    if frameFragment:
        frameFragment[-1] = frameFragment[-1].replace(",", "") 
        frames.append(frameFragment)

        
depth = 0
crawl(weblink, depth)
set = []
for fragment in frames:
    set.append('frame' + chr(setLetter))
    RScript.write( set[-1] + '=data.frame(' + ''.join(fragment) + ')\n')
    setLetter += 1

RScript.write('cor(' + set[0] + ',' + set[1] + ')\n')
    
