import pandas as pd


class gymDataProcessor():
    def __init__(self, dataFile):
        self. dataFile = dataFile
        self.DATAFRAME = pd.DataFrame()
        self.latestResult = pd.DataFrame()


     # function to remove anything but digits and commas
    def onlyDigAndCommas(self, string):
        output = "".join([char for char in string if char.isdigit() or char == ","])
        # if first char is a comma, remove it
        # if not empty
        if output != "":
            if output[0] == ",":
                output = output[1:]
            # if last char is a comma, remove it
            if output[-1] == ",":
                output = output[:-1]
        return output
    
    def onlyDigAndPeriods(self, string):
        output = "".join([char for char in string if char.isdigit() or char == "."])
        # if first char is a period, remove it
        # if not empty
        if output != "":
            if output[0] == ".":
                output = output[1:]
            # if last char is a period, remove it
            if output[-1] == ".":
                output = output[:-1]
        return output

    # funtion to grab only the date from the start of the string, in our case, up to the first space
    def onlyDate(self, string):
        output = ""
        for char in string:
            if char == " ":
                break
            else:
                output += char
        # if slashes are in date, change to dashes
        if "/" in output:
            output = output.replace("/", "-")
        return output

    # function to remove anything but digits
    def onlyDigits(self, string):
        output = "".join([char for char in string if char.isdigit()])
        return output

    # \/ Returns typeList of excersises 
    def dataToexcersies(self):

        with open(self.dataFile, "r") as f:
            data = f.read()
            f.close()

        perWorkoutData = data.split("\n\n")
        # data is now a list where each element is a workout

        # need to make a list of every excersise in the data. 

        typeList = []

        for workout in perWorkoutData:
            lineList = workout.split("\n")
            for lineIndex, line in enumerate(lineList):
                if lineIndex == 0:
                    pass
                else: 
                    excersise = ""
                    for char in line:
                        if char.isdigit() or char =="#" or char == "|":
                            break 
                        else: 
                            excersise += char   
                    excersise = excersise.strip()
                    typeList.append(excersise)

        # make unique
        typeList = list(set(typeList)) 

        return typeList

    # \/ Returns a list of workouts
    def dataToWorkouts(self):
        with open(self.dataFile, "r") as f:
            data = f.read()
            f.close()
        perWorkoutData = data.split("\n\n")
        return perWorkoutData


    def parseLine(self, line, date):
        line = line.strip()
        # empty list to be a row
        # [|DATE|, |EXCERSISE|, |WEIGHT|, [|REPS|]]
        output = []
        # first element is the date
        output.append(self.onlyDate(date))
        # get the excersise name
        endExerIndex = int()
        excersise = ""
        for char in line:
            if char.isdigit() or char == "#" or char == "|":
                # if also first digit, skip this line
                if line.index(char) == 0:
                    return "skip"  
                if line.index(char) > 1:
                    # note the index right before
                    endExerIndex = line.index(char) - 1
                break
            # catch if char is b and next is w
            elif char == "b" and line[line.index(char) + 1] == "w":
                break 
            else:
                excersise += char
        # next element is the excersise name
        output.append(excersise.strip())
        # get the weight
        weight = ""
        endWeightIndex = int()
        # line from weight to end stripped
        lineWeightToEnd = line[endExerIndex:].strip()
        # we can start where exercise ended
        for char in lineWeightToEnd:
            if not char == " ":
                weight += char
            elif char == " ":
                # get index of the char right before the reps
                endWeightIndex = lineWeightToEnd.index(char)
                # should be triggered by a space so don't need to minus 1 
                break
        output.append(self.onlyDigAndPeriods(weight.strip()))
        # get reps
        reps = ""
        # line from reps to end stripped   
        lineRepsToEnd = lineWeightToEnd[endWeightIndex:].strip()
        reps = self.onlyDigAndCommas(lineRepsToEnd)
        output.append(reps)  
        return output 

    # We need a a function just to parse a workout, so given a workout
    #   it returns a list of lists which would each be a row in the dataframe
    def parseWorkout(self, workout):
        # print(
        #     f"workout passed to parseWorkout:\n {workout} \n\n"
        # )
        # start empty list to be list of rows
        output = []
        workoutLines = workout.split("\n")
        date = workoutLines[0].strip()  
        for line in workoutLines:
            if workoutLines.index(line) == 0:
                # is date, don't parse
                pass
            elif workoutLines.index(line) != 0:
                lineToRow = self.parseLine(line, date)
                if "skip" != lineToRow:
                    # add the row to the output     
                    output.append(lineToRow)
        return output 


    def finalParsing(self):
        # Grab the content, this should have unique excersises
        with open(self.dataFile, "r") as f:
            content = f.read()
            f.close()
        # intialize a dataframe which we will add to as we parse the txt file
        df = pd.DataFrame(columns=['Date', 'Exercise', 'Weight', 'Reps'])
        # will look like this
        # | Date | Excersise | Reps | Weight |
        # Where reps is a list
        # split content so we can go by workout
        content = content.split("\n\n")
        print(f"len of content: {len(content)}")     
        for workout in content:
            output = self.parseWorkout(workout)
            # print(
            #     f"output from parseWokrout: {output} \n\n"
            # )
            # that output is a list of lists, each list is a row, and it is of one workout 
            # so we need to add it to the dataframe
            for row in output:
                df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
        
        # Dropping row with bad weight values. rep values we care less about. 
        df = df[df['Weight'].apply(lambda x: len(str(x)) >= 1)]
        # Enure the dates are dates to pandas
        df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')

        print(df)
        # make csv
        df.to_csv('DATAFRAME.csv', index=False)

        # and save our pandas dataframe
        self.DATAFRAME = df
        return df

    def DFToCSV(self, fileName):
        self.DATAFRAME.to_csv(fileName, index=False)

    def resultToCSV(self, fileName):
        self.latestResult.to_csv(fileName, index=False)

    def filterWhereXequalsY(self, x, y):
        result = self.DATAFRAME[self.DATAFRAME[x] == y]
        result = result.sort_values(by='Date')
        self.latestResult = result
        



if __name__ == "__main__":
    

    finalRun = gymDataProcessor("outPutFile.txt") 
    finalRun.finalParsing()

   
    finalRun.DATAFRAME
    


    finalRun.filterWhereXequalsY('Exercise', 'Skull Crushers')

    finalRun.resultToCSV('SkullCrushers.csv')   


    