from time import sleep
import threading
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from notify_run import Notify

class Items: #This is how I check what item I am on
    RTX1660 = 1
    RTX3060 = 2

class WebscrapperData: #This holds data for the Webscrapper, still moving things back and forth
    def __init__(self):
        self.ContinueLooping = True #Used to exit the program
        self.ItemAv = False
        self.notify = Notify()
        self.DRIVER_PATH = "D:\\Coding Projects\\WebScraping\\chromedriver.exe" #Path to the google driver
        self.ChromeOptions = Options() #OPtions object
        self.ChromeOptions.add_argument('log-level=3') #Changes the log level to keep console clear
        self.ChromeOptions.add_argument("--window-size=1920,1080") #Sets the display size of the client
        self.ChromeOptions.headless = True #Make the client headless
        self.ItemDict = {
            1 : 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=currentprice_facet%3DPrice~%24250%20-%20%24499.99%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%203060&type=page&usc=All%20Categories',
            2 : 'https://www.bestbuy.com/site/searchpage.jsp?st=1660+super&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
        }
        self.Item = Items
       


class WebScrapper:
    def __init__(self, ItemName, WebData, _Item): #The init function has the driver and Chrome options for the webdriver
        self.ItemName = ItemName
        self.WebData = WebData
        self._Item = _Item
        self.driver = webdriver.Chrome(options=self.WebData.ChromeOptions, executable_path=self.WebData.DRIVER_PATH) #Create the driver
        self.soup = None
    #This function is the meat of the class, it find the elements from the page and prints them out
    def Task_GetPage(self):
        while self.WebData.ContinueLooping == True:
            print("Getting Information: ", self.ItemName)
            self.Get_Page()
            self.Get_Page_Elements()
        self.driver.quit() #Closes webdriver

    #it then finds the elements I need and have specified
    #then prints out what it finds
    def Get_Page_Elements(self):
        for post in self.soup.find_all("li", class_="sku-item"):
            div = post.find('div', class_="sku-title")
            h4 = div.find('h4', class_="sku-header")
            _Name = h4.find('a')
            button = post.find("button", class_="add-to-cart-button")
            print(_Name.text)
            print(button.text)
            if button.text != "Sold Out":
                self.WebData.notify.send(_Name, button.text)
                self.WebData.ItemAv = True
        if self.WebData.ItemAv == True:
            sleep(600)

    #This Function get the webpage and reloads it
    #if it fails it prints a log then stops the loop
    def Get_Page(self):
        try:
           self.driver.get(self.WebData.ItemDict[self._Item])
           self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
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

    for _tasks in Tasks:
        _tasks.join()
    print("Exiting Program")
    
#This function constantly checks for certain key presses and Sets the variable continuelooping to false
#you press the key
def KeyCheck(Data):
    while Data.ContinueLooping == True:
        if keyboard.is_pressed("alt+o"):
            Data.ContinueLooping = False
            print("Stopping Application")


if __name__ == '__main__':
   main()


