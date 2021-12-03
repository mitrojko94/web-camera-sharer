from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder  #Za rad sa ucitavanjem fajlova
import time
from kivy.core.clipboard import Clipboard  #Ovu klasu koristimo da kopiramo nesto
from filesharer import FileSharer
import webbrowser  #Ova biblioteka nam sluzi za otvaranje slike na internetu

Builder.load_file("frontend.kv")  #Povezuje py fajl sa kivy fajlom


class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button text"""
        self.ids.camera.opacity = 1  #Na ovaj nacin smo napravili da se kamera pojavi kada pritisnemo dugme start
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"  #Na ovaj nacin smo napravili da kad ukljucimo kameru pise da je ugasimo
        self.ids.camera.texture = self.ids.camera._camera.texture  #Ovako smo namestili da kada ukljucimo kameru, posle iskljucenja, imamo opet sliku na ekranu

    def stop(self):
        """Stops camera and changes Button text"""
        self.ids.camera.opacity = 0  #Kad ugasimo kameru da ne bi bila bela pozadina, zbog toga smo stavili ovo, onda ce da bude crna
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None  #Na ovaj nacin kada ugasimo kameru brise se cela slika, tj. frejm, jer je texture = None  

    def capture(self):
        """Creates a filename with the current time and captures and saves a photo image under that filename"""
        current_time = time.strftime("%Y%m%d-%H%M%S")  #string from time(oznaka za to je %Y godina, %m mesec, %d dan - %H sati, %M minuti, %S sekunde)
        self.filepath = f"files/{current_time}.png"  #Napravili smo da na svaku sliku(kantonacija), koja ima ekstenziju dodajemo vreme i tako ce nam pisati kad je slika skinuta. To svo dodali na files, jer je to folder gde smestamo nase slike
        self.ids.camera.export_to_png(self.filepath)  #Na ovaj nacin mozemo da uhvatimo tj. snimomo deo slike koji hocemo i ta slika ce nam se pojaviti u nasem direktorijumu pod imenom image.png, jer smo je tako definisali
        self.manager.current = "image_screen"  #Ovaj image_screen je id ImageScreen, definisan u frontend.kv
        self.manager.current_screen.ids.img.source = self.filepath  #Ovde nam je image_screen zapravo current_screen i ovo nam omogucava da kada snimimo sliku da se ta slika prebaci na drugi ekran

        #self.ids daje pristup vidzetima klase gde je kod napisan, tipa camera.play
        #self.manager daje pristup vidzetima trenutnog ekrana koji korisnik koristi
        #dodali smo self.filepath da bi mogli da pristupimo putanji iz klase ImageScreen

class ImageScreen(Screen):
    link_message = "Create a Link First"  #Ovo je klasna metoda, da ne bi ponavljali kod, samo je u metodi u kojoj je zelimo, pozovemo, tipa self.link_message u ovom slucaju

    def create_link(self):
        """Accesses the photo filepath, uploads it to the web and inserts the link in the label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath  #Na ovaj nacin mozemo da pristupimo metodu capture, klase CameraScreen. get_running_app() je metoda klase App, a root je klasa CameraScreen.ids.id camera_screen(jer smo tako definisali u frontend.kv) i onda pristupimo cemu hocemo, to je u ovom slucaju filepath
        filesharer = FileSharer(filepath=file_path)  #Importujemo klasu FileSharer, prosledimo joj kao argument nasu putanju, koju smo definisali u kodu iznad(to je nasa slika)
        self.url = filesharer.share()  #funkcijom share je delimo na internet
        self.ids.link.text = self.url

        #self.url smo stavili da bi mogli da iz druge metode pristupimo tom elementu

    def copy_link(self):
        """Copy link to the clipboard available for pasting"""
        try:
            Clipboard.copy(self.url)  #Samo smo pozvali samo klasu Clipboard i dodelili joj funkciju copy, a ona kao parametar uzima sta hocemo da kopiramo, a to je u ovom slucaju nas link
        except:
            self.ids.link.text = self.link_message  #Ovde smo uveli try/except block, koji nam govori da ako funkcija u try bloku ne radi, izvrsi se kod u except bloku, a tu smo stavili da nam izbaci tekst, tako sto smo pristupili ids.text(id labele, a text je njeno polje)

    def open_link(self):
        """Open link with default browser"""
        try:
            webbrowser.open(self.url)  #importujemo biblioteku, njenu metodu open kojom prosledjujemo argument koji zelimo da otvorimo, a to je u ovom slucaju nas link
        except:
            self.ids.link.text = self.link_message
            

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    
    def build(self):
        return RootWidget()

MainApp().run()