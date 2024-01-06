import pandas as pd


# function to remove anything but digits and commas
def onlyDigAndCommas(string):
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

# only digits amd periods
def onlyDigAndPeriods(string):
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
def onlyDate(string):
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
def onlyDigits(string):
    output = "".join([char for char in string if char.isdigit()])
    return output
# \/ Returns typeList of excersises 
def dataToexcersies(fileName):

    with open(fileName, "r") as f:
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

# for line in dataToexcersies("noKeyData.txt"):
#     print(line)

# \/ Returns a list of workouts
def dataToWorkouts(fileName):
    with open(fileName, "r") as f:
        data = f.read()
        f.close()

    perWorkoutData = data.split("\n\n")
    return perWorkoutData

# Replace all excersise names with the new names from our key
def replaceExcersises(dataFile, outPutFileName, key):


    df = pd.read_csv(key)
    
    with open(dataFile, "r") as f:
        content = f.read()
        f.close()
 


         

        for index, (RName, NName) in df[["Raw_Name", "New_Name"]].iterrows():
             
                        
                
            # print(f"Replacing ||{RName}|| with ||{NName}||")
            content = content.replace(RName, NName)


    with open(outPutFileName, "w") as f:
        f.write(content)
        f.close()

        
# replaceExcersises("noKeyData.txt", "outPutFile.txt", "key.csv")
# print(len(dataToexcersies("outPutFile.txt")))

# with open("newUnique.txt", "w") as f:
#     for item in dataToexcersies("outPutFile.txt"):
#         f.write(item + "\n")
#     f.close()
        
# Given a line in a workout we need to return a list which corresponds to a row in the dataframe
def parseLine(line, date):

    line = line.strip()

    # empty list to be a row
    # [|DATE|, |EXCERSISE|, |WEIGHT|, [|REPS|]]
    output = []
    # first element is the date
    output.append(onlyDate(date))
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
    output.append(onlyDigAndPeriods(weight.strip()))

    

    # get reps
    reps = ""
    # line from reps to end stripped
    
    lineRepsToEnd = lineWeightToEnd[endWeightIndex:].strip()
    reps = onlyDigAndCommas(lineRepsToEnd)


    
    output.append(reps)
    
    
    return output 


# We need a a function just to parse a workout, so given a workout
#   it returns a list of lists which would each be a row in the dataframe
def parseWorkout(workout):
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
            lineToRow = parseLine(line, date)
            if "skip" != lineToRow:
                # add the row to the output     
                output.append(lineToRow)
    return output 


def finalParsing(dataTxtFile):
    # Grab the content, this should have unique excersises
    with open(dataTxtFile, "r") as f:
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
        output = parseWorkout(workout)
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

    # and return our pandas dataframe
    return df


df = finalParsing("outPutFile.txt")

def filterWhereXequalsY(df, x, y):
    result = df[df[x] == y]
    result = result.sort_values(by='Date')
    return result

def dfToCSV(df, fileName):
    df.to_csv(fileName, index=False)

print(
    filterWhereXequalsY(df, "Exercise", "SA Tri PD")
)

