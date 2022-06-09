import numpy as np


class Particle:
    # -- swarm properties

    # target location
    target = np.array([200,200])

    # closest location to target visited by any particle
    global_best = np.array([0, 0])

    def __init__(self, width, height, exploration_tendency=2, local_tendency=2, global_tendency=2, max_vel=10):
        # --- swarm variables ---

        Particle.width = width
        Particle.height = height
        Particle.exploration_tendency = exploration_tendency
        Particle.local_tendency = local_tendency
        Particle.global_tendency = global_tendency
        Particle.max_vel = max_vel

        # --- particle properties ---

        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

        # closest location to target visited by particle instance
        self.local_best = np.array([0, 0])

        # starting location of particle instance
        self.location = np.array([
            np.random.randint(0, Particle.width),
            np.random.randint(0, Particle.height)
        ])

        # randomly set velocity with max being max_val% of search space
        self.velocity = np.array([
            Particle.width * (np.random.randint(-Particle.max_vel, Particle.max_vel) / 1000),
            Particle.height * (np.random.randint(-Particle.max_vel, Particle.max_vel) / 1000)
        ])

    def update_velocity(self):
        # set velocity based on exploration, past-experience and swarm tendencies

        # inertia --> exploration's influence on velocity
        inertia = self.velocity * np.random.rand() * Particle.exploration_tendency

        # cognition --> past experience's influence on velocity
        cognition = (self.local_best - self.location) * np.random.rand() * Particle.local_tendency

        # social --> swarm's influence on velocity
        social = (Particle.global_best - self.location) * np.random.rand() * Particle.global_tendency

        self.velocity = inertia + cognition + social

        # cap velocity at max_val% of searchable area if it has gone above
        self.velocity[0] = min(
            abs(self.velocity[0]),
            abs((Particle.max_vel/1000)*Particle.width)) * np.sign(self.velocity[0])

        self.velocity[1] = min(
            abs(self.velocity[1]),
            abs((Particle.max_vel/1000)*Particle.height)) * np.sign(self.velocity[1])

    def update_location(self):
        # update location with new velocity
        self.location = self.location + self.velocity

    def calculate_objective_function(self):
        # see if particle is closer to target and update local and global 'best' vectors
        local_best_distance_to_target = np.linalg.norm(Particle.target - self.local_best)
        current_distance_to_target = np.linalg.norm(Particle.target - self.location)

        if current_distance_to_target < local_best_distance_to_target:
            self.local_best = self.location

            global_best_distance_to_target = np.linalg.norm(Particle.target - Particle.global_best)
            if current_distance_to_target < global_best_distance_to_target:
                Particle.global_best = self.local_best

    @classmethod
    def decay_tendencies(cls):
        cls.local_tendency += 0.01
        cls.global_tendency += 0.01
        cls.exploration_tendency *= 0.5

        if cls.exploration_tendency < 2:
            cls.exploration_tendency = 2

        if cls.local_tendency > 2:
            cls.local_tendency = 2
        if cls.global_tendency > 2:
            cls.global_tendency = 2

    @classmethod
    def decay_velocity(cls):
        cls.max_vel *= 0.8
        if cls.max_vel < 5:
            cls.max_vel = 5

    @classmethod
    def shake_target(cls, mag=3):
        cls.target[0] += np.random.randint(-mag, mag)
        cls.target[1] += np.random.randint(-mag, mag)
