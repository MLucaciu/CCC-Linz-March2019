import math
import traceback

DIRECTIONS = {
    0: {
        "x": 1,
        "y": 0
    },
    1: {
        "x": 0,
        "y": 1
    },
    2: {
        "x": -1,
        "y": 0
    },
    3: {
        "x": 0,
        "y": -1
    }
}

CMD_TURN_TYPE = "T"
CMD_F_TYPE = "F"


def euclidean_dist(p1, p2):
    return math.sqrt((p1.y - p2.y) ** 2 + (p1.x - p2.x) ** 2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Command:
    def __init__(self, ctype, cvalue):
        self.type = ctype
        self.value = cvalue


class Alien:
    def __init__(self, id, spawn_time, health, speed, traseu=list()):
        self.id = id
        self.spawn_time = spawn_time
        self.traseu = traseu
        self.health = health
        self.speed = speed
        self.dead = False
        self.spawned = False

    def get_pos_at_tick(self, tick):
        pos = int((tick - self.spawn_time) * self.speed)
        try:
            return self.traseu[pos]
        except:
            print(traceback.format_exc())
            if not self.dead:
                raise ValueError("Defeat")


class Query:
    def __init__(self, tick, id_alien):
        self.tick = tick
        self.id_alien = id_alien


class Tower:
    def __init__(self, id, damage, radius, position):
        self.id = id
        self.damage = damage
        self.radius = radius
        self.position = position
        self.locked_for = None

    def can_shot_current_alien(self, tick, alien=None):
        """
        pot sa il impusc pe cel curent
        :return:
        """
        if alien is None:
            return euclidean_dist(self.position, self.locked_for.get_pos_at_tick(tick)) <= self.radius
        else:
            return euclidean_dist(self.position, alien.get_pos_at_tick(tick)) <= self.radius

    def shot(self):

        self.locked_for.health -= self.damage
        if self.locked_for.health <= 0:
            # print("Tower %d kills %d" % (self.id, self.locked_for.id))
            self.locked_for.dead = True
            self.locked_for = None
        else:
            pass
            # print("Tower %d shoot %d" % (self.id, self.locked_for.id))

    def find_target(self, tick, aliens):
        target = None
        min_dist = math.inf
        for alien in aliens:
            if not alien.dead and alien.spawned:
                if self.can_shot_current_alien(tick, alien) and min_dist > euclidean_dist(self.position,
                                                                                          alien.get_pos_at_tick(tick)):
                    min_dist = euclidean_dist(self.position, alien.get_pos_at_tick(tick))
                    target = alien
        self.locked_for = target


def load_from_file_4(file_name):
    data = list()
    start_point = None
    dimenstions = None
    commands = list()
    list_of_alliens = list()
    current_line_nr = 0
    with open(file_name, "r") as f:
        text = f.read()
        lines = text.split("\n")
        current_line_nr = 0
        dimensions_txt = lines[current_line_nr]  # dimensiunea tabelei linia 0
        current_line_nr += 1
        dimensions_txt_list = dimensions_txt.split(" ")
        dimenstions = Point(int(dimensions_txt_list[0]), int(dimensions_txt_list[1]))
        start_point_txt = lines[current_line_nr]  # start point linia 1
        current_line_nr += 1
        start_point_txt_list = start_point_txt.split(" ")
        start_point = Point(int(start_point_txt_list[0]), int(start_point_txt_list[1]))
        commands_array = lines[current_line_nr].split(" ")  # commands linia 2
        current_line_nr += 1
        i = 0
        while i < len(commands_array):
            commands.append(Command(commands_array[i], int(commands_array[i + 1])))
            i += 2

        alien_charachteristics = lines[current_line_nr]
        current_line_nr += 1
        alien_charachteristics = alien_charachteristics.split(" ")
        hp = float(alien_charachteristics[0])
        speed = float(alien_charachteristics[1])

        nr_eliens = int(lines[current_line_nr])
        current_line_nr += 1
        for i in range(nr_eliens):
            list_of_alliens.append(Alien(i, int(lines[current_line_nr]), hp, speed))
            current_line_nr += 1
        tower_characteristics = lines[current_line_nr]
        current_line_nr += 1
        tower_characteristics = tower_characteristics.split(" ")
        damage = float(tower_characteristics[0])
        trange = int(tower_characteristics[1])
        nr_towers = int(lines[current_line_nr])
        current_line_nr += 1

        towers = list()
        for i in range(nr_towers):
            pos_tower = lines[current_line_nr]
            current_line_nr += 1
            pos_tower = pos_tower.split(" ")
            towers.append(Tower(i, damage, trange, Point(int(pos_tower[0]), int(pos_tower[1]))))

    return dimenstions, start_point, commands, hp, speed, list_of_alliens, damage, trange, towers


def load_from_file_5(file_name):
    data = list()
    start_point = None
    dimenstions = None
    commands = list()
    list_of_alliens = list()
    current_line_nr = 0
    with open(file_name, "r") as f:
        text = f.read()
        lines = text.split("\n")
        current_line_nr = 0
        dimensions_txt = lines[current_line_nr]  # dimensiunea tabelei linia 0
        current_line_nr += 1
        dimensions_txt_list = dimensions_txt.split(" ")
        dimenstions = Point(int(dimensions_txt_list[0]), int(dimensions_txt_list[1]))
        start_point_txt = lines[current_line_nr]  # start point linia 1
        current_line_nr += 1
        start_point_txt_list = start_point_txt.split(" ")
        start_point = Point(int(start_point_txt_list[0]), int(start_point_txt_list[1]))
        commands_array = lines[current_line_nr].split(" ")  # commands linia 2
        current_line_nr += 1
        i = 0
        while i < len(commands_array):
            commands.append(Command(commands_array[i], int(commands_array[i + 1])))
            i += 2

        alien_charachteristics = lines[current_line_nr]
        current_line_nr += 1
        alien_charachteristics = alien_charachteristics.split(" ")
        hp = float(alien_charachteristics[0])
        speed = float(alien_charachteristics[1])

        nr_eliens = int(lines[current_line_nr])
        current_line_nr += 1
        for i in range(nr_eliens):
            list_of_alliens.append(Alien(i, int(lines[current_line_nr]), hp, speed))
            current_line_nr += 1
        tower_characteristics = lines[current_line_nr]
        current_line_nr += 1
        tower_characteristics = tower_characteristics.split(" ")
        damage = float(tower_characteristics[0])
        trange = int(tower_characteristics[1])
        tcost = int(tower_characteristics[2])
        gold = int(lines[current_line_nr])
        current_line_nr += 1

    return dimenstions, start_point, commands, hp, speed, list_of_alliens, damage, trange, tcost, gold


def level_4_update_allien_position(tick, alliens):
    """

    :return:
    """
    for alien in alliens:
        if tick < alien.spawn_time:
            continue
        alien.spawned = True
        if not alien.dead:
            try:
                alien.get_pos_at_tick(tick)
            except ValueError:
                return True
    return False


def level_4_shoot(tick, aliens, tower_list):
    """

    :param tick:
    :param aliens:
    :return:
    """
    for tower in tower_list:
        if tower.locked_for is not None:
            if tower.can_shot_current_alien(tick):
                tower.shot()
            else:
                tower.find_target(tick, aliens)
                if tower.locked_for is not None:
                    tower.shot()
        else:
            tower.find_target(tick, aliens)
            if tower.locked_for is not None:
                tower.shot()


def level4_check_status(aliens):
    for alien in aliens:
        if alien.spawned is False or alien.health > 0:
            return False
    return True


def level_4(file_name):
    dimenstions, start_point, commands, hp, speed, list_of_alliens, damage, trange, towers = load_from_file_4(file_name)
    direction = 0
    output = str(start_point) + "\n"
    current_point = Point(start_point.x, start_point.y)
    traseu = [Point(current_point.x, current_point.y)]
    for cmd in commands:
        if cmd.type == CMD_F_TYPE:
            for i in range(cmd.value):
                current_point.x += DIRECTIONS[direction]["x"]
                current_point.y += DIRECTIONS[direction]["y"]
                traseu.append(Point(current_point.x, current_point.y))
        elif cmd.type == CMD_TURN_TYPE:
            direction += cmd.value
            direction = direction % 4
        else:
            print("WTF")
    for allien in list_of_alliens:
        allien.traseu = traseu

    current_tick = 0
    while True:
        reached_end = level_4_update_allien_position(current_tick, list_of_alliens)
        if reached_end:
            with open("%s.out" % file_name, "w") as g:
                g.write(str(current_tick) + "\n" + "LOSS")
            return
        else:
            if current_tick > 0:
                level_4_shoot(current_tick, list_of_alliens, towers)
            if level4_check_status(list_of_alliens):
                with open("%s.out" % file_name, "w") as g:
                    g.write(str(current_tick) + "\n" + "WIN")
                return
        print("Tick=" + str(current_tick))
        # for alien in list_of_alliens:
        #     try:
        #         print(str(alien.id) + " - " + "HP=" + str(alien.health) + " spawn="+ str(alien.spawn_time)+ " (" + str(
        #             alien.get_pos_at_tick(current_tick)) + ")")
        #     except:
        #         pass
        # print("====================================================================")
        new_allien = list()
        for alien in list_of_alliens:
            if not alien.dead:
                new_allien.append(alien)
        list_of_alliens = [i for i in new_allien]
        for t in towers:
            if t.locked_for is not None:
                if t.locked_for.dead:
                    t.locked_for = None
        current_tick += 1

    #     for qu in query_list:
    #         current_answer = str(qu.tick) + " " + str(qu.id_alien) + " " + str(
    #             list_of_alliens[qu.id_alien].get_pos_at_tick(qu.tick, speed))
    #
    #         g.write(str(current_answer) + "\n")


def valid_tower(max_towers, curr_pos, towers, traseu, radius):
    traseu_covered = list()
    for i in range(len(traseu)):
        traseu_covered.append(0)
    for tower in towers:
        for i in range(len(traseu)):
            if euclidean_dist(tower.position, traseu[i]) <= tower.radius:
                traseu_covered[i] += 1
    for i in range(len(traseu)):
        if euclidean_dist(curr_pos, traseu[i]) <= radius:
            if traseu_covered[i] >= max_towers:
                return False
    return True


def valid_tower1(max_towers, curr_pos, towers, traseu, radius):
    cate = 0
    for t in towers:
        if euclidean_dist(curr_pos, t.position) <= radius:
            cate += 1
    if cate >= max_towers:
        return False
    return True

def valid_tower2(max_towers, curr_pos, towers, traseu, radius):
    cate = 0
    for t in towers:
        if euclidean_dist(t.position, curr_pos) <= radius:
            cate += 1
    if cate <= radius:
        return True
    return False


def level_5(file_name):
    dimenstions, start_point, commands, hp, speed, list_of_alliens, damage, trange, tcost, gold = load_from_file_5(
        file_name)
    direction = 0
    output = str(start_point) + "\n"
    current_point = Point(start_point.x, start_point.y)
    traseu = [Point(current_point.x, current_point.y)]
    for cmd in commands:
        if cmd.type == CMD_F_TYPE:
            for i in range(cmd.value):
                current_point.x += DIRECTIONS[direction]["x"]
                current_point.y += DIRECTIONS[direction]["y"]
                traseu.append(Point(current_point.x, current_point.y))
        elif cmd.type == CMD_TURN_TYPE:
            direction += cmd.value
            direction = direction % 4
        else:
            print("WTF")
    for allien in list_of_alliens:
        allien.traseu = traseu

    towers = list()
    libere = list()
    for i in range(len(traseu)):
        for p in [Point(traseu[i].x,traseu[i].y+1),
                  Point(traseu[i].x, traseu[i].y-1),
                  Point(traseu[i].x+1, traseu[i].y),
                  Point(traseu[i].x-1, traseu[i].y),
                  Point(traseu[i].x+1, traseu[i].y+1),
                  Point(traseu[i].x+1, traseu[i].y-1),
                  Point(traseu[i].x-1, traseu[i].y+1),
                  Point(traseu[i].x-1, traseu[i].y-1)]:
            if p not in traseu and p not in libere:
                curr_cost = 0
                for pct in traseu:
                    if euclidean_dist(pct, p) <= trange:
                        curr_cost += 1
                p.cost = curr_cost
                libere.append(p)
    libere = sorted(libere, key=lambda x: x.cost, reverse=True)
    max_towers = hp // damage + 1
    nr_turnuri = min(gold // tcost, 500)
    print(nr_turnuri)
    towers = list()
    with open("%s.out" % file_name, "w") as g:
        for i in range(len(libere)):
            if nr_turnuri <= len(towers):
                break
            if valid_tower2(max_towers, libere[i], towers, traseu, trange):
                towers.append(Tower(i, damage, trange, libere[i]))

                g.write(str(libere[i]) + "\n")

    print(len(towers))
    # simulare
    current_tick = 0
    while True:
        reached_end = level_4_update_allien_position(current_tick, list_of_alliens)
        if reached_end:
            print(str(current_tick) + "\n" + "LOSS")
            return
        else:
            if current_tick > 0:
                level_4_shoot(current_tick, list_of_alliens, towers)
            if level4_check_status(list_of_alliens):
                print(str(current_tick) + "\n" + "WIN")
                return
        print("Tick=" + str(current_tick))
        # for alien in list_of_alliens:
        #     try:
        #         print(str(alien.id) + " - " + "HP=" + str(alien.health) + " spawn="+ str(alien.spawn_time)+ " (" + str(
        #             alien.get_pos_at_tick(current_tick)) + ")")
        #     except:
        #         pass
        # print("====================================================================")
        new_allien = list()
        for alien in list_of_alliens:
            if not alien.dead:
                new_allien.append(alien)
        list_of_alliens = [i for i in new_allien]
        for t in towers:
            if t.locked_for is not None:
                if t.locked_for.dead:
                    t.locked_for = None
        current_tick += 1

    #     for qu in query_list:
    #         current_answer = str(qu.tick) + " " + str(qu.id_alien) + " " + str(
    #             list_of_alliens[qu.id_alien].get_pos_at_tick(qu.tick, speed))
    #
    #         g.write(str(current_answer) + "\n")


if __name__ == "__main__":
    level_5("level5_5.in")
