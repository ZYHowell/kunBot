import random
from configparser import ConfigParser

def classPrehead(knowledges): 
    string = "今天我们要讲的是这几个内容：首先是 " + knowledges[0][1] \
            + "，然后我们要讲 " + knowledges[1][1] + "，然后是 " + knowledges[2][1] + \
                "。如果有时间，我还想讲一下" + knowledges[3][1] + "，但我估计我应该是没有时间了。"
    return string

def trivialPattern1(knowledge): 
    return "有的同学可能会问" + knowledge + \
        "是什么，这是我之前讲过的，你回去看一下定义，很多同学可能会觉得这个很蠢，我就不在这里讲了"
def trivialPattern2(knowledge): 
    return "关于" + knowledge + \
        "的证明，其实是很基础的，我之前讲过，我们这门课最难的证明R-N已经过去了。" + \
            "算了，我还是讲一下吧。"
def trivialPattern3(knowledge): 
    return "我其实都不想讲" + knowledge + "的定义了，我觉得你们看教材就看得懂，这个证明属于直接套定义就可以做完了的"
def teachDef1(definition): 
    return definition + "这个定义其实是很trivial的，任何人都能很容易地看懂。" + \
        "但是提出它的人之所以伟大，就在于他能提出这样一个定义。我常常说，做数学的提出一个定义或者写出一个猜想，就已经快要做完了。"
def teachDef2(definition):
    return definition + "这个定义的思想是老百姓都能理解的。"
def teachDef3(definition):
    return "我一直说我教这门课就是为了带你们去看看人类历史上做出的非常美的一些东西，" + definition + \
        "就是这样一个东西。我希望你们能把" + definition + "为什么这样定义研究清楚了。" + \
            "至于" + definition + "这个定义本身，是没有什么难度的。"
def sigh(): 
    return "我看看我还有多少时间...我好像没有多少时间了。今天讲这个又花了太长时间。"
def appreciate(mathmatician, award): 
    return mathmatician + "为什么伟大，很多人都没有说到点子上。我一直觉得" + mathmatician + \
        "之所以被称为一个伟大的数学家，就在于他做出了" + award

proofTrivial = [trivialPattern1, trivialPattern2, trivialPattern3]
definitionTrivial = [teachDef1, teachDef2, teachDef3]
introduceWords = ["我们先讲", "接下来我们讲", "然后是", "最后我们要讲到"]

# todo: modify input format to support appreciation for Kolmogorov
# todo: plot expressions of Kun
class time: 
    def __init__(self): 
        self.hour = 10
        self.minute = 0
    def timePass(self, time): 
        self.minute += time
        if self.minute >= 60: 
            self.hour += int(self.minute / 60)
            self.minute %= 60
    def noTimeAfter(self, time): 
        minute = self.minute + time
        hour = self.hour
        if minute >= 60: 
            hour += int(self.minute / 60)
            minute %= 60
        if hour > 11 or (hour == 11 and minute > 45): return True
        return False 
    def restTime(self): 
        return 60 * (self.hour - 11) + 45 - self.minute
    def noTime(self): 
        if self.hour > 11 or (self.hour == 11 and self.minute > 40): return True
        return False
    def forceNoTime(self):
        if self.hour > 11 or (self.hour == 11 and self.minute > 45): return True
        return False
    def time2str(self): 
        return str(self.hour) + ':' + ('' if self.minute > 9 else '0') + str(self.minute)

class Printer: 
    def __init__(self): 
        self.clock = time()
    def print(self, words, moreTime=0): 
        if self.clock.forceNoTime(): return

        # todo: silence not only at the beginning, but in the middle
        silence = random.randint(0, 10) == 0
        length = len(words)
        costTime = max(random.randint(int(length * 0.1), int(length * 0.5)) + moreTime, 5)
        if silence: silenceRatio = float(random.randint(0, 5)) / 5.0
        else: silenceRatio = 0
        beginning = int(silenceRatio * len(words))

        if self.clock.noTimeAfter(costTime): 
            ratio = float(self.clock.restTime()) / float(costTime)
            canPrint = int(ratio * len(words))
            if silenceRatio < ratio: print(words[beginning:canPrint])
        else: print(words[beginning:])
        if silence: costTime += 2
        self.clock.timePass(costTime)
        print('now it is ' + self.clock.time2str())
    def forceNoTime(self): 
        return self.clock().forceNoTime()

if __name__ == '__main__':
    config = ConfigParser()
    config.read('teaching.config', encoding='UTF-8')
    knowledges = []
    zoom = Printer()
    for i in range(4): 
        baseName = 'knowledge' + str(i + 1)
        knowledges.append([config[baseName]['type'], config[baseName]['content']])
        
    # todo: before class, talk in wechat group
    beginning = classPrehead(knowledges)
    zoom.print(beginning, -30)
    currentStage = 0
    while currentStage < 4: 
        zoom.print(introduceWords[currentStage] + knowledges[currentStage][1])
        if knowledges[currentStage][0] == "thm": 
            zoom.print(proofTrivial[random.randint(0, 2)](knowledges[currentStage][1]), 
                        moreTime=10)
        else: zoom.print(definitionTrivial[random.randint(0, 2)](knowledges[currentStage][1]), 
                        moreTime=10)
        # randomly sigh
        if 3 > currentStage > 0 and random.randint(0, 2) == 0: zoom.print(sigh())
        currentStage += 1
    # todo: add random(almost sure) "I have no time to teach this" for the last part
    # todo: after class, talk in wechat group