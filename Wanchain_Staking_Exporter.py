# Importing Packages
import pandas as pd
import time
from tqdm import tqdm

#Progress Bar
tqdm.pandas()

# Input fields
adr = input("Please Enter your Wan Adress")
pages = int(input(" Please Enter Pages "))

# Initiate lists
page = 0
data = []

#For loop Data 
for page in range(0,pages):
    page += 1
    df = pd.read_html(f"https://www.wanscan.org/rewardD?addr={adr}&page={page}&validator=undefined")[0]
    data.append(df)
    print(f"Done With page:  {page}")


# Data Cleaning
data = pd.concat(data)
data.drop("No",axis="columns",inplace=True)
data["Currency"] = "WAN"
data["Amount"] = data.Reward.str.strip("WAN")
data.Amount = data.Amount.astype(float)
data.drop("Unnamed: 4",axis="columns",inplace=True)
data.drop("Reward",axis="columns",inplace=True)


#Getting Dates from Block information 
def Date_Block(block):
    date_raw = pd.read_html(f"https://www.wanscan.org/block/{block}")[0].T.iloc[1:,2]
    return date_raw
    
# Applying function
data["Date"] =data.Block.progress_apply(Date_Block)

#Cleaning String
data["Date"] = data.Date.apply(lambda x: x[x.find("(")+1:x.find(")")])
data["Date"] = data["Date"].apply(lambda x: x.split(" ", 1)[0])
data["Date"] = data.Date.apply(lambda x: x.replace("Spt","Sep"))
data["Date"] = pd.to_datetime(data.Date)



#Export to Excel or CSV
while True:
    file_ouput = input("Which File Format do you want: excel, csv or both").lower()
    if file_ouput == "excel":
        data.to_excel("wanchain.xlsx",index=False)
        print("Excel file is succesfully created")
        break
    elif file_ouput == "csv" : 
        data.to_csv("wanchain.csv")
        print("CSV file is succesfully created")
        break
    elif file_ouput == "both":
        data.to_excel("wanchain.xlsx",index=False)
        data.to_csv("wanchain.csv")
        print("Both excel and CSV are succesfully created")
        break
    elif file_ouput != "excel" or "csv" or "both":
        print("You Should enter either excel, csv or both")
    
print("Script is done running - You can close it now")