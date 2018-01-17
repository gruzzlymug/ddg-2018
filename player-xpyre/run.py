import battlecode as bc
import random
import sys
import traceback

#===============================================================================

# XPYRE Player

#-------------------------------------------------------------------------------
def do_factory(unit):
    # early out if not done building
    if not unit.structure_is_built():
        return False

    garrison = unit.structure_garrison()
    if len(garrison) > 0:
        d = random.choice(directions)
        if gc.can_unload(unit.id, d):
            # print('unloaded a thing!')
            gc.unload(unit.id, d)
            return True

    need_knights = not bc.UnitType.Knight in last_counts or last_counts[bc.UnitType.Knight] < 50
    if need_knights and gc.can_produce_robot(unit.id, bc.UnitType.Knight):
        gc.produce_robot(unit.id, bc.UnitType.Knight)
        # print('produced a knight!')
        return True

    need_healers = not bc.UnitType.Healer in last_counts or last_counts[bc.UnitType.Healer] < 2
    if need_healers and gc.can_produce_robot(unit.id, bc.UnitType.Healer):
        gc.produce_robot(unit.id, bc.UnitType.Healer)
        # print('produced a healer!')
        return True

    return False

#-------------------------------------------------------------------------------
def do_worker(unit):
    dd = random.choice(directions)

    need_workers = not bc.UnitType.Worker in last_counts or last_counts[bc.UnitType.Worker] < 4
    if need_workers and gc.can_replicate(unit.id, dd):
        gc.replicate(unit.id, dd)
        return True

    need_rockets = not bc.UnitType.Rocket in last_counts or last_counts[bc.UnitType.Rocket] < 4
    if need_rockets and gc.can_blueprint(unit.id, bc.UnitType.Rocket, dd):
        # print("BUILT A ROCKET")
        gc.blueprint(unit.id, bc.UnitType.Rocket, dd)
        return True

    # next, let's look for nearby blueprints to work on
    nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
    for other in nearby:
        if gc.can_build(unit.id, other.id):
            gc.build(unit.id, other.id)
            # print('built something:')
            return True
    return False

#-------------------------------------------------------------------------------
def do_knight(unit):
    # print("knight")
    nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
    for other in nearby:
        # if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
        #     # print('attacked a thing!')
        #     gc.attack(unit.id, other.id)
        #     return True
        if other.unit_type == bc.UnitType.Rocket and gc.can_load(other.id, unit.id):
            if not other.rocket_is_used():
                # print("knight boarding rocket")
                gc.load(other.id, unit.id)
                return True
    return False

#-------------------------------------------------------------------------------
def find_landing_site():
    dest = bc.MapLocation(bc.Planet.Mars, 0, 0)

    no_landing_site = True
    for n in range(7):
        dest.x = random.randint(0, mars_map.width)
        dest.y = random.randint(0, mars_map.height)
        if no_landing_site and mars_map.is_passable_terrain_at(dest):
            no_landing_site = False
            # print("found dest", dest.x, dest.y)
            return dest

    # TODO return null or something...dest is not valid
    if no_landing_site:
        # print("nuts")
        return dest

#-------------------------------------------------------------------------------
def do_rocket(unit):
    # early out if not done building
    if not unit.structure_is_built():
        return False

    if unit.rocket_is_used():
        garrison = unit.structure_garrison()
        if len(garrison) > 0:
            d = random.choice(directions)
            if gc.can_unload(unit.id, d):
                # print('unloaded on mars!')
                gc.unload(unit.id, d)
                return True

    # TODO this is a hack
    if unit.rocket_is_used():
        # nothing to unload, dead in the water
        return False

    garrison = unit.structure_garrison()
    if len(garrison) == 0:
        # print("no crew! aborting!")
        return False

    landing_site = find_landing_site()

    # TODO this effectively crashes docker...why?
    # if gc.can_launch_rocket(unit.id, landing_site)
    print("launching!")
    gc.launch_rocket(unit.id, landing_site)
    #     return True
    return False

#===============================================================================

print("XPYRE 2018.01.16c")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

my_team = gc.team()

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)

unit_counts = {}
last_counts = {}

# NOTE not used
old_landing_sites = []

print("pystarted")

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)
gc.queue_research(bc.UnitType.Healer)

while True:
    # We only support Python 3, which means brackets around print()
    turn = gc.round()

    # TODO "classify others" pre-step

    last_counts = unit_counts
    unit_counts = {}

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():
            ut = unit.unit_type
            if ut in unit_counts:
                unit_counts[ut] += 1
            else:
                unit_counts[ut] = 1

            if not unit.location.is_on_map():
                # print("{} not on map".format(unit.unit_type))
                continue

            if ut == bc.UnitType.Factory:
                handled = do_factory(unit)
                if handled:
                    continue
            elif ut == bc.UnitType.Worker:
                handled = do_worker(unit)
                if handled:
                    continue
            elif ut == bc.UnitType.Knight:
                handled = do_knight(unit)
                if handled:
                    continue
            elif ut == bc.UnitType.Rocket:
                handled = do_rocket(unit)
                if handled:
                    continue

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            # print("karbonite: ", gc.karbonite())
            # print("  need: ", bc.UnitType.Factory.blueprint_cost())
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
