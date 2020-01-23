from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<Tabuleiro>:
    canvas:
        Rectangle:
            pos: self.center_x+140, 0
            size: 10, self.height
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgb:(0,1,0)

        Rectangle:
            pos: self.center_x-140, 0
            size: 10, self.height
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgb:(0,1,0)
        
        Rectangle:
            pos: 0 , self.center_y+110
            size: self.width, 10
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgb:(0,1,0)

        Rectangle:
            pos: 0 , self.center_y-110
            size: self.width, 10
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgb:(0,1,0)

    GridLayout:
        rows: 3
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

j1 = "x"
j2 = "o"
c = 0
class Tabuleiro(BoxLayout):
    def __init__(self, **kwargs):
        super(Tabuleiro, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        # c = 0 needs stay out because when you touch down a label c in def not grow up +1. 
        # It turn c = 0 again and again. That is the def.   
        global c
        # player 1 = j1 
        if c == 0 or c == 2 or c == 4 or c == 6 or c ==8:
            # if a label is touched/collide insert a simbol(text) in tic-tac-toe screen
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

        #player 2 = j2
        if c == 1 or c == 3 or c == 5 or c == 7:            
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

        # Victory Conditions
        # x
        if self.ids.two.text == "x" and self.ids.four.text == "x" and self.ids.six.text == "x" or self.ids.zero.text == "x" and self.ids.four.text == "x" and self.ids.eight.text == "x" or self.ids.zero.text == "x" and self.ids.one.text == "x" and self.ids.two.text == "x" or self.ids.three.text == "x" and self.ids.four.text == "x" and self.ids.five.text == "x" or self.ids.six.text == "x" and self.ids.seven.text == "x" and self.ids.eight.text == "x" or self.ids.zero.text == "x" and self.ids.three.text == "x" and self.ids.six.text == "x" or self.ids.one.text == "x" and self.ids.four.text == "x" and self.ids.seven.text == "x" or self.ids.two.text == "x" and self.ids.five.text == "x" and self.ids.eight.text == "x":
            popup = Popup(size = (250, 250),title='Resultado:',content=Label(text='O jogador 1(X) ganhou!'),size_hint=(None,None), title_color=(0,1,1,1))
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
        
        # o
        elif self.ids.two.text == "o" and self.ids.four.text == "o" and self.ids.six.text == "o" or self.ids.zero.text == "o" and self.ids.four.text == "o" and self.ids.eight.text == "o" or self.ids.zero.text == "o" and self.ids.one.text == "o" and self.ids.two.text == "o" or self.ids.three.text == "o" and self.ids.four.text == "o" and self.ids.five.text == "o" or self.ids.six.text == "o" and self.ids.seven.text == "o" and self.ids.eight.text == "o" or self.ids.zero.text == "o" and self.ids.three.text == "o" and self.ids.six.text == "o" or self.ids.one.text == "o" and self.ids.four.text == "o" and self.ids.seven.text == "o" or self.ids.two.text == "o" and self.ids.five.text == "o" and self.ids.eight.text == "o":
            popup = Popup(size = (250, 250),title='Resultado:',content=Label(text='O jogador 2(O) ganhou!'),size_hint=(None,None), title_color=(0,1,1,1))
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

        # draw game, no more moves
        elif c > 8:
            popup = Popup(size = (250, 250),title='Resultado:',content=Label(text='Deu velha kkk... XD'),size_hint=(None,None), title_color=(0,1,1,1))
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

class Iniciar(App):
    def build(self):
        return Tabuleiro()

if __name__ == "__main__":
    Iniciar().run()
