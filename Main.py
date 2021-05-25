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
        self.ChromeOptions = Options() #OPtions object
        self.ChromeOptions.add_argument('log-level=3') #Changes the log level to keep console clear
        self.ChromeOptions.add_argument("--window-size=1920,1080") #Sets the display size of the client
        self.ChromeOptions.headless = True #Make the client headless
        self.driver = webdriver.Chrome(options=self.ChromeOptions, executable_path=self.DRIVER_PATH) #Create the driver
        self.RTX1660 = 'https://www.bestbuy.com/site/searchpage.jsp?st=1660+ti&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
        self.RTX3060 = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=currentprice_facet%3DPrice~%24250%20-%20%24499.99%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti&sc=Global&st=rtx%203060&type=page&usc=All%20Categories'
        self.Item = Items

def main():
    #Create instance of class holding informtation to for webscraping
    _Data = WebscrapperData()
    #Create threads to for checking key presses and running the webscraper
    Task_KeyCheck = threading.Thread(target=KeyCheck, args=(_Data, 0.05,))  #Takes class we made a arguement and a delay  
    Task_GTX3060 = threading.Thread(target=Task_GetPage, args=(_Data, 0 , 60, _Data.Item.RTX3060,))
    #Task_GTX1660TI = threading.Thread(target=Task_GetPage, args=(_Data, 60 , 60,))
    #Start them
    Task_KeyCheck.start()
    Task_GTX3060.start()
    #Task_GTX1660TI.start()


    
#If the program is to continue looping check for key press to stop looping
def KeyCheck(KeyData, Delay=0.05):
    KeyData.ContinueLooping = True
    while KeyData.ContinueLooping == True:
        if keyboard.is_pressed("l"):
            KeyData.ContinueLooping = False
            print("Exiting app")
        sleep(0.10)

#Get the html page with a headless client
#Parse the html with bs4
#Search a set of tags to find specific information
def Task_GetPage(WebData, StartDelay, Delay, _Item):
    sleep(StartDelay) #Delay to space the threads
    while WebData.ContinueLooping == True:
        print("Getting Information")
        CheckItem(WebData, _Item)
        soup = BeautifulSoup(WebData.driver.page_source, "html.parser")
        for post in soup.find_all("li", class_="sku-item"):
            div = post.find('div', class_="sku-title")
            h4 = div.find('h4', class_="sku-header")
            Name = h4.find('a')
            button = post.find("button", class_="add-to-cart-button")
            print("---------------------")
            print(Name.text)
            print(button.text)
            print("---------------------")
        sleep(Delay) #Delay so we arent grabbing the site faster than allowed
    WebData.driver.quit() #Closes webdriver




def CheckItem(_Data, _Item):
    if _Item == _Data.Item.RTX1660:
        _Data.driver.get(_Data.RTX1660)
    elif _Item == _Data.Item.RTX3060:
        _Data.driver.get(_Data.RTX3060)
    else:
        print("Couldn't get webpage")
    



if __name__ == '__main__':
   main()


