
import random
import math
import copy

# Define grid size (25x25 unit square)
GRID_SIZE = 25

# Define components with their respective width and height
components = {
    "ALU": (5, 5),
    "Cache": (7, 4),
    "Control Unit": (4, 4),
    "Register File": (6, 6),
    "Decoder": (5, 3),
    "Floating Unit": (5, 5)
}

# Define the order of components (used for consistency in encoding)
component_order = list(components.keys())

# Generate a random chromosome (placement of all components)
def generate_random_chromosome():
    return [(random.randint(0, GRID_SIZE - components[name][0]),
             random.randint(0, GRID_SIZE - components[name][1]))
            for name in component_order]

# Initialize a population of chromosomes
def initial_population(n=6):
    return [generate_random_chromosome() for _ in range(n)]

# Get the center of a component based on its bottom-left coordinate
def get_center(coord, comp_name):
    x, y = coord
    w, h = components[comp_name]
    return (x + w/2, y + h/2)

# Compute Euclidean distance between two points
def euclidean(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Define all wiring connections between components
connections = [
    ("Register File", "ALU"),
    ("Control Unit", "ALU"),
    ("ALU", "Cache"),
    ("Register File", "Floating Unit"),
    ("Cache", "Decoder"),
    ("Decoder", "Floating Unit")
]

# Compute total wiring distance (sum of center-to-center distances for required connections)
def compute_wiring_distance(chromosome):
    pos = dict(zip(component_order, chromosome))
    return sum(euclidean(get_center(pos[a], a), get_center(pos[b], b)) for a, b in connections)

# Compute bounding box area that contains all components
def compute_bounding_area(chromosome):
    xs, ys = [], []
    for i, (x, y) in enumerate(chromosome):
        w, h = components[component_order[i]]
        xs.extend([x, x + w])
        ys.extend([y, y + h])
    return (max(xs) - min(xs)) * (max(ys) - min(ys))

# Count overlapping pairs among all component placements
def count_overlaps(chromosome):
    overlaps = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            x1, y1 = chromosome[i]
            x2, y2 = chromosome[j]
            w1, h1 = components[component_order[i]]
            w2, h2 = components[component_order[j]]

            # Check if rectangles overlap
            if not (x1 + w1 <= x2 or x1 >= x2 + w2 or y1 + h1 <= y2 or y1 >= y2 + h2):
                overlaps += 1
    return overlaps

# Calculate fitness score (negative because we minimize objectives)
def fitness(chromosome, alpha=1000, beta=2, gamma=1):
    overlap = count_overlaps(chromosome)
    wiring = compute_wiring_distance(chromosome)
    area = compute_bounding_area(chromosome)
    return -(alpha * overlap + beta * wiring + gamma * area)

# Randomly select two parents from population
def select_parents(pop, k=2):
    return random.sample(pop, k)

# Perform single-point crossover between two parents
def single_point_crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

# Perform two-point crossover between two parents (used in Task 2)
def two_point_crossover(p1, p2):
    pt1 = random.randint(0, len(p1) - 2)
    pt2 = random.randint(pt1 + 1, len(p1) - 1)
    c1 = p1[:pt1] + p2[pt1:pt2] + p1[pt2:]
    c2 = p2[:pt1] + p1[pt1:pt2] + p2[pt2:]
    return c1, c2

# Mutate a chromosome (randomly adjust a block's coordinates with a small probability)
def mutate(chromosome, mutation_rate=0.1):
    if random.random() < mutation_rate:
        index = random.randint(0, len(chromosome) - 1)
        w, h = components[component_order[index]]
        chromosome[index] = (random.randint(0, GRID_SIZE - w),
                              random.randint(0, GRID_SIZE - h))
    return chromosome

# Main GA loop: evolves population and finds best layout
def genetic_algorithm(iterations=15, pop_size=6, crossover_method='single'):
    population = initial_population(pop_size)
    best = None

    for gen in range(iterations):
        # Sort population based on fitness
        population = sorted(population, key=lambda c: fitness(c))

        # Update best solution
        if best is None or fitness(population[0]) > fitness(best):
            best = copy.deepcopy(population[0])

        # Start new generation with elite member
        next_gen = [copy.deepcopy(population[0])]

        # Create offspring and fill the rest of the population
        while len(next_gen) < pop_size:
            p1, p2 = select_parents(population)
            if crossover_method == 'single':
                c1, c2 = single_point_crossover(p1, p2)
            else:
                c1, c2 = two_point_crossover(p1, p2)
            next_gen.extend([mutate(c1), mutate(c2)])

        # Update population for next generation
        population = next_gen[:pop_size]

    return best

# Run GA and print final result
if __name__ == "__main__":
    best_layout = genetic_algorithm(crossover_method='single')  # Use 'two' for Task 2
    print("Best layout:", best_layout)
    print("Wiring distance:", compute_wiring_distance(best_layout))
    print("Bounding area:", compute_bounding_area(best_layout))
    print("Overlap count:", count_overlaps(best_layout))
    print("Total Fitness:", fitness(best_layout))
