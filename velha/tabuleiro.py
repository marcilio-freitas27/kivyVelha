from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button

# telas
from kivy.uix.screenmanager import ScreenManager, Screen

# timer
import time, datetime
from kivy.clock import Clock

# image
from kivy.uix.image import AsyncImage

# sound
from kivy.core.audio import SoundLoader

Builder.load_string('''
<Jogadores>:
    # Nome do jogo
    BoxLayout:
        pos_hint: {'center_x':0.5, 'top':1}
        size_hint: 0.3, 0.3
        orientation: 'vertical'
        # image
        Image:
            source:'kivydavelha.png'
            allow_stretch: False
            size_hint_y: None
        Label:
            text: "Kivy da Velha"
            font_size: 50
    # Escolha do x ou o para os jogadores
    # melhor de 3
    GridLayout:
        cols: 2
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint: 0.8, 0.2
        orientation: 'vertical'
        Label:
            text: "J1: X ou O"
            font_size: 25
        TextInput:
            id: text1
            multiline: False
            font_size: 25
        Label:
            text: "J2: X ou O"
            font_size: 25
        TextInput:
            id: text2
            multiline: False
            font_size: 25
        # linha do melhor de 3
        Label:
            text: "Melhor de:"
            font_size: 25
        TextInput:
            id: text3
            multiline: False
            font_size: 25
    # botão para dar inicio ao jogo
    BoxLayout:
        pos_hint: {'center_x':0.5, 'top':0.3}
        size_hint: 0.2, 0.1
        orientation: 'vertical'
        Button:
            background_color: 0,1,0,1
            font_size: 25
            text: "Start!"
            on_release: root.inserir(self)

<Tabuleiro>:
    # desenho do tabuleiro
    canvas:
        Color:
            #amarelo
            rgb: 1, 1, 0
        Rectangle:
            pos: self.center_x+140, 0
            size: 10, self.height    

        Rectangle:
            pos: self.center_x-140, 0
            size: 10, self.height
            
        Color:
            #verde
            rgb: 0, 1, 0
        Rectangle:
            pos: 0 , self.center_y+110
            size: self.width, 10

        Rectangle:
            pos: 0 , self.center_y-110
            size: self.width, 10

    #score j1
    AnchorLayout:
        anchor_x:'left'
        anchor_y:'top'
        Label:
            id: score1
            text: "0"
            font_size: 35
            size_hint_y: 0.1
            size_hint_x: 0.1
    # timer
    AnchorLayout:
        anchor_x:'center'
        anchor_y:'top'
        Label:
            id: time
            text: "01:00"
            font_size: 35
            size_hint_y: 0.1
            size_hint_x: 0.1
    #score  j2    
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'top'
        Label:
            id: score2
            text: "0"
            font_size: 35
            size_hint_y: 0.1
            size_hint_x: 0.1

    # telas do tabuleiro que recebem x e o
    GridLayout:
        rows: 4
        cols: 3
        Label:
            id: zero
            font_size: 70  
            text: ''
        Label:
            id: one
            font_size: 70  
            text: ''
        Label:
            id: two
            font_size: 70  
            text: ''

        Label:
            id: three
            font_size: 70  
            text: ''
        Label:
            id: four
            font_size: 70  
            text: ''
        Label:
            id: five
            font_size: 70  
            text: ''
        
        Label:
            id: six
            font_size: 70  
            text: ''
        Label:
            id: seven
            font_size: 70  
            text: ''
        Label:
            id: eight
            font_size: 70  
            text: ''
<Tabuleiro2>:
    # desenho do tabuleiro para melhor de 3
    canvas:
        Color:
            #amarelo
            rgb: 1, 1, 0
        Rectangle:
            pos: self.center_x+140, 0
            size: 10, self.height
            
        Rectangle:
            pos: self.center_x-140, 0
            size: 10, self.height
            
        Color:
            #verde
            rgb: 0, 1, 0
        Rectangle:
            pos: 0 , self.center_y+110
            size: self.width, 10
            

        Rectangle:
            pos: 0 , self.center_y-110
            size: self.width, 10
            

    #score j1
    AnchorLayout:
        anchor_x:'left'
        anchor_y:'top'
        Label:
            id: score10
            text: "0"
            font_size: 35
            size_hint_y: 0.1
            size_hint_x: 0.1
    
    #score  j2    
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'top'
        Label:
            id: score20
            text: "0"
            font_size: 35
            size_hint_y: 0.1
            size_hint_x: 0.1

    # telas do tabuleiro que recebem x e o
    GridLayout:
        rows: 4
        cols: 3
        Label:
            id: zero
            font_size: 70  
            text: ''
        Label:
            id: one
            font_size: 70  
            text: ''
        Label:
            id: two
            font_size: 70  
            text: ''

        Label:
            id: three
            font_size: 70 
            text: ''
        Label:
            id: four
            font_size: 70 
            text: ''
        Label:
            id: five
            font_size: 70  
            text: ''
        
        Label:
            id: six
            font_size: 70  
            text: ''
        Label:
            id: seven
            font_size: 70  
            text: ''
        Label:
            id: eight
            font_size: 70  
            text: ''
''')

