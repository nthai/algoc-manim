from manimlib.imports import *
import numpy as np

class LinkedListNode():
    def __init__(self, scale=.5):
        self.data = Rectangle(width=scale*3, height=scale*2)
        self.next = Rectangle(width=scale*3, height=scale*1).next_to(self.data, DOWN, buff=0)

    def shift(self, pos):
        self.data.shift(pos)
        self.next.shift(pos)

class MyCurvedLine(Line):
    def fit1(self):
        start = self.points[0]
        end = self.points[3]

        bezier_anchor1 = np.zeros(3)
        bezier_anchor2 = np.zeros(3)

        bezier_anchor1[0] = end[0]
        bezier_anchor1[1] = start[1]

        bezier_anchor2[0] = start[0]
        bezier_anchor2[1] = end[1]

        self.points[1] = bezier_anchor1
        self.points[2] = bezier_anchor2

    def fit2(self):
        start = self.points[0]
        end = self.points[3]

        bezier_anchor1 = np.zeros(3)
        bezier_anchor2 = np.zeros(3)

        bezier_anchor1[0] = start[0]
        bezier_anchor1[1] = end[1]

        bezier_anchor2[0] = end[0]
        bezier_anchor2[1] = start[1]

        self.points[1] = bezier_anchor1
        self.points[2] = bezier_anchor2

    def fit3(self):
        start = self.points[0]
        end = self.points[3]

        bezier_anchor1 = np.zeros(3)
        bezier_anchor2 = np.zeros(3)

        bezier_anchor1[0] = end[0]
        bezier_anchor1[1] = start[1]

        bezier_anchor2[0] = end[0]
        bezier_anchor2[1] = start[1]

        self.points[1] = bezier_anchor1
        self.points[2] = bezier_anchor2

    def fit4(self):
        start = self.points[0]
        end = self.points[3]

        bezier_anchor1 = np.zeros(3)
        bezier_anchor2 = np.zeros(3)

        bezier_anchor1[0] = start[0]
        bezier_anchor1[1] = end[1]

        bezier_anchor2[0] = start[0]
        bezier_anchor2[1] = end[1]

        self.points[1] = bezier_anchor1
        self.points[2] = bezier_anchor2

