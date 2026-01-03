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

import random
import uuid

import pandas


class Serverinf:
    def __init__(self):
        self.df = self.Init_DF()
        self.debug_mode = True
        self.items = {  # ItemName : [Percent Chance to Obtain Item , Price]
            "Mana_Crystal": [10, 200],
            "Broken_CD": [60, 20],
        }

    def Init_DF(self):
        try:
            f = open("UserData.parquet")
        except FileNotFoundError:
            data = {
                "Session_ID": [],
                "Temp_OTP": [],
                "Online": [],
                "Money": [],
                "Mana_Crystal": [],  # Item1
                "Broken_CD": [],  # Item2
            }
            df = pandas.DataFrame(data)
        else:
            df = pandas.read_parquet("UserData.parquet")
        return df

    def Register_User(self, Username):
        pass

    def ChanceValue(self):
        weightArray = []
        for j in range(0, len(self.items)):
            name = list(self.items.keys())[j]
            chance = list(self.items.values())[j][0]
            weightArray += [name] * int(chance * 100)
        return random.choice(weightArray)

    def Dig(self, Email):
        ItemValue = self.ChanceValue()
        self.df.loc[Email, ItemValue] += 1
        self.df.to_parquet("UserData.parquet")
        return {"Message": "You Got Item", "Data": ItemValue}

    def ShopList(self):
        return {"Message": "List of all Items", "Data": self.items}

    def BuyItem(self, Email, ItemName, ItemValue):
        if self.df.loc[Email]["Money"] > 0:
            if self.items[ItemName][1] * ItemValue < self.df.loc[Email]["Money"]:
                self.df.loc[Email, ItemName] += ItemValue
                self.df.loc[Email, "Money"] -= self.items[ItemName][1] * ItemValue

    def SellItem(self, Email, ItemName, ItemValue):
        if self.df.loc[Email][ItemName] > 0:
            if ItemValue <= self.df.loc[Email][ItemName]:
                self.df.loc[Email, ItemName] -= ItemValue
                self.df.loc[Email, "Money"] += self.items[ItemName][1] * ItemValue

    def Inventory(self, Email):
        Inv = {}
        for i in range(0, len(self.items)):
            name = list(self.items.keys())[i]
            value = self.df.loc[Email][str(name)]
            Inv[name] = str(value)
        return {"Message": "All Items in Inventory", "Data": Inv}

    def Display_Money(self):
        return {
            "Message": "List of all Items",
            "Data": str(self.df.loc[Email]["Money"]),
        }

    def TurnEnvAttack(self):
        pass
