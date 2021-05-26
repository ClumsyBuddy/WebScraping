from time import sleep
import threading
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Items: #This is how I check what item I am on
    RTX1660 = 1
    RTX3060 = 2

class WebscrapperData: #This holds data for the Webscrapper, still moving things back and forth
    def __init__(self):
        self.ContinueLooping = True #Used to exit the program
        self.DRIVER_PATH = "D:\\Coding Projects\\WebScraping\\chromedriver.exe" #Path to the google driver

        self.ItemDict = {
            1 : 'https://www.bestbuy.com/site/searchpage.jsp?st=1660+ti&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys',
            2 : 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=currentprice_facet%3DPrice~%24250%20-%20%24499.99%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%203060&type=page&usc=All%20Categories'
        }
        self.Item = Items


class WebScrapper:
    def __init__(self, ItemName, WebData, _Item): #The init function has the driver and Chrome options for the webdriver
        self.ItemName = ItemName
        self.WebData = WebData
        self._Item = _Item
        self.ChromeOptions = Options() #OPtions object
        self.ChromeOptions.add_argument('log-level=3') #Changes the log level to keep console clear
        self.ChromeOptions.add_argument("--window-size=1920,1080") #Sets the display size of the client
        self.ChromeOptions.headless = True #Make the client headless
        self.driver = webdriver.Chrome(options=self.ChromeOptions, executable_path=self.WebData.DRIVER_PATH) #Create the driver
    #This function is the meat of the class, it find the elements from the page and prints them out
    def Task_GetPage(self):
        while self.WebData.ContinueLooping == True:
            print("Getting Information: ", self.ItemName)
            self.CheckItem()
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            for post in soup.find_all("li", class_="sku-item"):
                div = post.find('div', class_="sku-title")
                h4 = div.find('h4', class_="sku-header")
                _Name = h4.find('a')
                button = post.find("button", class_="add-to-cart-button")
                print("---------------------")
                print(_Name.text)
                print(button.text)
                print("---------------------")
                if button.text == "Sold Out":
                    print("Sold out")
        self.driver.quit() #Closes webdriver
    #This Function get the webpage and reloads it
    #if it fails it prints a log then stops the loop
    def CheckItem(self):
        try:
           self.driver.get(self.WebData.ItemDict[self._Item])
        except:
            print("Couldn't Get Webpage", self.ItemName)
            self.WebData.ContinueLooping = False




def main():

    #Create instance of class holding informtation to for webscraping
    _Data = WebscrapperData()
    #First we start the thread to get key presses
    Task_KeyCheck = threading.Thread(target=KeyCheck, args=(_Data,))
    Task_KeyCheck.start()
    #We make a dictionary for the different products
    NameList = {
        "3060" : 1, 
        "1660" : 2
    }
    #This will hold the different classes
    ClassHolder = []
    #This will hold the different tasks (Threads)
    Tasks = []
    #Loop through the dictionary and create a classs for each with the arguements name _data num
    for name,num in NameList.items():
        ClassHolder.append(WebScrapper(name, _Data, num))
    #Loop through the classes and start the threads, the threads run the Task_GetPage Function
    for Index in range(len(ClassHolder)):
        Tasks.append(threading.Thread(target=ClassHolder[Index].Task_GetPage))
    #Start the tasks 15 seconds apart
    for _tasks in Tasks:
        _tasks.start()
        sleep(15)
    
#This function constantly checks for certain key presses and Sets the variable continuelooping to false
#you press the key
def KeyCheck(Data):
    print("Grabbing keys")
    while Data.ContinueLooping == True:
        if keyboard.is_pressed("l"):
            Data.ContinueLooping = False
            print("Exiting app")


if __name__ == '__main__':
   main()