class Reverse(Scene):
    def __init__(self, *args, **kwargs):
        self.to_play = []
        super().__init__(*args, **kwargs)

    def play_to_play(self):
        self.play(*self.to_play)
        self.wait(1)
        self.to_play = []

    def create_line_anchors(self):
        self.line_anchors = []
        for idx in range(4):
            dot = Dot()
            dot.move_to(4*RIGHT + (3.5-idx*0.5)*UP)
            self.line_anchors.append(dot)

    def construct(self):
        self.create_line_anchors()
        # create squares and dots in them
        squares = [Square(side_length=1) for _ in range(5)]
        dots = [Dot() for _ in range(5)]
        for idx, square in enumerate(squares):
            square.shift((idx - 2) * RIGHT * 2)
            dots[idx].move_to(square.get_center())
            self.to_play.append(ShowCreation(square))
            self.to_play.append(FadeIn(dots[idx]))
        
        # create head dot
        head_dot = Dot()
        head_dot.move_to(2*UP + 6*LEFT)
        self.add(head_dot)
        head_text = TextMobject("\\texttt{{head}}")
        head_text.move_to(head_dot.get_center()+0.5*UP)
        self.add(head_text)

        # create head pointers
        head_pointers = []
        for idx, square in enumerate(squares):
            tip = Triangle(color=WHITE, fill_opacity=1, start_angle=-PI/2)
            tip.set_width(0.25)
            tip.set_height(0.25)
            tip.next_to(square, UP, buff=0.1)
            line = MyCurvedLine(head_dot.get_center(), tip.get_corner(UP), buff=0)
            line.fit3()
            pointer = VGroup(tip, line)
            head_pointers.append(pointer)
        head_pointer = head_pointers[0].copy()
        self.to_play.append(FadeIn(head_pointer))

        # create original pointers
        original_pointers = []
        for i in range(4):
            start = squares[i].get_center()
            end = squares[i+1].get_corner(LEFT)
            arrow = Arrow(start, end, buff=0)
            original_pointers.append(arrow)
            self.to_play.append(GrowArrow(arrow))

        self.play_to_play()

        # fade out old arrows
        for arr in original_pointers:
            self.to_play.append(FadeOut(arr))
        self.play_to_play()

        # show end result
        end_pointers = []
        for i in range(4):
            start = squares[i+1].get_center()
            end = squares[i].get_corner(RIGHT)
            arrow = Arrow(start, end, buff=0)
            end_pointers.append(arrow)
            self.to_play.append(GrowArrow(arrow))
        self.to_play.append(Transform(head_pointer, head_pointers[4]))

        self.play_to_play()

        # back to original
        self.to_play += [FadeOut(arrow) for arrow in end_pointers]
        self.play_to_play()

        self.to_play += [FadeIn(arrow) for arrow in original_pointers]
        self.to_play.append(Transform(head_pointer, head_pointers[0]))
        self.play_to_play()

        # create null pointer
        null_dot1 = Dot().shift(5.5*RIGHT)
        null_text1 = TextMobject("\\texttt{{NULL}}").move_to(null_dot1.get_center()+RIGHT)
        self.to_play.append(FadeIn(null_dot1))
        self.to_play.append(FadeIn(null_text1))
        self.play_to_play()

        # connect null pointer
        null_arr1_tip = Triangle(color=WHITE, fill_opacity=1, start_angle=0)
        null_arr1_tip.set_width(0.25)
        null_arr1_tip.set_height(0.25)
        null_arr1_tip.next_to(null_dot1, LEFT, buff=0)
        null_arr1_line = MyCurvedLine(squares[4].get_center(), null_arr1_tip.get_corner(LEFT), buff=0)
        null_arr1 = VGroup(null_arr1_tip, null_arr1_line)
        self.to_play.append(FadeIn(null_arr1))
        self.play_to_play()

        # create head pointing to end NULL pointer
        null_head_tip = Triangle(color=WHITE, fill_opacity=1, start_angle=-PI/2)
        null_head_tip.set_width(0.25)
        null_head_tip.set_height(0.25)
        null_head_tip.next_to(null_dot1, UP, buff=0)
        null_head_line = MyCurvedLine(head_dot.get_center(), null_head_tip.get_corner(UP), buff=0)
        null_head_line.fit3()
        pointer = VGroup(null_head_tip, null_head_line)
        head_pointers.append(pointer)

        # highlight middle node
        self.to_play.append(ApplyMethod(squares[2].set_color, BLUE))
        self.to_play.append(ApplyMethod(dots[2].set_color, BLUE))
        self.to_play.append(ApplyMethod(original_pointers[2].set_color, BLUE))

        # create another null node
        null_dot2 = Dot().shift(5.5*LEFT)
        null_text2 = TextMobject("\\texttt{{NULL}}").move_to(null_dot2.get_center()+LEFT)
        self.to_play.append(FadeIn(null_dot2))
        self.to_play.append(FadeIn(null_text2))

        # connect null pointer
        null_arr2_tip = Triangle(color=WHITE, fill_opacity=1, start_angle=-PI)
        null_arr2_tip.set_width(0.25)
        null_arr2_tip.set_height(0.25)
        null_arr2_tip.next_to(null_dot2, RIGHT, buff=0)
        null_arr2_line = MyCurvedLine(squares[0].get_center(), null_arr2_tip.get_corner(RIGHT), buff=0)
        null_arr2 = VGroup(null_arr2_tip, null_arr2_line)
        self.to_play.append(FadeIn(null_arr2))

        # fade out old arrows
        self.to_play.append(FadeOut(original_pointers[0]))
        self.to_play.append(FadeOut(original_pointers[1]))
        # fade in end arrow
        self.to_play.append(FadeIn(end_pointers[0]))
        # move head
        self.to_play.append(Transform(head_pointer, head_pointers[2]))
        self.play_to_play()

        # create prev pointer
        prev_dot = Dot()
        prev_dot.move_to(2*DOWN + 6*LEFT)
        prev_text = TextMobject("\\texttt{{prev}}")
        prev_text.move_to(prev_dot.get_center()+0.5*DOWN)
        self.to_play.append(FadeIn(prev_dot))
        self.to_play.append(FadeIn(prev_text))

        # create prev pointing to start NULL pointer
        prev_pointers = []
        null_prev_tip = Triangle(color=WHITE, fill_opacity=1, start_angle=PI/2)
        null_prev_tip.set_width(0.25)
        null_prev_tip.set_height(0.25)
        null_prev_tip.next_to(null_dot2, DOWN, buff=0)
        null_prev_line = MyCurvedLine(prev_dot.get_center(), null_prev_tip.get_corner(DOWN), buff=0)
        null_prev_line.fit3()
        null_prev_pointer = VGroup(null_prev_tip, null_prev_line)
        prev_pointers.append(null_prev_pointer)

        # create prev pointers
        for idx, square in enumerate(squares):
            tip = Triangle(color=WHITE, fill_opacity=1, start_angle=PI/2)
            tip.set_width(0.25)
            tip.set_height(0.25)
            tip.next_to(square, DOWN, buff=0.1)
            line = MyCurvedLine(prev_dot.get_center(), tip.get_corner(DOWN), buff=0)
            line.fit3()
            pointer = VGroup(tip, line)
            prev_pointers.append(pointer)
        prev_pointer = prev_pointers[2].copy()
        self.to_play.append(FadeIn(prev_pointer))

        self.play_to_play()

        # move current nodes pointer to previous element
        head_next_is_prev = TextMobject("\\texttt{{head->next = prev;}}")
        head_next_is_prev.scale(0.5)
        # head_next_is_prev.to_corner(UR)
        head_next_is_prev.next_to(self.line_anchors[0], RIGHT, buff=0)
        self.to_play.append(FadeIn(head_next_is_prev))

        end_pointers[1].set_color(BLUE)
        self.to_play.append(FadeIn(end_pointers[1]))
        self.to_play.append(FadeOut(original_pointers[2]))

        self.play_to_play()

        # create tmp dot
        tmp_dot = Dot()
        tmp_dot.move_to(2*DOWN + 6*RIGHT)
        tmp_text = TextMobject("\\texttt{{tmp}}")
        tmp_text.move_to(tmp_dot.get_center()+0.5*DOWN)
        self.to_play.append(FadeIn(tmp_dot))
        self.to_play.append(FadeIn(tmp_text))

        # create tmp pointers
        tmp_pointers = []
        for idx, square in enumerate(squares):
            tip = Triangle(color=WHITE, fill_opacity=1, start_angle=PI/2)
            tip.set_width(0.25)
            tip.set_height(0.25)
            tip.next_to(square, DOWN, buff=0.1)
            line = MyCurvedLine(tmp_dot.get_center(), tip.get_corner(DOWN), buff=0)
            line.fit3()
            pointer = VGroup(tip, line)
            tmp_pointers.append(pointer)
        tmp_pointer = tmp_pointers[3].copy()
        self.to_play.append(FadeIn(tmp_pointer))

        # create tmp pointing to end NULL pointer
        null_tmp_tip = Triangle(color=WHITE, fill_opacity=1, start_angle=PI/2)
        null_tmp_tip.set_width(0.25)
        null_tmp_tip.set_height(0.25)
        null_tmp_tip.next_to(null_dot1, DOWN, buff=0)
        null_tmp_line = MyCurvedLine(tmp_dot.get_center(), null_tmp_tip.get_corner(DOWN), buff=0)
        null_tmp_line.fit3()
        null_tmp_pointer = VGroup(null_tmp_tip, null_tmp_line)
        tmp_pointers.append(null_tmp_pointer)

        # insert tmp = head->next code
        tmp_is_head_next = TextMobject("\\texttt{{tmp = head->next;}}")
        tmp_is_head_next.scale(0.5)
        tmp_is_head_next.next_to(self.line_anchors[0], RIGHT, buff=0)
        self.to_play.append(FadeIn(tmp_is_head_next))
        self.to_play.append(ApplyMethod(head_next_is_prev.next_to, self.line_anchors[1], {"buff": 0}))

        self.play_to_play()

        # move prev to head
        self.to_play.append(Transform(prev_pointer, prev_pointers[3]))
        prev_is_head = TextMobject("\\texttt{{prev = head;}}").scale(0.5)
        prev_is_head.next_to(self.line_anchors[2], RIGHT, buff=0)
        self.to_play.append(FadeIn(prev_is_head))

        self.play_to_play()

        # move head to tmp
        self.to_play.append(Transform(head_pointer, head_pointers[3]))
        head_is_tmp = TextMobject("\\texttt{{head = tmp;}}").scale(0.5)
        head_is_tmp.next_to(self.line_anchors[3], RIGHT, buff=0)
        self.to_play.append(FadeIn(head_is_tmp))
        self.play_to_play()

        # loop back
        start = head_is_tmp.get_corner(DOWN)
        directions = [0.5*DOWN, 1.5*LEFT, 2*UP]
        lines = []
        for direction in directions:
            lines.append(Line(start, start + direction))
            start += direction
        lines.append(Arrow(start, start+0.5*RIGHT, buff=0))
        broken_line = VGroup(*lines)
        self.to_play.append(FadeIn(broken_line))
        self.to_play.append(Transform(tmp_pointer, tmp_pointers[4]))
        self.play_to_play()


