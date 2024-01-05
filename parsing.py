import pandas as pd

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