# variavies do jogo
# jogadores
j1 = ""
j2 = ""
# jogadores para atribuir valor de uma classe para outra
j11 = []
j22 = []

#classe das telas 
class Telas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # menu inicial para escolher simbolo, melhor de 3 ou tempo
        self.add_widget(Jogadores(name="jogadores"))
        # tabuleiro de tempo(timer)
        self.add_widget(Tabuleiro(name="tabuleiro"))
        # tabuleiro do melhor de 3
        self.add_widget(Tabuleiro2(name="tabuleiro2"))

# escolha os jogadores
class Jogadores(Screen):
    # recebe o local onde está o arquivo de áudio
    sound = SoundLoader.load('loopmix.wav')
    # contagem para carregar e mudar página
    contar = 0
    # local da imagem de carregamento de página
    src = 'loading.gif'
    # carrega a imagem
    im = AsyncImage(source=src, allow_stretch=True,size_hint=(0.99,None))
    def __init__(self,**kwargs):
        super(Jogadores, self).__init__(**kwargs)

    def inserir(self, obj):
        # campos para escolhar x ou o e melhor de 3,5 e 10
        #ambos os campos preenchidos
        # configurações para usar o timer
        if self.ids.text1.text.upper() == "x".upper() and self.ids.text2.text.upper() == "o".upper() and self.ids.text3.text == "":
            j11.append(self.ids.text1.text)
            j22.append(self.ids.text2.text)

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)
        
        elif self.ids.text1.text.upper() == "o".upper() and self.ids.text2.text.upper() == "x".upper() and self.ids.text3.text == "":
            j11.append(self.ids.text1.text)
            j22.append(self.ids.text2.text)
        

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)
        
        #ambos os campos vazios
        elif self.ids.text1.text == "" and self.ids.text2.text == "" and self.ids.text3.text == "":
            j11.append("x")
            j22.append("o")
            
            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)

        #j1 os campos preenchido
        elif self.ids.text1.text.upper() == "x".upper() and self.ids.text2.text == "" and self.ids.text3.text == "":
            j11.append(self.ids.text1.text)
            j22.append("o")

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)
        
        elif self.ids.text1.text.upper() == "o".upper() and self.ids.text2.text == "" and self.ids.text3.text == "":
            j11.append(self.ids.text1.text)
            j22.append("x")

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)

        #j2 os campos preenchido
        elif self.ids.text1.text == "" and self.ids.text2.text.upper() == "o".upper() and self.ids.text3.text == "":
            j11.append("x")
            j22.append(self.ids.text2.text)

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)
        
        elif self.ids.text1.text == "" and self.ids.text2.text.upper() == "x".upper() and self.ids.text3.text == "":
            j11.append("o")
            j22.append(self.ids.text2.text)
        
            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais, 0.5)

        
        # melhor de 3
        # campos preenchidos
        elif self.ids.text1.text.upper() == "x".upper() and self.ids.text2.text.upper() == "o".upper() and self.ids.text3.text == "3":
            j11.append(self.ids.text1.text)
            j22.append(self.ids.text2.text)

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)
        
        elif self.ids.text1.text.upper() == "o".upper() and self.ids.text2.text.upper() == "x".upper() and self.ids.text3.text == "3":
            j11.append(self.ids.text1.text)
            j22.append(self.ids.text2.text)
        

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)
        
        #ambos os campos vazios
        elif self.ids.text1.text == "" and self.ids.text2.text == "" and self.ids.text3.text == "3":
            j11.append("x")
            j22.append("o")
            
            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)

        #j1 os campos preenchido
        elif self.ids.text1.text.upper() == "x".upper() and self.ids.text2.text == "" and self.ids.text3.text == "3":
            j11.append(self.ids.text1.text)
            j22.append("o")

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)
        
        elif self.ids.text1.text.upper() == "o".upper() and self.ids.text2.text == "" and self.ids.text3.text == "3":
            j11.append(self.ids.text1.text)
            j22.append("x")

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)

        #j2 os campos preenchido
        elif self.ids.text1.text == "" and self.ids.text2.text.upper() == "o".upper() and self.ids.text3.text == "3":
            j11.append("x")
            j22.append(self.ids.text2.text)

            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)
        
        elif self.ids.text1.text == "" and self.ids.text2.text.upper() == "x".upper() and self.ids.text3.text == "3":
            j11.append("o")
            j22.append(self.ids.text2.text)
        
            self.add_widget(self.im)
            Clock.schedule_interval(self.contarmais2, 0.5)

        # se não atende as opções anteriores
        else:
            popup = Popup(size = (250, 250),title='Atenção:',content=Button(text='Valor incorreto!'),size_hint=(None,None), title_color=(0,1,1,1))
            popup.open()

    # para o som quando o tempo acaba ou quando alguem faz 3 pontos
    def para_som(self):
        self.sound.stop()
    
    # contagem para carregar a imagem de espera/loading
    def contarmais(self,obj):
        self.contar = self.contar + 1
        if self.contar  == 5:
            # remove imagem de carregamento, 
            # para o contador, 
            # zera o contador e passa e para a proxima tela
            self.remove_widget(self.im)
            Clock.unschedule(self.contarmais)
            self.manager.current = "tabuleiro"
            self.contar = 0
            #play sound
            self.sound.play()
            self.sound.loop = True
            self.sound.volume = 0.25

    def contarmais2(self,obj):
        self.contar = self.contar + 1
        if self.contar  == 5:
            # remove imagem de carregamento, 
            # para o contador, 
            # zera o contador e passa e para a proxima tela
            self.remove_widget(self.im)
            Clock.unschedule(self.contarmais2)
            self.manager.current = "tabuleiro2"
            self.contar = 0
            #play sound
            self.sound.play()
            self.sound.loop = True
            self.sound.volume = 0.25

