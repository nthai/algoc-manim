from manimlib.imports import *

class CodeText(Text):
    CONFIG = {
        "font": "Consolas"
    }

class Code():
    def __init__(self):
        self.base_addr = 16*16*16
        self.scale = 0.5
        self.original_code = [
            CodeText("void print_array(int* arr, int size) {"),
            CodeText("    if (size == 0) return;"),
            CodeText("    printf(\"%d \", *arr);"),
            CodeText("    print_array(arr + 1, size - 1);"),
            CodeText("}")
        ]

        for idx, code in enumerate(self.original_code):
            code.scale(self.scale)
            code.to_corner(UL)
            code.shift(self.scale * idx * DOWN)

        self.subcode = [
            CodeText(f"void print_array({hex(self.base_addr)}, {4}) {{"),
            CodeText(f"    if ({4} == 0) return;"),
            CodeText(f"    printf(\"%d \", *({hex(self.base_addr)}));"),
            CodeText(f"    print_array({hex(self.base_addr + 8)}, {3});")
        ]

        for idx, code in enumerate(self.subcode):
            code.scale(self.scale)
            code.to_corner(UL)
            code.shift(self.scale * idx * DOWN)

        self.blocks = []
        for i in range(4):
            rec_block = [
                CodeText(" "*4*(i+1) + f"    if ({3 - i} == 0) return;"),
                CodeText(" "*4*(i+1) + f"    printf(\"%d \", *({hex(self.base_addr + 8*(i+1))}));"),
                CodeText(" "*4*(i+1) + f"    print_array({hex(self.base_addr + 8*(i+2))}, {2 - i});"),
                CodeText(" "*4*(i+1) + f"}}")
            ]
            for j, code in enumerate(rec_block):
                code.scale(self.scale)
                code.to_corner(UL)
                code.shift(self.scale * (4 + j + 3*i) * DOWN)
            self.blocks.append(rec_block)

class MemorySlot():
    def __init__(self, address, text, scale=0.5):
        self.scale = scale
        self.rectangle = Rectangle(height=1*scale, width=3*scale)
        self.text = TextMobject(str(text))
        self.text.scale(scale)
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

    def to_corner(self, edge=LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER):
        self.rectangle.to_corner(edge, buff)
        self.realign_text_and_label()

    def move_to(self, pos, aligned_edge=ORIGIN):
        self.rectangle.move_to(pos, aligned_edge)
        self.realign_text_and_label()
    
    def shift(self, dir):
        self.rectangle.shift(dir * self.scale)
        self.realign_text_and_label()

MAGIC_NUMBER = 0.53

