import fileinput


class Formatter:
    #class can and should have instance variables
    

    def __init__(self, inputfile, inputLines):

        self.formatKeys = {".LW": 0, ".LM": 0, ".LS": 0, ".FT": "off"}
        self.filename = inputfile
        self.lines = []

        self.read_file()

    def read_file(self):
        charCount = 0
        try:
            newPara = False

            with open(self.filename) as self.file:
                for line in self.file:
                    #line = line.strip('\n')

                    if check_newline(self.line): # appends the newline the the line. If true continues to the next iteration
                        newPara = True
                        continue
                    cmd = self.get_args(line)
                    if cmd != '0':
                        self.set_args(line, cmd)
                        newPara = True
                        continue
                    if newPara:
                        charCount += self.new_para_formatting(line) #Applies appropriate formatting to the first line of the paragraph, and returns the amount of characters printed
                        newPara = False
                        continue

                    charCount += self.format(line, charCount)
                    #self.lines.append(line)
             
        except FileNotFoundError:
            print("File not found")
            sys.exit(0)

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

    def format(self, l, charCount):
        numcharsAdded = charCount

        l = l.split()

        for word in l:
            if numcharsAdded+1 > self.formatKeys[".LW"]:
            
        
            if numcharsAdded == self.formatKeys[".LW"]:

            else:
                numcharsAdded += len(word)
                self.line.append(' ')
                self.lines.append(word)
                numcharsAdded += 1

        return numcharsAdded



    def lm_printer(self):
    if self.formatKeys[".LM"] > 0: 
        for y in range(self.formatKeys[".LM"]):
            self.lines.append(' ')
    else:
        return 

    def ls_printer(self):
    if self.formatKeys[".LS"] > 0: 
        for y in range(self.formatKeys[".LS"]):
            self.lines.append('\n')
    else:
        return   

    def check_newline(self,l):
        if l == '\n':
            self.lines.append(l)
            return true

        else:
            return false

    def new_para_formatting(self, l):
        self.lm_printer()
        self.ls_printer()
        numcharsAdded += self.formatKeys[".LM"]

        l = l.split()

        for word in l:
            numcharsAdded += len(word)
            self.lines.append(word)
            self.line.append(' ')
            numcharsAdded += 1
        
        return numcharsAdded


        

    #Errors to handle or suggest a strategy to handle:

    # 1. A formatting code appears in the middle of a text file
    # 2. Line width exceeds the width of the page (goes over or goes negative)
    # 3. Formatting commands have negative arguments
    # 4. Formatting commands contain no arguments
    # 5. Multiple formatting commands on one line

