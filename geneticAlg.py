import random


items = [[2,35],[3,85],[9,135],[0.5,10],[2,25],[0.1,2],[4,94]]
capacity = 25
pop_size = 20
gen_max = 1000
start_pop_with_zero = False
bestpos =[]
bestfit = []
def spawn_starting_population(amount):
    return [spawn_individual() for x in range(0,amount)]


def spawn_individual():
    arr = []
    if start_pop_with_zero is True:
        for x in range(0,len(items)):
            arr.append([random.randint(0, 0), random.randint(0,0)])
    else:
        for x in range(0,len(items)):
            arr.append([random.randint(0, 1), random.randint(0, 1000)])
    return arr


def fitness(target):
    total_val = 0
    total_weight = 0
    index = 0

    for i in target:
        if index >= len(items):
            break
        if i[0] == 1:
            total_val += items[index][1] * i[1]
            total_weight += items[index][0] * i[1]
        index += 1
    if total_weight > capacity:
        return 0
    else:
      #  print(target, total_val, total_weight)

        return total_val

def evolve_population(pop, bestval):
    parent_eligibility = 0.2
    mutation_chance = 0.08
    parent_lottery = 0.08

    parent_length = int(parent_eligibility*len(pop))
    parents = pop[:parent_length]
    nonparents = pop[parent_length:]

    for np in nonparents:
        if parent_lottery > random.random():
            parents.append(np)

    for p in parents:
        if mutation_chance > random.random():
            mutate(p)

    children = []
    desired_length = len(pop) - len(parents)
    while len(children) < desired_length:
        male = pop[random.randint(0,len(parents)-1)]
        female = pop[random.randint(0,len(parents)-1)]
        half = round(len(male)/2)
        child = male[:half] + female[half:] # from start to half from father, from half to end from mother

        if mutation_chance > random.random() and bestval != 0:
            mutate(child)
        children.append(child)

    parents.extend(children)
    return parents


def mutate(target):
    """
    Changes a random element of the permutation array from 0 -> 1 or from 1 -> 0.
    """
    r = random.randint(0,len(target)-1)
    if target[r][0] == 1:
        target[r][0] = 0
    else:
        target[r][0] = 1

    if target[r][1] * items[r][0] > 25:
        target[r][1] = round(25/items[r][0])
    else:
        target[r][1] -= random.randint(0,10)
        if target[r][1] < 0:
            target[r][1] = round(25/items[r][0])


def main():
    generation = 1
    population = spawn_starting_population(pop_size)
    bestval = 0
    besttarget = []
    for g in range(gen_max):
       # print("Generation %d with %d" % (generation,len(population)))
        population = sorted(population,key=lambda x:fitness(x), reverse=True)
        b = fitness(population[0])
        if bestval < b:
            bestval = b
            besttarget = population[0]
            print(bestval)
            print(besttarget)
        population = evolve_population(population,bestval)
        generation += 1



if __name__ == '__main__':
    main()