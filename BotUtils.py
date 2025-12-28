# to be re-writen
# Data Management
# Login System (Just Check if it Works Good)

# Main Commands
# Dig to optain Rersources
# Shop To sell Resources
# Money To See Corrent Balance
# Inv To See Current Items
# Inv Storage Email:[Item1, Item2 ]

# Name Of Items in Game , Discription and Price

# Server_Class.Add_Money("debanjanpahari009@gmail.com")
# print(Server_Class.Init_DF())

# Features to add
# Trade Trading items With other players
# PVE Battle To earn items and money
# Auction (maybe)
# Guild / Clan System (if possible I guess)

import pandas
import uuid
import random
import smtplib
from email.message import EmailMessage

class Serverinf:
    def __init__(self):
        self.df = self.Init_DF()
        self.debug_mode = True
        self.items = { # ItemName : [Percent Chance to Obtain Item , Price]
            "Mana_Crystal":[10 , 200],
            "Broken_CD":[60, 20]
        }

    def Init_DF(self):
        try:
            f = open("UserData.parquet")
        except FileNotFoundError:
            data = {
                "Session_ID":[],
                "Temp_OTP":[],
                "Online":[],
                "Money":[],
                "Mana_Crystal":[], # Item1
                "Broken_CD":[] # Item2
            }
            df = pandas.DataFrame(data)
        else:
            df = pandas.read_parquet("UserData.parquet")
        return df

    def Generate_OTP(self,Email):
        Generated_OTP = ""
        From_Mail_Pass = 'ladd vpgi hviz fnqv'
        From_Mail = 'faloautoapi21@gmail.com'

        for i in range(6):
            Generated_OTP += str(random.randint(0,9))

        if self.debug_mode == False:
            OTP_Server = smtplib.SMTP('smtp.gmail.com', 587)
            OTP_Server.starttls()
            OTP_Server.login(From_Mail, From_Mail_Pass)

            MSG = EmailMessage()
            MSG['Subject'] = "OTP Verification"
            MSG['From'] = From_Mail
            MSG['To'] = Email
            MSG.set_content("Your OTP = " + Generated_OTP)
            OTP_Server.send_message(MSG)

        return Generated_OTP


    def Login_User(self, Email, OTP):
        if Email not in self.df.index:
            self.df.loc[Email] = ["Wait", self.Generate_OTP(Email), False, 0, 0, 0]
            self.df.to_parquet("UserData.parquet")
            return {"Message":"Check your Mail for OTP", "Data": "CHECKMAIL"}
        else:
            if self.df.loc[Email]["Online"] == False:
                Get_OTP_DB = self.df.loc[Email]["Temp_OTP"]
                if str(OTP) == str(Get_OTP_DB):
                    Session_ID = uuid.uuid4()
                    self.df.loc[Email,"Session_ID"] = str(Session_ID)
                    self.df.loc[Email,"Online"] = True
                    self.df.to_parquet("UserData.parquet")
                    return {"Message":"You are Loggedin Now", "Data": str(Session_ID)}
                else:
                    self.df.loc[Email,"Temp_OTP"] = self.Generate_OTP(Email)
                    self.df.to_parquet("UserData.parquet")
                    if OTP == "GET_OTP":
                        return {"Message":"Check your Mail for OTP", "Data": "CHECKMAIL"}
                    else:
                        return {"Message":"Some Message", "Data": "ERROR"}
            else:
                return {"Message":"Loggout First to Login", "Data": "LOGOUT"}

    def Logout(self,Email,LogAuth):
        if self.df.loc[Email]["Online"] == True:
            if LogAuth == self.df.loc[Email]["Temp_OTP"] or self.df.loc[Email]["Session_ID"]:
                self.df.loc[Email,"Online"] = False
                self.df.loc[Email,"Session_ID"] = "Wait"
                self.df.to_parquet("UserData.parquet")
                return {"Message":"You Logged out Now", "Data": "LOGOUTSUCESS"}
            else:
                self.df.loc[Email,"Temp_OTP"] = self.Generate_OTP(Email)
                self.df.to_parquet("UserData.parquet")
                if LogAuth == "GET_OUTOTP":
                    return {"Message":"Check your Mail for OTP", "Data": "CHECKMAIL"}
                else:
                    return {"Message":"Some Message", "Data": "ERROR"}
        else:
            return {"Message":"Login First to Loggout", "Data": "LOGIN"}

    def ChanceValue(self):
        weightArray = []
        for j in range(0,len(self.items)):
            name = list(self.items.keys())[j]
            chance = list(self.items.values())[j][0]
            weightArray += [name]*int(chance*100)
        return random.choice(weightArray)

    def Dig(self,Email, LogAuth):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                ItemValue = self.ChanceValue()
                self.df.loc[Email, ItemValue] += 1
                self.df.to_parquet("UserData.parquet")
                return {"Message":"You Got Item", "Data": ItemValue}

    def ShopList(self ,Email ,LogAuth):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                return {"Message":"List of all Items", "Data": self.items}

    def BuyItem(self,Email, LogAuth,ItemName,ItemValue):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                if self.df.loc[Email]["Money"] > 0:
                    if self.items[ItemName][1] * ItemValue < self.df.loc[Email]["Money"]:
                        self.df.loc[Email, ItemName] += ItemValue
                        self.df.loc[Email, "Money"] -= self.items[ItemName][1] * ItemValue

    def SellItem(self,Email, LogAuth,ItemName,ItemValue):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                if self.df.loc[Email][ItemName] > 0:
                    if ItemValue <= self.df.loc[Email][ItemName]:
                        self.df.loc[Email, ItemName] -= ItemValue
                        self.df.loc[Email, "Money"] += self.items[ItemName][1] * ItemValue

    def Inventory(self, Email, LogAuth):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                Inv = {}
                for i in range (0, len(self.items)):
                    name = list(self.items.keys())[i]
                    value = self.df.loc[Email][str(name)]
                    Inv[name] = str(value)
                return {"Message":"All Items in Inventory", "Data": Inv}

    def Display_Money(self,Email, LogAuth):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                return {"Message":"List of all Items", "Data": str(self.df.loc[Email]["Money"])}

    def TurnEnvAttack(self,Email, LogAuth):
        if LogAuth == self.df.loc[Email]["Session_ID"]:
            if self.df.loc[Email]["Online"] == True:
                pass