class Array(Scene):
    def construct(self):
        to_play = []

        # create numbers
        nums = [9, 3, 0, 3]
        num_objs = []
        for idx, num in enumerate(nums):
            num_obj = TextMobject(str(num))
            num_obj.to_edge(DOWN, buff=2)
            num_obj.shift(1.5*LEFT + idx*RIGHT)
            num_objs.append(num_obj)

        code = Code()
        # write the code
        for c in code.original_code:
            to_play.append(Write(c))

        # create memory image
        data_base_addr = 16*16*16
        data_stack = []
        for i in range(15):
            hex_addr = hex(data_base_addr + 8 * i)
            text = None
            if i < 4:
                text = f"arr[{i}]: {nums[i]}"
            elif i == 4:
                text = "\\vdots"
                hex_addr = "\\vdots"
            else:
                if i % 2 == 0:
                    text = f"{4 - (i - 6) // 2}"
                else:
                    text = hex(data_base_addr + 8 * ((i - 5) // 2))
                hex_addr = hex(data_base_addr + 9*16*16*16 + 8 * (i-5))
            memslot = MemorySlot(hex_addr, text, scale=0.5)
            memslot.to_corner(UR)
            memslot.shift(0.3 * UP)
            memslot.shift(DOWN * i)
            memslot.shift(2 * LEFT)
            data_stack.append(memslot)
            if i != 4:
                to_play.append(ShowCreation(memslot.rectangle))
            to_play.append(Write(memslot.label))
            if i <= 4:
                to_play.append(Write(memslot.text))

        # create arrow
        arrow = Arrow(ORIGIN, 0.8*RIGHT,
                      stroke_width=20,
                      max_tip_length_to_length_ratio=0.5,
                      max_stroke_width_to_length_ratio=10)
        arrow.move_to(code.original_code[0].get_left() + 0.25 * LEFT)
        to_play.append(ShowCreation(arrow))

        # create brace
        mem_group = VGroup(data_stack[5].rectangle, data_stack[6].rectangle)
        brace = Brace(mem_group, LEFT)

        self.play(*to_play)
        self.wait(1)

        # substitute values into variables
        for i in range(4):
            to_play = [FadeOut(code.original_code[i], DOWN),
                       FadeIn(code.subcode[i], UP)]
            if i != 0:
                # shift down arrow
                to_play.append(ApplyMethod(arrow.shift, code.scale*DOWN))
            else:
                # display values in memory
                to_play.append(FadeIn(data_stack[5].text))
                to_play.append(FadeIn(data_stack[6].text))
                to_play.append(ShowCreation(brace))
            self.play(*to_play)
            self.wait(1)
            if i == 2:
                self.play(Write(num_objs[0]))
        
        # fade in new code and shift down brace
        to_play = [ApplyMethod(code.original_code[4].shift, code.scale*4*DOWN)]
        for c in code.blocks[0]:
            to_play.append(FadeIn(c))
        to_play.append(FadeIn(data_stack[7].text))
        to_play.append(FadeIn(data_stack[8].text))
        to_play.append(ApplyMethod(brace.shift, DOWN))
        self.play(*to_play)

        # shift code diagonally into the corner
        diagonal_shift = code.scale*3*UP + MAGIC_NUMBER*LEFT
        to_play = [ApplyMethod(code.original_code[4].shift, diagonal_shift)]
        for c in code.subcode:
            to_play.append(ApplyMethod(c.shift, diagonal_shift))
        for c in code.blocks[0]:
            to_play.append(ApplyMethod(c.shift, diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale*3*UP))
        self.play(*to_play)

        # move arrow and print number
        for i in range(3):
            to_play = []
            to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN))
            if i == 2:
                self.play(Write(num_objs[1]))
            self.play(*to_play)

        # fade in next code and shift down brace
        to_play = []
        for c in code.blocks[1]:
            c.shift(diagonal_shift)
            to_play.append(FadeIn(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*DOWN))
        to_play.append(FadeIn(data_stack[9].text))
        to_play.append(FadeIn(data_stack[10].text))
        to_play.append(ApplyMethod(brace.shift, DOWN))
        self.play(*to_play)

        # shift everythin diagonally again and shift arrow up
        to_play = []
        for c in code.blocks[0] + code.blocks[1] + code.subcode + [code.original_code[-1]]:
            to_play.append(ApplyMethod(c.shift, diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale*3*UP))
        self.play(*to_play)

        # move arrow and print number
        for i in range(3):
            to_play = []
            to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN))
            if i == 2:
                self.play(Write(num_objs[2]))
            self.play(*to_play)

        # fade in next code
        to_play = []
        for c in code.blocks[2]:
            c.shift(diagonal_shift * 2)
            to_play.append(FadeIn(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[1][-1].shift, code.scale*4*DOWN))
        to_play.append(FadeIn(data_stack[11].text))
        to_play.append(FadeIn(data_stack[12].text))
        to_play.append(ApplyMethod(brace.shift, DOWN))
        self.play(*to_play)

        # shift again
        to_play = []
        for c in code.blocks[0] + code.blocks[1] + code.blocks[2] + code.subcode + [code.original_code[-1]]:
            to_play.append(ApplyMethod(c.shift, diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale*3*UP))
        self.play(*to_play)

        # move arrow and print number
        for i in range(3):
            to_play = []
            to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN))
            if i == 2:
                self.play(Write(num_objs[3]))
            self.play(*to_play)

        # fade in final
        to_play = []
        for c in code.blocks[3]:
            c.shift(diagonal_shift * 3)
            to_play.append(FadeIn(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[1][-1].shift, code.scale*4*DOWN))
        to_play.append(ApplyMethod(code.blocks[2][-1].shift, code.scale*4*DOWN))

        to_play.append(FadeIn(data_stack[13].text))
        to_play.append(FadeIn(data_stack[14].text))
        to_play.append(ApplyMethod(brace.shift, DOWN))
        self.play(*to_play)

        # shift arrow down
        self.play(ApplyMethod(arrow.shift, code.scale * DOWN))
        self.wait(1)

        # shift arrow to end of code
        self.play(ApplyMethod(arrow.shift, code.scale * DOWN * 3))
        self.wait(1)

        # fade out code and shift arrow back
        to_play = []
        to_play.append(ApplyMethod(arrow.shift, code.scale * UP * 4))
        for c in code.blocks[3]:
            to_play.append(FadeOut(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[1][-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[2][-1].shift, code.scale*4*UP))

        to_play.append(FadeOut(data_stack[13].text))
        to_play.append(FadeOut(data_stack[14].text))
        to_play.append(ApplyMethod(brace.shift, UP))

        self.play(*to_play)
        self.wait(1)

        self.play(ApplyMethod(arrow.shift, code.scale * DOWN))

        # shift code back
        to_play = []
        for c in code.blocks[0] + code.blocks[1] + code.blocks[2] + code.subcode + [code.original_code[-1]]:
            to_play.append(ApplyMethod(c.shift, -diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN * 3))
        self.play(*to_play)

        # fade out code and shift arrow back
        to_play = []
        to_play.append(ApplyMethod(arrow.shift, code.scale * UP * 4))
        for c in code.blocks[2]:
            to_play.append(FadeOut(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[1][-1].shift, code.scale*4*UP))

        to_play.append(FadeOut(data_stack[11].text))
        to_play.append(FadeOut(data_stack[12].text))
        to_play.append(ApplyMethod(brace.shift, UP))
        self.play(*to_play)

        self.play(ApplyMethod(arrow.shift, code.scale * DOWN))
        # shift code back
        to_play = []
        for c in code.blocks[0] + code.blocks[1] + code.subcode + [code.original_code[-1]]:
            to_play.append(ApplyMethod(c.shift, -diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN * 3))
        self.play(*to_play)

        # fade out code
        to_play = []
        to_play.append(ApplyMethod(arrow.shift, code.scale * UP * 4))
        for c in code.blocks[1]:
            to_play.append(FadeOut(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*UP))
        to_play.append(ApplyMethod(code.blocks[0][-1].shift, code.scale*4*UP))

        to_play.append(FadeOut(data_stack[9].text))
        to_play.append(FadeOut(data_stack[10].text))
        to_play.append(ApplyMethod(brace.shift, UP))
        self.play(*to_play)

        self.play(ApplyMethod(arrow.shift, code.scale * DOWN))
        # shift code back
        to_play = []
        for c in code.blocks[0] + code.subcode + [code.original_code[-1]]:
            to_play.append(ApplyMethod(c.shift, -diagonal_shift))
        to_play.append(ApplyMethod(arrow.shift, code.scale * DOWN * 3))
        self.play(*to_play)

        # fade out code
        to_play = []
        to_play.append(ApplyMethod(arrow.shift, code.scale * UP * 4))
        for c in code.blocks[0]:
            to_play.append(FadeOut(c))
        to_play.append(ApplyMethod(code.original_code[-1].shift, code.scale*4*UP))

        to_play.append(FadeOut(data_stack[7].text))
        to_play.append(FadeOut(data_stack[8].text))
        to_play.append(ApplyMethod(brace.shift, UP))
        self.play(*to_play)

        self.play(ApplyMethod(arrow.shift, code.scale * DOWN))

        to_play = []
        for c in code.subcode:
            to_play.append(FadeOut(c))
        for idx, c in enumerate(code.original_code):
            if idx != 4:
                to_play.append(FadeIn(c))
        to_play.append(FadeOut(data_stack[5].text))
        to_play.append(FadeOut(data_stack[6].text))
        to_play.append(FadeOut(brace))
        self.play(*to_play)

        self.wait(3)