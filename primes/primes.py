from manimlib.imports import *
import os
import pyclbr
import numpy as np

SCALE = 2

class MyText:
    def __init__(self, val, scale=SCALE):
        self.val = val
        self.text = TextMobject(str(val))
        self.text.scale(scale)
        self.circle = Circle(radius=0.4*scale, color=GREEN)

class Numbers(Scene):
    def construct(self):
        numbers = [1, 2, 5, 6, 8, 12, 17]
        nums = [MyText(n) for n in numbers]
        colons = [MyText(":") for _ in range(len(numbers))]

        for idx, elem in enumerate(nums):
            pos = [(-3 + idx) * SCALE, 0, 0]
            elem.text.move_to(pos)

        for idx, elem in enumerate(colons):
            pos = [-5, (3 - idx), 0]
            elem.text.move_to(pos)

        divs = [
            ["1"],
            ["1,","2"],
            ["1,", "5"],
            ["1,", "2,", "3,", "6"],
            ["1,", "2,", "4,", "8"],
            ["1,", "2,", "3,", "4,", "6,", "12"],
            ["1,", "17"]
        ]
        div_obj = []
        for idx, d_list in enumerate(divs):
            for jdx, d in enumerate(d_list):
                d = MyText(d)
                d_list[jdx] = d
                if jdx == 0:
                    d.text.move_to(colons[idx].text.get_center() + RIGHT)
                else:
                    d.text.move_to(d_list[jdx - 1].text.get_center() + RIGHT)
                div_obj.append(d)


        self.play(*[Write(num.text) for num in nums])
        self.play(*[ApplyMethod(nums[i].text.move_to, (colons[i].text.get_center() + LEFT))
                                for i in range(len(nums))])
        self.play(*[Write(col.text) for col in colons],
                  *[Write(d.text) for d in div_obj])

        self.wait(2)

class Primes(Scene):
    def construct(self):
        div_dict = {
            "1": ["1"],
            "2": ["1,","2"],
            "5": ["1,", "5"],
            "6": ["1,", "2,", "3,", "6"],
            "8": ["1,", "2,", "4,", "8"],
            "12": ["1,", "2,", "3,", "4,", "6,", "12"],
            "17": ["1,", "17"]
        }

        colons = [MyText(":") for _ in range(len(div_dict.keys()))]
        for idx, elem in enumerate(colons):
            pos = [-2, (3 - idx), 0]
            elem.text.move_to(pos)

        div_obs = []
        i = 0
        for num, divs in div_dict.items():
            num_obj = MyText(num)
            pos = colons[i].text.get_center() + LEFT
            i = i + 1
            num_obj.text.move_to(pos)
            div_obj_list = []
            for div in divs:
                d_obj = MyText(div)
                div_obj_list.append(d_obj)
            div_obs.append((num_obj, div_obj_list))

        for idx, (_, divs) in enumerate(div_obs):
            for jdx, div in enumerate(divs):
                if jdx == 0:
                    div.text.move_to(colons[idx].text.get_center() + RIGHT)
                else:
                    div.text.move_to(divs[jdx - 1].text.get_center() + RIGHT)

        self.play(*[Write(num.text) for num, _ in div_obs])
        self.play(*[Write(col.text) for col in colons],
                  *[Write(num.text) for _, divs in div_obs for num in divs])

        self.play(*[ApplyMethod(elem.text.set_color, GREEN) for elem, divs in div_obs if len(divs) == 2],
                  *[ApplyMethod(elem.text.set_color, GREEN) for _, divs in div_obs for elem in divs if len(divs) == 2],
                  *[ApplyMethod(colons[idx].text.set_color, GREEN) for idx, (_, divs) in enumerate(div_obs) if len(divs) == 2],
                  *[ApplyMethod(elem.text.set_color, GRAY) for elem, divs in div_obs if len(divs) != 2],
                  *[ApplyMethod(elem.text.set_color, GRAY) for _, divs in div_obs for elem in divs if len(divs) != 2],
                  *[ApplyMethod(colons[idx].text.set_color, GRAY) for idx, (_, divs) in enumerate(div_obs) if len(divs) != 2])
        self.play(*[FadeOut(num.text) for num, _ in div_obs],
                  *[FadeOut(col.text) for col in colons],
                  *[FadeOut(num.text) for _, divs in div_obs for num in divs])

class Number7(Scene):
    def construct(self):
        numbers = list(range(1, 8))
        numbers = [MyText(num) for num in numbers]

        question = TextMobject("Prím-e a 7?")
        question.to_edge(UP)
        question.scale(SCALE)

        for i, num in enumerate(numbers):
            pos = [(-3 + i) * SCALE, -1, 0]
            num.text.move_to(pos)
            num.circle.move_to(pos)

        self.play(*[Write(num.text) for num in numbers],
                  Write(question))

        arrow = Arrow(UP, DOWN)
        arrow.move_to(numbers[1].text.get_center() + 2*UP)
        self.play(GrowArrow(arrow))
        for idx, num in enumerate(numbers):
            if idx >= 2 and idx < len(numbers) - 1:
                self.play(ApplyMethod(arrow.move_to, num.text.get_center() + 2 * UP),
                          ApplyMethod(numbers[idx - 1].text.set_color, GREEN),
                          ShowCreation(numbers[idx - 1].circle))
        self.play(ApplyMethod(numbers[-2].text.set_color, GREEN),
                  ShowCreation(numbers[idx - 1].circle))
        self.play(*[FadeOut(num.text) for num in numbers],
                  *[FadeOut(num.circle) for idx, num in enumerate(numbers) if idx > 0 and idx < len(numbers) - 1],
                  FadeOut(question), FadeOut(arrow))

class Number9(Scene):
    def construct(self):
        numbers = list(range(1, 10))
        numbers = [MyText(num, scale=1.5) for num in numbers]

        question = TextMobject("Prím-e a 9?")
        question.to_edge(UP)
        question.scale(SCALE)

        for i, num in enumerate(numbers):
            pos = [-6 + i * 6/4, -1, 0]
            num.text.move_to(pos)
            num.circle.move_to(pos)

        self.play(*[Write(num.text) for num in numbers],
                  Write(question))

        arrow = Arrow(UP, DOWN)
        arrow.move_to(numbers[1].text.get_center() + 2*UP)
        self.play(GrowArrow(arrow))
        self.play(ApplyMethod(arrow.move_to, numbers[2].text.get_center() + 2 * UP),
                  ApplyMethod(numbers[1].text.set_color, GREEN),
                  ShowCreation(numbers[1].circle))
        numbers[2].circle.set_color(RED)
        self.play(ApplyMethod(numbers[2].text.set_color, RED),
                  ShowCreation(numbers[2].circle))
        self.play(*[FadeOut(num.text) for num in numbers],
                  FadeOut(question), FadeOut(arrow), FadeOut(numbers[1].circle),
                  FadeOut(numbers[2].circle))