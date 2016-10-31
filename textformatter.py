import fileinput
import sys

class Formatter:
    #class can and should have instance variables
    

    def __init__(self, inputfile, inputLines):

        self.formatKeys = {".LW": 0, ".LM": 0, ".LS": 0, ".FT": "off"}
        self.filename = inputfile
        self.filelen = 0
        self.currentLine = ""
        self.lines = []
        self.charCount = 0
        self.read_file()  

    def read_file(self):
        filelines = self.set_file_len()
        idx = 0
        extraNewline = False
        newPara = False
        firstWord = False

        for line in filelines:#self.file:
            idx +=1
            #print(line, end='') 
            if idx == self.filelen and line == '\n':
                extraNewline = True
                break;      
            if self.check_newline(line) and (idx != self.filelen): # appends an empty string to the the line (the driver will print the newline). If true continues to the next iteration
                newPara = True
                continue
            cmd = self.get_args(line)
            if cmd != '0': 
                self.set_args(line, cmd)
                newPara = True
                continue
            if newPara and self.formatKeys[".FT"] == "on":
                #print("I SHOULDNT BE IN HERE")
                self.new_para_formatter() #Applies appropriate formatting to the first line of the paragraph, and returns the amount of characters printed
                firstWord = True
                newPara = False
                
            firstWord = self.inParaFormatter(line, firstWord)


        if self.formatKeys[".FT"] == "on": 
            self.lines.append(self.currentLine)

        if extraNewline:
            self.lines.append('')
    
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

        #print(self.formatKeys)

    def get_args(self,l):
        l = l.split()
        if ((".LW" in l) or (".LS" in l) or (".LM" in l) or (".FT" in l)) and len(l) == 2:
                return l[0]

        else:
            return '0'

    def check_newline(self,l):
        if l == '\n':
            self.charCount = 0
            self.lines.append(self.currentLine) # add the currentline to the lines list
            self.currentLine = "" #clear the current line
            self.currentLine += '' #add a blank element to the currentline
            self.lines.append(self.currentLine) #add the blank element to the line list
            self.ls_printer()
            self.ls_printer()

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

                self.filelen = idx
                #print(idx)
            return lineList
        except FileNotFoundError:
            print("File not found")
            sys.exit(0)

    def inParaFormatter(self, l, fw):
        if self.formatKeys[".FT"] == "on":

            firstWord = fw
            #print(l)
            l = l.split() # Turn the line into an array of words

            for word in l:
                # print(self.currentLine)
                self.charCount += len(word)

                if self.charCount +1 > self.formatKeys[".LW"]:
                    self.lines.append(self.currentLine)
                    self.currentLine = "" 
                    self.ls_printer()
                    self.charCount = self.lm_printer() #call this function to add appropriate line spacing after the newline, it returns the number of chars added
                    self.currentLine += word #add the current word to the new line
                    self.charCount += len(word) # Add the length of the word to the number of chars added by margin (Now the charCount should only account for the current word and the margin added)
                    firstWord = False

                elif self.charCount +1 == self.formatKeys[".LW"]:
                    self.currentLine += ' ' #add a space to the current line
                    self.currentLine += word #add the word to the current line
                    self.lines.append(self.currentLine) #add the current line to the lines list
                    self.currentLine = "" #clear the current line
                    self.ls_printer() # Print out appropriate linespacing
                    self.charCount = self.lm_printer() #call this function to add appropriate line spacing after the newline, it returns the number of chars added
                    firstWord = True

                else:
                    if firstWord:
                        self.currentLine += word
                        firstWord = False
                    else:
                        self.currentLine += ' ' # add a space to before the new word on the current line
                        self.currentLine += word # add the word to the current line 
                        self.charCount += 1 #add the space to the charcount
                        #print(self.currentLine)

            return firstWord  

        else:
            if l != '\n':
                l = l.strip('\n')
                self.lines.append(l)

        

    def new_para_formatter(self):
        if self.formatKeys[".FT"] == "on":
            self.lm_printer()
            #self.ls_printer()
            self.charCount += self.formatKeys[".LM"]
            
        return 0

    def lm_printer(self): 
        charsAdded = self.formatKeys[".LM"]
         
        for y in range(self.formatKeys[".LM"]):
            self.currentLine += ' '
        return charsAdded
         
    def ls_printer(self):
        for y in range(self.formatKeys[".LS"]):
            self.lines.append('')

        return 0

    #Errors to handle or suggest a strategy to handle:

    # 1. A formatting code appears in the middle of a text file
    # 2. Line width exceeds the width of the page (goes over or goes negative)
    # 3. Formatting commands have negative arguments
    # 4. Formatting commands contain no arguments
    # 5. Multiple formatting commands on one line

