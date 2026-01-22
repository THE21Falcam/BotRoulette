# Main Commands
# Shop To sell Resources
# Money To See Corrent Balance
# Inv To See Current Items

# Name Of Items in Game , Discription and Price

from configparser import ConfigParser

config = ConfigParser()
config.read("ClientConfig.ini")


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
