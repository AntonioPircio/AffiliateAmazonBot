from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import constant,createTelegramMessage as message, scraper, utils
import asyncio
from threading import Thread, Event
from os.path import exists

class Window:

    def __init__(self, master):
        self.master = master

        self.Main = Frame(self.master, background='black')

        self.L1 = Label(self.Main, text="ANDIAMO A GUADAGNARE", background='green')
        self.L1.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        # ID CANALE
        self.labelIDChannel = Label(self.Main, text="ID DEL CANALE: ", background='red')
        self.labelIDChannel.grid(row=1, column=0, padx=5, pady=5)

        self.entryIDChannel = Entry(self.Main, width=30)
        self.entryIDChannel.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

        # CODE AMAZON AFFILIATE
        self.labelAffiliateCode = Label(self.Main, text="CODICE AFFILIATO AMAZON: ", background='green')
        self.labelAffiliateCode.grid(row=2, column=0, padx=5, pady=5)

        self.entryAffiliateCode = Entry(self.Main, width=30)
        self.entryAffiliateCode.grid(row=2, column=1, padx=5, pady=5, columnspan=3)

        # LINK CHANNEL
        self.labelLinkChannel = Label(self.Main, text="LINK CANALE TELEGRAM: ", background='red')
        self.labelLinkChannel.grid(row=3, column=0, padx=5, pady=5)

        self.entryLinkChannel = Entry(self.Main, width=30)
        self.entryLinkChannel.grid(row=3, column=1, padx=5, pady=5, columnspan=3)

        #PRODUCTS TYPE
        self.comboScrapingType = ttk.Combobox(self.Main, values=scrapingList)
        self.comboScrapingType.grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.comboScrapingType.set('Cosa vuoi pubblicare')

        # Buttons
        self.startButton = Button(self.Main, text="AVVIA BOT", command=self.insertData, background='red')
        self.startButton.grid(row=10, column=3, padx=5, pady=5, sticky="e")

        self.Main.pack_configure(padx=5, pady=5, ipadx=20, ipady=300)

    def insertData(self):
        if utils.controlInputValue(self.entryIDChannel.get().strip()) & utils.controlInputValue(self.entryAffiliateCode.get().strip()) & utils.controlInputValue(self.entryLinkChannel.get().strip()):
            constant.channel_id = self.entryIDChannel.get().strip()
            constant.affiliateCode = self.entryAffiliateCode.get().strip()
            constant.channelLink = self.entryLinkChannel.get().strip()
            constant.URLS = utils.getScrapingType(self.comboScrapingType.get().strip())
            Thread(target=self.botStart).start()
        else:
            messagebox.showerror("ERRORE", "CAMPI VUOTI")

    def botStart(self):
        try:
            if utils.checkRequirments():
                self.startButton['state'] = DISABLED
                for URL in constant.URLS:
                    scraper.scrapingProducts(URL)
                message.replaceAffiliateLink()
                asyncio.new_event_loop().run_until_complete(message.createTelegramMessage())
                event = Event()
                event.set()
                while True:
                    if event.is_set():
                        break
                message.resetCsv()
                self.startButton['state'] = NORMAL
            else:
                messagebox.showinfo("PROVA", "PERIODO DI PROVA SCADUTO")
        except Exception as e:
            messagebox.showerror("ERRORE", "QUALCOSA E' ANDATO STORTO CONTROLLA I DATI INSERITI O LA CONNESSIONE")
            self.startButton['state'] = NORMAL
            if exists('AmazonWebScraperDataset.csv'):
                message.resetCsv()


scrapingList = ['Elettronica/Informatica', 'Abbigliamento']

if __name__ == '__main__':
    root = Tk()
    root.title('AFFILIATE AMAZON BOT')
    root.configure(background='red')
    root.geometry('600x500')
    window = Window(root)
    root.mainloop()
