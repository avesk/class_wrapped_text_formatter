import fileinput
import sys

class Formatter:
    
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
        lastLineWasNewline = False

        for line in filelines:#self.file:
            idx +=1
            #print(line, end='') 
            if idx == self.filelen and line == '\n': #covers the edge case where there is a blank line at the end of the file
                extraNewline = True #sets this value to true to let the program know we only want to print none-extraneous newlines at the EOF
                break; 
            if firstWord == True and line == '\n': #covers the edge case where the charcount has been exactly reached and there is a paragraph break
                self.lines.append('')
                continue
            if self.check_newline(line, lastLineWasNewline) and (idx != self.filelen): # appends an empty string to the the line (the driver will print the newline). If true continues to the next iteration
                newPara = True #Value lets the program know that the incoming line is a new paragraph
                lastLineWasNewline = True #Lets the program know that the last line was a newline
                continue
            lastLineWasNewline = False #This will only be reached if the last line was not a newline

            cmd = self.get_args(line) # gets the formatting command and sets the arguments. Returns '0' if no commands were found
            if cmd != '0': #Will evaluate to false if no commands were found
                self.set_args(line, cmd)
                newPara = True
                continue
            if newPara and self.formatKeys[".FT"] == "on": 
                self.new_para_formatter() #Applies appropriate formatting to the first line of the paragraph, and returns the amount of characters printed
                firstWord = True #lets the program know that the incoming word is the first word of the line
                newPara = False #next incoming line no longer a new paragraph, unless otherwise specified later in the algorithm
                
            firstWord = self.inParaFormatter(line, firstWord) #The inParaFormatter returns the truth value of firstword for its next iteration

        if self.formatKeys[".FT"] == "on": #as long as formatting is on, the last line processed should be added to the lines list, if it already was, an empty string will be appended
            self.lines.append(self.currentLine)

        if extraNewline: #covers the edge case of extra newlines
            self.lines.append('')

        return 0

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

    def check_newline(self,l, llwnl):

        if l == '\n' and self.formatKeys[".FT"] == "on":
            if llwnl: #If the last line was a newline, we only want to print out one line
                self.lines.append('')
                return True

            else:    
                self.charCount = 0
                self.lines.append(self.currentLine) # add the currentline to the lines list
                self.currentLine = "" #clear the current line
                self.currentLine += '' #add a blank element to the currentline
                self.lines.append(self.currentLine) #add the blank element to the line list
                self.ls_printer() #apply appropriate linespacing
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
                    idx+=1
                    lineList.append(line)

                self.filelen = idx
            return lineList

        except FileNotFoundError:
            print("File not found")
            sys.exit(0)

    def inParaFormatter(self, l, fw):
        if self.formatKeys[".FT"] == "on":

            firstWord = fw
            l = l.split() # Turn the line into an array of words

            for word in l:
                self.charCount += len(word)

                if self.charCount +1 > self.formatKeys[".LW"]: #Checks if the incomming word exceeded the charcount
                    self.lines.append(self.currentLine) #Breaks the line, clears the current line, applies formatting
                    self.currentLine = "" 
                    self.ls_printer()
                    self.charCount = self.lm_printer() #call this function to add appropriate line spacing after the newline, it returns the number of chars added
                    self.currentLine += word #add the current word to the new line
                    self.charCount += len(word) # Add the length of the word to the number of chars added by margin (Now the charCount should only account for the current word and the margin added)
                    firstWord = False #If this block of code was ran, we are not processing the first word

                elif self.charCount +1 == self.formatKeys[".LW"]: #checks if the current word proccessed exactly matched the charcount
                    self.currentLine += ' ' #add a space to the current line
                    self.currentLine += word #add the word to the current line
                    self.lines.append(self.currentLine) #add the current line to the lines list
                    self.currentLine = "" #clear the current line
                    self.ls_printer() # Print out appropriate linespacing
                    self.charCount = self.lm_printer() #call this function to add appropriate line spacing after the newline, it returns the number of chars added
                    firstWord = True

                else:
                    if firstWord: #If we are processing the first word of the line, just concatenate the word with no spaces, or else we will get extra spaces
                        self.currentLine += word
                        firstWord = False
                    else: #Else, concat a space and then the word
                        self.currentLine += ' ' # add a space to before the new word on the current line
                        self.currentLine += word # add the word to the current line 
                        self.charCount += 1 #add the space to the charcount

            return firstWord #return the truth value of first word, incase the last word processed of the line exactly matched the charcount 

        else: #if formatting is off, concat the raw lines to the lines list
            l = l.strip('\n')
            self.lines.append(l)

    def new_para_formatter(self): #for pre-emptively applying line margin to new paragraph lines, or else formatting will be applied out of sequence
        if self.formatKeys[".FT"] == "on":
            self.lm_printer()
            self.charCount += self.formatKeys[".LM"]    
        return 0

    def lm_printer(self): #called to add appropriate line margin
        charsAdded = self.formatKeys[".LM"]   
        for y in range(self.formatKeys[".LM"]):
            self.currentLine += ' '
        return charsAdded
         
    def ls_printer(self):#called to add appropriate line spacing
        for y in range(self.formatKeys[".LS"]):
            self.lines.append('')
        return 0

    #Errors to handle or suggest a strategy to handle:

    # 1. A formatting code appears in the middle of a text file
    # 2. Line width exceeds the width of the page (goes over or goes negative)
    # 3. Formatting commands have negative arguments
    # 4. Formatting commands contain no arguments
    # 5. Multiple formatting commands on one line

