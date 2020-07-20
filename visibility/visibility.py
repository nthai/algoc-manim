from manimlib.imports import *

class Code():
    def __init__(self, scale=0.5, linediff=0.4):
        self.codelines = []
        self.scale = scale
        self.linediff = linediff

    def append(self, text):
        # print(text)
        text_obj = Text(text, font="Consolas")
        text_obj.scale(self.scale) # it's important to scale before move
        text_obj.to_corner(UL, buff=0.5)
        text_obj.shift(self.linediff * DOWN * len(self.codelines))
        self.codelines.append(text_obj)

class Visibility(Scene):
    def construct(self):
        code = Code()
        with open("code.c") as codefile:
            for idx, line in enumerate(codefile):
                if line.endswith("\n"):
                    line = line[:-1]
                code.append(line)

        arrow = Arrow(LEFT, 0.15 * RIGHT)
        arrow.next_to(code.codelines[5].get_left() + LEFT)
            
        self.play(*[Write(x) for x in code.codelines],
                  ShowCreation(arrow))



        
