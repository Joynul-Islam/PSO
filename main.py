import random

import pygame
import Particles


def main():
    # -------- INITIAL SETUP -----------
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (1200, 800)
    screen = pygame.display.set_mode(size)

    # window name
    pygame.display.set_caption("Particle Swarm Optimisation - Visualisation")

    # text font to use
    font = pygame.font.SysFont(None, 24)

    # Loop until the user clicks the close button.
    end_simulation = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # frame counter
    frame = 0

    # -------- SIMULATION SETUP -----------

    # Initialising swarm
    swarm = [Particles.Particle(size[0], size[1], max_vel=2) for _ in range(100)]

    # images
    bee = pygame.image.load('images/bee.png')
    bee = pygame.transform.scale(bee, (18, 13))

    # sounds
    pygame.mixer.music.load("sounds/Bee-noise.wav")

    # -------- MAIN PROGRAM LOOP -----------
    # play sound
    pygame.mixer.music.play(-1)
    while not end_simulation:
        # --- Main loop ---

        # close program when window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_simulation = True

            # set new target location on mouseclick
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                Particles.Particle.target[0] = pos[0]
                Particles.Particle.target[1] = pos[1]

                # increase exploration tendency when new target is set
                new_target_tendencies()

        # --- Simulation logic
        frame += 1
        simulation_logic(swarm, frame)

        # adjust volume according to average speed
        adjust_volume(swarm)

        # --- Screen-clearing
        screen.fill((0, 0, 0))

        # --- Drawing code

        # Draw Target
        pygame.draw.circle(screen, (200, 200, 0), (Particles.Particle.target[0], Particles.Particle.target[1]), 8)

        # Draw particles
        draw_particles(screen, swarm)

        # Draw text
        draw_text(screen, font)

        # --- Update screen
        pygame.display.flip()

        # --- Frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


def new_target_tendencies():
    # temporarily change parameters to maximise exploration upon new target initialisation
    Particles.Particle.exploration_tendency = 10
    Particles.Particle.max_vel = 20
    Particles.Particle.local_tendency = 0
    Particles.Particle.global_tendency = 0


def simulation_logic(swarm, frame):
    # calculate distance to target for each particle
    for particle in swarm:
        particle.calculate_objective_function()

    # target shakes around (just for fun)
    Particles.Particle.shake_target(mag=10)

    # diminish exploration tendency and increase local and global tendencies as time goes on
    if frame % 10 == 0:
        Particles.Particle.decay_tendencies()
        Particles.Particle.decay_velocity()


def draw_particles(screen, swarm):
    for particle in swarm:
        particle.update_velocity()
        particle.update_location()

        # bee_rot = pygame.transform.rotate(bee, np.random.randint(0, 360))
        # screen.blit(bee_rot, (particle.location[0], particle.location[1]))

        # circle for head
        pygame.draw.circle(screen, (255, 255, 0), (particle.location[0], particle.location[1]), 3)

        # line length according to the velocity for perceived body trail
        pygame.draw.line(
            screen,
            particle.color,
            #(255, 255, 255),
            (
                particle.location[0],
                particle.location[1]
            ),
            (
                particle.location[0] - particle.velocity[0]*3,
                particle.location[1] - particle.velocity[1]*3
            ),
            2
        )


def draw_text(screen, font):
    img = font.render('explore: {}'.format(round(Particles.Particle.exploration_tendency, 2)), True, (255, 255, 255))
    screen.blit(img, (20, 20))

    img = font.render('local: {}'.format(round(Particles.Particle.local_tendency, 2)), True, (255, 255, 255))
    screen.blit(img, (20, 50))

    img = font.render('global: {}'.format(round(Particles.Particle.global_tendency, 2)), True, (255, 255, 255))
    screen.blit(img, (20, 80))


def adjust_volume(swarm):
    x = 0
    y = 0
    for particle in swarm:
        x += particle.velocity[0]
        y += particle.velocity[1]
    x = x/len(swarm)
    y = y/len(swarm)

    mag = (x**2 + y**2)**0.5

    if mag > 20:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(mag/10)
if __name__ == '__main__':
    main()