# variável das jogadas
c = 0
class Tabuleiro(Screen):
    # variável contadora
    count = 59 + 1
    def __init__(self,**kwargs):
        super(Tabuleiro, self).__init__(**kwargs)

    # quando muda da tela jogadores para tabuleiro o timer inicia 
    def on_pre_enter(self):
        self.clock_start()
        
    # chamar o metodo para iniciar o timer
    def clock_start(self):
        Clock.schedule_interval(self.callback_clock,0.5)

    
    # parar o contador nas seguintes condições, voltar para a tela de jogadores e indicar os ganhadores
    def callback_clock(self, dt):
        # instanciando a classe Jogadores para usar um dos seus módulos/funções/def
        jogadores = Jogadores()
        # subitração para criar a contagem
        self.count = self.count-1
        # exibir o tempo em formado de horas e minutos
        self.ids.time.text = str(datetime.time(minute=self.count).isoformat(timespec='minutes'))
        # quando o tempo acaba o resultado é mostrado
        if self.count == 0:
            Clock.unschedule(self.callback_clock)
            if int(self.ids.score1.text) > int(self.ids.score2.text) :
                content = Button(text='j1 ganhou!')
                popup = Popup(size = (250, 250),title='Resultado',content=content,size_hint=(None,None), title_color=(0,1,1,1))
                content.bind(on_release=popup.dismiss)
                popup.open()
            
            elif int(self.ids.score1.text) < int(self.ids.score2.text):
                content = Button(text='j2 ganhou!')
                popup = Popup(size = (250, 250),title='Resultado',content=content,size_hint=(None,None), title_color=(0,1,1,1))
                content.bind(on_release=popup.dismiss)
                popup.open()

            else:
                content = Button(text='Empate!')
                popup = Popup(size = (250, 250),title='Resultado',content=content,size_hint=(None,None), title_color=(0,1,1,1))
                content.bind(on_release=popup.dismiss)
                popup.open()

            # zerar tudo 
            jogadores.para_som()
            self.manager.current = "jogadores"    
            self.ids.score1.text = "0"
            self.ids.score2.text = "0"
            self.ids.time.text = "01:00"
            self.count = 59 + 1
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            j11.clear()
            j22.clear()
            c=0
        

    # if a label is touched/collide insert a simbol of tic-tac-toy
    # condições de toque nas telas para inserir os simbolos e determinar quais as jogadas(c)
    def on_touch_down(self, touch):
        global c
        j1 = j11[0]
        j2 = j22[0]
        # primeira jogada
        if c == 0:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        # segunda jogada
        elif c == 1:           
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1
        
        # terceira jogada
        elif c == 2:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        # quarta jogada
        elif c == 3:            
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1
        
        # quinta jogada
        elif c == 4:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        # sexta jogada
        elif c == 5:    
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1

        # setima jogada
        elif c == 6:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        # oitava jogada
        elif c == 7:          
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1

        # utlima jogada
        elif c == 8:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1


        # digonal 1
        # adicionando condições para vitória do jogar relacionado ao seu símbolo
        # x
        if self.ids.two.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.six.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
            
        # o
        if self.ids.two.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.six.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)

            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #diagonal 2
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
        
        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
        
        # horizontal 1
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.one.text.upper() == "x".upper() and self.ids.two.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.one.text.upper() == "o".upper() and self.ids.two.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #horizontal 2
        # x
        if self.ids.three.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.five.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.three.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.five.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #horizontal 3
        # x
        if self.ids.six.text.upper() == "x".upper() and self.ids.seven.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.six.text.upper() == "o".upper() and self.ids.seven.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # vertical 1
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.three.text.upper() == "x".upper() and self.ids.six.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.three.text.upper() == "o".upper() and self.ids.six.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #vertical 2
        # x
        if self.ids.one.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.seven.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.one.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.seven.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #vertical 3
        # x
        if self.ids.two.text.upper() == "x".upper() and self.ids.five.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.two.text.upper() == "o".upper() and self.ids.five.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score1.text = str(int(self.ids.score1.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score2.text = str(int(self.ids.score2.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # draw
        if c > 8:
            content = Button(text='Deu velha kkk... XD')
            popup = Popup(size = (250, 250),title='Resultado:',content=content,size_hint=(None,None), title_color=(0,1,1,1),auto_dismiss=False)
            content.bind(on_release=popup.dismiss)
            popup.open()
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

class Tabuleiro2(Screen):
    count = 59+1
    def __init__(self,**kwargs):
        super(Tabuleiro2, self).__init__(**kwargs)

    # if a label is touched/collide insert a simbol of tic-tac-toy
    # condições de toque nas telas para inserir os simbolos e determinar quais as jogadas(c)
    def on_touch_down(self, touch):
        global c
        j1 = j11[0]
        j2 = j22[0]
        if c == 0:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        elif c == 1:           
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1
            
        elif c == 2:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        elif c == 3:            
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1
        
        elif c == 4:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        elif c == 5:    
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1

        elif c == 6:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        elif c == 7:          
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j2
                    c+=1
        
            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j2
                    c+=1
            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j2
                    c+=1
            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j2
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j2
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j2
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j2
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j2
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j2
                    c+=1

        elif c == 8:
            if self.ids.zero.collide_point(*touch.pos):
                if self.ids.zero.text == "":
                    self.ids.zero.text = j1
                    c+=1

            elif self.ids.one.collide_point(*touch.pos):
                if self.ids.one.text == "":
                    self.ids.one.text = j1
                    c+=1

            elif self.ids.two.collide_point(*touch.pos):
                if self.ids.two.text == "":
                    self.ids.two.text = j1
                    c+=1

            elif self.ids.three.collide_point(*touch.pos):
                if self.ids.three.text == "":
                    self.ids.three.text = j1
                    c+=1

            elif self.ids.four.collide_point(*touch.pos):
                if self.ids.four.text == "":
                    self.ids.four.text = j1
                    c+=1

            elif self.ids.five.collide_point(*touch.pos):
                if self.ids.five.text == "":
                    self.ids.five.text = j1
                    c+=1

            elif self.ids.six.collide_point(*touch.pos):
                if self.ids.six.text == "":
                    self.ids.six.text = j1
                    c+=1

            elif self.ids.seven.collide_point(*touch.pos):
                if self.ids.seven.text == "":
                    self.ids.seven.text = j1
                    c+=1

            elif self.ids.eight.collide_point(*touch.pos):
                if self.ids.eight.text == "":
                    self.ids.eight.text = j1
                    c+=1

        #elif self.count == 0:
        #    c = 0

        # digonal 1
        # adicionando condições para vitória do jogar relacionado ao seu símbolo
        # x
        if self.ids.two.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.six.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
            
        # o
        if self.ids.two.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.six.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)

            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #diagonal 2
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
        
        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
        
        # horizontal 1
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.one.text.upper() == "x".upper() and self.ids.two.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.one.text.upper() == "o".upper() and self.ids.two.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #horizontal 2
        # x
        if self.ids.three.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.five.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.three.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.five.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #horizontal 3
        # x
        if self.ids.six.text.upper() == "x".upper() and self.ids.seven.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.six.text.upper() == "o".upper() and self.ids.seven.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # vertical 1
        # x
        if self.ids.zero.text.upper() == "x".upper() and self.ids.three.text.upper() == "x".upper() and self.ids.six.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.zero.text.upper() == "o".upper() and self.ids.three.text.upper() == "o".upper() and self.ids.six.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #vertical 2
        # x
        if self.ids.one.text.upper() == "x".upper() and self.ids.four.text.upper() == "x".upper() and self.ids.seven.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.one.text.upper() == "o".upper() and self.ids.four.text.upper() == "o".upper() and self.ids.seven.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        #vertical 3
        # x
        if self.ids.two.text.upper() == "x".upper() and self.ids.five.text.upper() == "x".upper() and self.ids.eight.text.upper() == "x".upper():
            if j1.upper() == "x".upper(): 
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)

            if j2.upper() == "x".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # o
        if self.ids.two.text.upper() == "o".upper() and self.ids.five.text.upper() == "o".upper() and self.ids.eight.text.upper() == "o".upper():
            if j1.upper() == "o".upper():
                self.ids.score10.text = str(int(self.ids.score10.text) + 1)
            
            if j2.upper() == "o".upper():
                self.ids.score20.text = str(int(self.ids.score20.text) + 1)
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0

        # draw
        if c > 8:
            content = Button(text='Deu velha kkk... XD')
            popup = Popup(size = (250, 250),title='Resultado:',content=content,size_hint=(None,None), title_color=(0,1,1,1),auto_dismiss=False)
            content.bind(on_release=popup.dismiss)
            popup.open()
    
            # clear all labels text: restart de game
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            c=0
        
        jogadores = Jogadores(
        if self.ids.score10.text == "3":
            content = Button(text='j1 ganhou!')
            popup = Popup(size = (250, 250),title='Resultado',content=content,size_hint=(None,None), title_color=(0,1,1,1))
            content.bind(on_release=popup.dismiss)
            popup.open()

            jogadores.para_som()
            self.manager.current = "jogadores"    
            self.ids.score10.text = "0"
            self.ids.score20.text = "0"
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            j11.clear()
            j22.clear()
            c=0
            

        elif self.ids.score20.text == "3":
            content = Button(text='j2 ganhou!')
            popup = Popup(size = (250, 250),title='Resultado',content=content,size_hint=(None,None), title_color=(0,1,1,1))
            content.bind(on_release=popup.dismiss)
            popup.open()
        
            jogadores.para_som()
            self.manager.current = "jogadores"    
            self.ids.score10.text = "0"
            self.ids.score20.text = "0"
            self.ids.zero.text = ""
            self.ids.one.text = ""
            self.ids.two.text = ""
            self.ids.three.text = ""
            self.ids.four.text = ""
            self.ids.five.text = ""
            self.ids.six.text = ""
            self.ids.seven.text = ""
            self.ids.eight.text = ""
            j11.clear()
            j22.clear()
            c=0
            

# inicar o jogo
class KivyDaVelha(App):
    def build(self):
        telas = Telas()
        return telas

if __name__ == "__main__":
    KivyDaVelha().run()


