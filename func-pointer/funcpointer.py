from manimlib.imports import *


def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def maximum(a, b):
    return max(a, b)

class FPointer(Scene):
    def __init__(self, *args, **kwargs):
        self.to_play = []
        self.scale = 2
        super().__init__(*args, **kwargs)

    def play_to_play(self, wait=1):
        self.play(*self.to_play)
        self.wait(wait)
        self.to_play = []

    def create_numbers(self, nums, func):
        self.num_objs = [TextMobject(str(num)) for num in nums]
        offset = len(nums) / 2 * self.scale * LEFT
        for idx, num_obj in enumerate(self.num_objs):
            num_obj.scale(self.scale)
            num_obj.shift((offset) + idx*self.scale*RIGHT +
                          0.75*self.scale*DOWN)
        
        self.agg_objs = []
        idx = 0
        aggregated = nums[0]
        offset = offset + self.scale*RIGHT
        while True:
            agg_obj = TextMobject(str(aggregated))
            agg_obj.scale(self.scale)
            agg_obj.shift(offset + idx*self.scale*RIGHT +
                          0.75*self.scale*UP)
            self.agg_objs.append(agg_obj)
            idx += 1
            if idx == len(nums): break
            aggregated = func(aggregated, nums[idx])

    def fpointer(self, fname, func, nums):
        if len(nums) < 2:
            raise Exception("Array too small, nothing worthy of animation.")
        
        self.create_numbers(nums, func)

        for num_obj in self.num_objs:
            self.to_play.append(Write(num_obj))
        self.play_to_play()

        rect = Rectangle(height=2.5*self.scale, width=1*self.scale)
        rect.shift((len(nums)/2-1)*self.scale*LEFT)

        func_obj = TextMobject(f"{fname}")
        func_obj.shift((len(nums)/2-1)*self.scale*LEFT)

        for idx in range(len(self.agg_objs)):
            self.to_play.append(Write(self.agg_objs[idx]))


            if idx == 0:
                self.play_to_play()
                self.to_play.append(ShowCreation(rect))
                self.to_play.append(Write(func_obj))
                self.play_to_play()
            elif idx != len(self.agg_objs) - 1:
                self.play_to_play(0)
                self.to_play.append(ApplyMethod(rect.shift, self.scale*RIGHT))
                self.to_play.append(ApplyMethod(func_obj.shift, self.scale*RIGHT))
                self.play_to_play(0)
            else:
                self.play_to_play()
        
        # fade all
        for num_obj in self.num_objs:
            self.to_play.append(FadeOut(num_obj))
        for agg_obj in self.agg_objs:
            self.to_play.append(FadeOut(agg_obj))
        self.to_play.append(FadeOut(rect))
        self.to_play.append(FadeOut(func_obj))
        self.play_to_play()

    def construct(self):
        nums = [2, 3, 3, -4, 10, 1]

        self.fpointer("+", add, nums)
        self.fpointer("$\\times$", mul, nums)
        self.fpointer("$\\max$", maximum, nums)
