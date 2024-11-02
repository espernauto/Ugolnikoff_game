import pandas as pd
import random
import copy
import time
import queue


class GameOfUgoles:
    def __init__(self, mode, constellation_neighbor, begin, end = ""):
        self.constellation_neighbor = constellation_neighbor
        self.begin = begin
        self.end = end
        self.mode = mode
        
    def closest_path(self, curr, cons_nei):
        used =  {}
        dist = {}
        for key in cons_nei.keys():
            used[key] = -1
            dist[key] = 100000000000
        path = {}
        path[curr] = -1
        used[curr] = 1
        dist[curr] = 0
        q = queue.Queue()
        q.put(curr)
        while not q.empty():
            v = q.get()
            for nei in cons_nei[v]:
                to = nei
                if used[nei] == -1:
                    used[nei] = 1
                    q.put(nei)
                    dist[nei] = dist[v] + 1
                    path[to] = v
        return used, path, dist[end]

    def next_step(self, curr, cons_nei):
        for el in cons_nei[curr]:
            if len(cons_nei[el]) == 1:
                return el
        used, p, distance = self.closest_path(curr, cons_nei)
        if distance == 2:
            for el in cons_nei[curr]:
                _, _, distance = self.closest_path(el, cons_nei)
                if distance > 1:
                    return el
        path = []
        if used[self.end] == -1:
        	return random.choice(cons_nei[curr])
        cons = self.end
        while cons != curr:
            path.append(cons)
            cons = p[cons]
        path.append(curr)
        path.reverse()
        return path[1]

    def next_step_random(self, curr, cons_nei):
        return random.choice(cons_nei[curr])

    def update(self, cons_nei, curr_cons):
        nei_list = cons_nei[curr_cons]
        #print(nei_list)
        for cons in nei_list:
            #print(cons_nei[cons])
            cons_nei[cons].remove(curr_cons)
        del cons_nei[curr_cons]
        return cons_nei

    def game_of_ugoles_two_points(self, cons_nei, error_limit = 3):
        curr_cons = self.begin
        curr_error = 0
        human_win_text = "Вы победили в войне машин. Что ты будешь делать дальше, Нео?"
        machine_win_text = "Видели бы вы себя, мистер Андерсон. Слепой мессия... Вы символ своего вида, мистер Андерсон. Беспомощные, жалкие люди. Они только и ждут, чтобы их избавили от мучений."
        while True:
            next_cons = self.next_step(curr_cons, cons_nei)
            print(next_cons)
            if next_cons == self.end or len(cons_nei[next_cons]) == 0:
                return machine_win_text
            cons_nei = self.update(copy.deepcopy(cons_nei), curr_cons)
            curr_cons = next_cons
            if len(cons_nei[next_cons]) == 0:
                return machine_win_text
            our_cons = input()
            while our_cons not in cons_nei[curr_cons]:
                curr_error += 1
                print(f"Это ваша {curr_error}-я ошибка, мистер Андерсон. У вас осталось ещё {error_limit - curr_error} попыток")
                if curr_error == error_limit:
                    return machine_win_text
                our_cons = input()
            cons_nei = self.update(copy.deepcopy(cons_nei), curr_cons)
            curr_cons = our_cons
            if curr_cons == self.end or len(cons_nei[curr_cons]) == 0:
                return human_win_text
            #time.sleep(1)

    def game_of_ugoles_endless_journey(self, cons_nei, error_limit = 3):
        curr_cons = self.begin
        curr_error = 0
        human_win_text = "Вы победили в войне машин. Что ты будешь делать дальше, Нео?"
        machine_win_text = "Видели бы вы себя, мистер Андерсон. Слепой мессия... Вы символ своего вида, мистер Андерсон. Беспомощные, жалкие люди. Они только и ждут, чтобы их избавили от мучений."
        while True:
            next_cons = self.next_step_random(curr_cons, cons_nei)
            print(next_cons)
            if len(cons_nei[next_cons]) == 0:
                return machine_win_text
            cons_nei = self.update(copy.deepcopy(cons_nei), curr_cons)
            curr_cons = next_cons
            if len(cons_nei[next_cons]) == 0:
                return machine_win_text
            our_cons = input()
            if our_cons == "Кентавр":
                our_cons = "Центавр"
            while our_cons not in cons_nei[curr_cons]:
                curr_error += 1
                if error_limit - curr_error > 1:
                    print(f"Это ваша {curr_error}-я ошибка, мистер Андерсон. У вас осталось ещё {error_limit - curr_error} попытки")
                elif error_limit - curr_error == 1:
                    print(f"Это ваша {curr_error}-я ошибка, мистер Андерсон. У вас осталcя последний шанс")
                if curr_error == error_limit:
                    return machine_win_text
                our_cons = input()
                if our_cons == "Кентавр":
                    our_cons = "Центавр"
            cons_nei = self.update(copy.deepcopy(cons_nei), curr_cons)
            curr_cons = our_cons
            if len(cons_nei[curr_cons]) == 0:
                return human_win_text
            #time.sleep(1)

    def start_game(self):
        cons_nei = copy.deepcopy(constellation_neighbor)
        if self.mode == "Ugolnikoff":
            print(self.game_of_ugoles_two_points(cons_nei))
        elif self.mode == "Endless journey":
            print(self.game_of_ugoles_endless_journey(cons_nei))

df = pd.read_csv('constellations.tsv', sep = '\t')
df = df.dropna()
df = df.drop_duplicates()
df = df.reset_index(drop = True)
df = df[['constellationLabel', 'neighborLabel']]

constellation_neighbor = {}
for i in range(len(df)):
    constellation_neighbor.setdefault(df['constellationLabel'][i], [])
    constellation_neighbor[df['constellationLabel'][i]].append(df['neighborLabel'][i])

print("Введите стартовое созвездие. Если оно состоит из двух слов, то оба слова с большой буквы. Если в нем есть буква ё, то буква ё строго обязательна...")

begin = input()

if begin == "Кентавр":
    begin = "Центавр"

print("Введите режим. На данный момент доступно два: режим Ugolnikoff -- стандартная игра Угольникова, где нужно дойти от начала до конца и режим Endless journey, в котором программа ходит рандомно и игра идёт до трех ваших ошибок")

mode = input()

if mode == "Ugolnikoff":
    print("Введите конечное созвездие")
    end = input()
    our_game = GameOfUgoles(mode, constellation_neighbor, begin, end)
else:
    our_game = GameOfUgoles(mode, constellation_neighbor, begin)
    
our_game.start_game()
