from manimlib.imports import *
import numpy as np

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

class MemorySlot():
    def __init__(self, address, text, scale=0.5):
        self.scale = scale
        self.rectangle = Rectangle(height=1*scale, width=3*scale)
        self.text = TextMobject(str(text))
        self.label = TextMobject(str(address))
        self.label.scale(scale)
        self.realign_text_and_label()
    
    def set_text(self, text):
        self.prev_text = self.text
        self.text = TextMobject(str(text))
        self.realign_text()

    def realign_text_and_label(self):
        self.realign_text()
        self.realign_label()

    def realign_text(self):
        self.text.move_to(self.rectangle.get_center())

    def realign_label(self):
        self.label.move_to(self.rectangle.get_right() + RIGHT * self.scale)

    def to_edge(self, edge=LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER):
        self.rectangle.to_edge(edge, buff)
        self.realign_text_and_label()

    def move_to(self, pos, aligned_edge=ORIGIN):
        self.rectangle.move_to(pos, aligned_edge)
        self.realign_text_and_label()
    
    def shift(self, dir):
        self.rectangle.shift(dir * self.scale)
        self.realign_text_and_label()

class Stack(Scene):
    def construct(self):
        # building the stack
        to_play = []
        stack = []
        baseaddr = 16 ** 3
        for i in range(4):
            hex_addr = hex(baseaddr + 8 * i)
            if i == 3:
                hex_addr = "\\vdots"
            memslot = MemorySlot(hex_addr, "", scale=1)
            memslot.to_edge(TOP, buff=0.5)
            memslot.shift(DOWN * i)
            memslot.shift(2 * RIGHT)
            stack.append(memslot)
            to_play.append(ShowCreation(memslot.rectangle))
            to_play.append(Write(memslot.label))

        self.play(*to_play)
        self.wait(2)

        # first arrow
        arrow_main = Arrow(LEFT, RIGHT)
        arrow_main.move_to(stack[0].rectangle.get_left() + LEFT)
        text_main = TextMobject("\\texttt{{main}} függvény")
        text_main.move_to(arrow_main.get_left() + 2 * LEFT)

        # second arrow
        arrow_inner = Arrow(LEFT, RIGHT)
        arrow_inner.move_to(stack[1].rectangle.get_left() + LEFT)
        text_inner = TextMobject("belső blokk")
        text_inner.move_to(arrow_inner.get_left() + 2 * LEFT)

        # third arrow
        arrow_func = Arrow(LEFT, RIGHT)
        arrow_func.move_to(stack[2].rectangle.get_left() + LEFT)
        text_func = TextMobject("\\texttt{{f}} függvény")
        text_func.move_to(arrow_func.get_left() + 2 * LEFT)

        stack[0].set_text("x: 2")
        self.play(Write(stack[0].text),
                  ShowCreation(arrow_main),
                  Write(text_main))
        self.wait(1)

        stack[1].set_text("x: 3")
        self.play(Write(stack[1].text),
                  ShowCreation(arrow_inner),
                  Write(text_inner))
        self.wait(1)

        stack[1].set_text("x: 6")
        self.play(Transform(stack[1].prev_text, stack[1].text))
        self.wait(1)

        stack[2].set_text("x: 6")
        stack[2].text.move_to(stack[1].text.get_center())
        self.add(stack[2].text)
        self.play(ApplyMethod(stack[2].text.move_to, stack[2].rectangle.get_center()),
                  ShowCreation(arrow_func),
                  Write(text_func))
        self.wait(1)

        stack[2].set_text("x: 13")
        self.play(Transform(stack[2].prev_text, stack[2].text))
        self.wait(1)

        self.play(FadeOut(stack[2].text),
                  FadeOut(stack[2].prev_text),
                  FadeOut(arrow_func),
                  FadeOut(text_func))
        self.wait(1)

        self.play(FadeOut(stack[1].text),
                  FadeOut(stack[1].prev_text),
                  FadeOut(arrow_inner),
                  FadeOut(text_inner))
        self.wait(1)

        stack[0].set_text("x: 3")
        self.play(Transform(stack[0].prev_text, stack[0].text))
        self.wait(1)

        self.play(FadeOut(stack[0].text),
                  FadeOut(stack[0].prev_text),
                  FadeOut(arrow_main),
                  FadeOut(text_main))
        self.wait(1)
