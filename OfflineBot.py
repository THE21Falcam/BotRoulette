# Main Commands
# Dig to optain Rersources
# Shop To sell Resources
# Money To See Corrent Balance
# Inv To See Current Items

# Name Of Items in Game , Discription and Price

from configparser import ConfigParser

import BotUtils
import requests

ONLINE = False
ENDPOINT = "http://127.0.0.1:5000"

config = ConfigParser()
config.read("ClientConfig.ini")

Server_Class = ServerUtils.Serverinf()

Running = True
print('Welcome To The Game Type "help" to Get Help ')
while Running:
    Dig = input("Enter Command >> ")
    match Dig:  # Direct with ServerUtils
        case "help":
            print("List of Commands")
            print("login = Logs You In")
            print("quit = Logs You Out")
            print("dig = Gives you a Random Item")
            print("buy = Bying Items")
            print("sell = Selling Items")
            print("inv = Shows Your Inventory")
            print("shop = shows list of Items in Shop")
            print("cash = Shows cash")
            print("attack = Attack Enemy")
        case "login":
            LoginData = Server_Class.Login_User(
                "debanjanpahari009@gmail.com", "GET_OTP"
            )
            print(LoginData)
            print(Server_Class.Init_DF())
            if LoginData["Data"] == "CHECKMAIL":
                ENOTP = input("Enter Your OTP >> ")
                LoginDataSD = Server_Class.Login_User(
                    "debanjanpahari009@gmail.com", ENOTP
                )
                config["CLIENT"] = {"Sesson_ID": str(LoginDataSD["Data"])}
                with open("ClientConfig.ini", "w") as ConfLOG:
                    config.write(ConfLOG)
                print(LoginDataSD)
            if LoginData["Data"] == "LOGOUT":
                print("You are Loggedin")

        case "buy":
            SessionID = config["CLIENT"]["Sesson_ID"]
            Server_Class.BuyItem(
                "debanjanpahari009@gmail.com", str(SessionID), "Broken_CD", 2
            )

        case "sell":
            SessionID = config["CLIENT"]["Sesson_ID"]
            Server_Class.SellItem(
                "debanjanpahari009@gmail.com", str(SessionID), "Broken_CD", 4
            )

        case "shop":
            SessionID = config["CLIENT"]["Sesson_ID"]
            print(Server_Class.ShopList("debanjanpahari009@gmail.com", str(SessionID)))

        case "inv":
            SessionID = config["CLIENT"]["Sesson_ID"]
            print(Server_Class.Inventory("debanjanpahari009@gmail.com", str(SessionID)))

        case "cash":
            SessionID = config["CLIENT"]["Sesson_ID"]
            print(
                Server_Class.Display_Money(
                    "debanjanpahari009@gmail.com", str(SessionID)
                )
            )

        case "dig":
            SessionID = config["CLIENT"]["Sesson_ID"]
            print(Server_Class.Dig("debanjanpahari009@gmail.com", str(SessionID)))

        case "attack":
            print("Attack")

        case "quit":
            SessionID = config["CLIENT"]["Sesson_ID"]
            LogoutData = Server_Class.Logout(
                "debanjanpahari009@gmail.com", str(SessionID)
            )
            print(LogoutData)

            if LogoutData["Data"] == "ERROR":
                LogoutDataSD = Server_Class.Logout(
                    "debanjanpahari009@gmail.com", "GET_OUTOTP"
                )
                if LogoutDataSD["Data"] == "CHECKMAIL":
                    print(Server_Class.Init_DF())
                    ENOTPs = input("Enter Your OTP >> ")
                    LogoutSDCOMP = Server_Class.Logout(
                        "debanjanpahari009@gmail.com", ENOTPs
                    )
            if LogoutData["Data"] == "LOGIN" or "LOGOUTSUCESS":
                print("You are Loggedout")
                Running = False
