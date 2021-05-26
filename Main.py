from time import sleep
import threading
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Items:
    RTX1660 = 1
    RTX3060 = 2

class WebscrapperData:
    def __init__(self):
        self.ContinueLooping = True #Used to exit the program
        self.DRIVER_PATH = "D:\\Coding Projects\\WebScraping\\chromedriver.exe" #Path to the google driver
        self.RTX1660 = 'https://www.bestbuy.com/site/searchpage.jsp?st=1660+ti&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
        self.RTX3060 = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=currentprice_facet%3DPrice~%24250%20-%20%24499.99%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%203060&type=page&usc=All%20Categories'
        self.Item = Items


class WebScrapper:
    def __init__(self, ItemName, WebData, _Item):
        self.ItemName = ItemName
        self.WebData = WebData
        self._Item = _Item
        self.ChromeOptions = Options() #OPtions object
        self.ChromeOptions.add_argument('log-level=3') #Changes the log level to keep console clear
        self.ChromeOptions.add_argument("--window-size=1920,1080") #Sets the display size of the client
        self.ChromeOptions.headless = True #Make the client headless
        self.driver = webdriver.Chrome(options=self.ChromeOptions, executable_path=self.WebData.DRIVER_PATH) #Create the driver

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

    def CheckItem(self):
        if self._Item == self.WebData.Item.RTX1660:
            self.driver.get(self.WebData.RTX1660)
        elif self._Item == self.WebData.Item.RTX3060:
            self.driver.get(self.WebData.RTX3060)
        else:
            print("Couldn't get webpage")



def main():
    #Create instance of class holding informtation to for webscraping
    _Data = WebscrapperData()

    GPU3060 = WebScrapper("3060", _Data, _Data.Item.RTX3060)
    GPU1660 = WebScrapper("1660", _Data, _Data.Item.RTX1660)

    #Create threads to for checking key presses and running the webscraper
    Task_KeyCheck = threading.Thread(target=KeyCheck, args=(_Data,))
    Task_KeyCheck.start()

    Task_GTX3060 = threading.Thread(target=GPU3060.Task_GetPage)
    Task_GTX3060.start()

    sleep(10)

    Task_GTX1660TI = threading.Thread(target=GPU1660.Task_GetPage)
    Task_GTX1660TI.start()
    
    
def KeyCheck(Data):
    while Data.ContinueLooping == True:
        if keyboard.is_pressed("l"):
            Data.ContinueLooping = False
            print("Exiting app")
        #sleep(0.10)yCheck():



if __name__ == '__main__':
   main()


