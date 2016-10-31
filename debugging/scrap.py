import fileinput
import sys

class Formatter:
    #class can and should have instance variables
    

    def __init__(self, inputfile, inputLines):

        self.formatKeys = {".LW": 0, ".LM": 0, ".LS": 0, ".FT": "off"}
        self.filename = inputfile
        self.lines = []
        self.file_len = 0
        self.read_file()
        lineCount = 0
        

    def read_file(self):
        filelines = self.set_file_len()
        maxCharsPerLine = 0
        #print(filelines)
        #try:

            #with open(self.filename) as self.file:
        for line in filelines:#self.file:
            #print(line, end='')       
            if self.check_newline(line): # appends an empty string to the the line (the driver will print the newline). If true continues to the next iteration
                newPara = True
                continue
            cmd = self.get_args(line)
            if cmd != '0': 
                newPara = True
                self.set_args(line, cmd)
                continue

            #line = line.strip('\n')
            self.inParaFormat(line, maxCharsPerLine)

            
            # self.lines.append(line)
             
        # except FileNotFoundError:
        #     print("File not found")
        #     sys.exit(0)

    def get_lines(self):
        #returns formatted lines
        return self.lines

    def set_args(self, l, cmd):
        if "+" in l:
            tempLine = l.replace('+',' ') # using a templine, because I want to perserve the original line for subsequent if statements
            tempLine = tempLine.split()
            self.formatKeys[cmd] += int(tempLine[1])
            self.formatKeys[".FT"] = "on"

        elif "-" in l: #This block of code checks for if the arguments of LM are subtracting margin
            tempLine2 = l.replace('-',' ') # using a templine, because I want to perserve the original line for subsequent if statements
            tempLine2 = tempLine2.split()
            self.formatKeys[cmd] -= int(tempLine2[1])
            self.formatKeys[".FT"] = "on"

        else:
            l = l.split() #Put the line into an array split on spaces
            try: #This try will pass if the arguments are of type int
                self.formatKeys[cmd] = int(l[1]) #Add arguments from the line to the dictionary
                self.formatKeys[".FT"] = "on"

            except ValueError: #If this exception is caught, that means FT args have been set
                self.formatKeys[cmd] = l[1]

        print(self.formatKeys)

    def get_args(self,l):
        l = l.split()
        if ((".LW" in l) or (".LS" in l) or (".LM" in l) or (".FT" in l)) and len(l) == 2:
                return l[0]

        else:
            return '0'

    def check_newline(self,l):
        if l == '\n':
            self.lines.append('')
            #self.lines.append("FOUND A LINE THATS JUST A NEWLINE!!!!")
            return True

        else:
            return False    

    def set_file_len(self):
        idx = 0
        lineList = []
        try:

            with open(self.filename) as self.file:
                for line in self.file:
                    #print(line)
                    idx+=1
                    lineList.append(line)

                self.file_len = idx

            return lineList
        except FileNotFoundError:
            print("File not found")
            sys.exit(0)

    def inParaFormat(self, l, c):
        charCount = c

        l = l.split() # Turn the line into an array of words

        for word in l:
            charCount += len(word) + 1 

            if charCount > self.formatKeys[".LW"]:
                #ls_printer(self.formatKeys["LS"])
                charCount = self.lm_printer() #call this function to add appropriate line spacing after the newline, it returns the number of chars added
                self.lines.append('\n')
                self.lines.append(word)
                charCount += len(word) # Add the length of the word to the number of chars added by margin (Now the charCount should only account for the current word and the margin added)

            elif charCount == self.formatKeys[".LW"]:
                self.lines.append(' ')
                #ls_printer(formatKeys["LS"]) # Print out appropriate linespacing
                self.lm_printer() #call this function to add appropriate line spacing after the newline
                charCount = self.formatKeys[".LM"] #set the margin to the charcount because the margin is the only string on the line

            else:
                self.lines.append(word)
                self.lines.append(' ')
                #self.lines.append("ARE WE EVER MAKING IT HERE???")

        return charCount

    def lm_printer(self): 
        charsAdded = self.formatKeys[".LM"]
         
        for y in range(self.formatKeys[".LM"]):
            self.lines.append(' ')
        return charsAdded
         


    #Errors to handle or suggest a strategy to handle:

    # 1. A formatting code appears in the middle of a text file
    # 2. Line width exceeds the width of the page (goes over or goes negative)
    # 3. Formatting commands have negative arguments
    # 4. Formatting commands contain no arguments
    # 5. Multiple formatting commands on one line

