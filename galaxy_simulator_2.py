"""Build 2-D model of a galaxy, post the expansion rings for galactic empire."""
import tkinter as tk
import time
from random import randint, uniform, random
import math

# ==============================================================================
# MAIN INPUT

# location of galactic empire homeworld on map:
HOMEWORLD_LOC = (0, 0)

# maximum number of years to simulate
MAX_YEARS = 10000000

# average expansion velocity as fraction of speed of light
SPEED = 0.005

# scale units
UNIT = 200

# ==============================================================================

# set up display canvas
root = tk.Tk()
root.title("Milky Way Galaxy")
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

# actual milky way dimensions
DISC_RADIUS = 50000  # Light years

disc_radius_scaled = round(DISC_RADIUS/UNIT)


def polar_coordinates():
    """Generate random x, y point on a disc for a 2-D display"""
    # choose random values for r and theta
    r = random()
    theta = uniform(0, 2 * math.pi)

    # x, y calculated using polar coordinates, disc radius scales length
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y


def spirals(b, r, rot_fac, fuz_fac, arm):
    """Build spiral arms for tkinter display using logarithmic spiral formula

    b = arbitary constant in logarithmic spiral equation
    r = scaled galactic disc radius
    rot_fac = rotation factor
    fuz_fac = random shift in star position in arm
    arm = spiral arm (0 = main arm, 1 = trailing stars)
    """
    spiral_stars = []
    fuzz = int(0.030 * abs(r))  # randomly shift star locations
    theta_max_degrees = 520

    # loop through each value of theta and calculate x and y values using
    # logarithmic spiral equation
    for i in range(theta_max_degrees):  # range(0, 600, 2) for no black hole
        theta = math.radians(i)
        x = r * math.exp(b * theta) * math.cos(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac
        y = r * math.exp(b * theta) * math.sin(theta + math.pi * rot_fac)\
            + randint(-fuzz, fuzz) * fuz_fac

        spiral_stars.append((x, y))

    for x, y in spiral_stars:
        # arm = 0 is main arms, arm = 1 is secondary trailing arms of spiral
        if arm == 0 and int(x % 2) == 0:
            # even points give large stars
            c.create_oval(x-2, y-2, x+2, y-2, fill='white', outline='')
        elif arm == 0 and int(x % 2) != 0:
            # odd points give medium stars
            c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')

        elif arm == 1:
            # small stars
            c.create_oval(x, y, x, y, fill='white', outline='')


def star_haze(disc_radius_scaled, density):
    """random distribute faint tkinter stars in a galactic disc

    disc radius scaled = galatic disc radius scaled to radio bubble diameter
    density = multiplier to vary numer of stars posted
    """

    # loop through a range proportional to the the size of the galaxy disc
    # and gather x, y coordinates for tiny stars
    for i in range(0, disc_radius_scaled * density):
        x, y = polar_coordinates()
        c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')


def model_expansion():
    """Model empire expansion from homeworld with concentric rings"""
    r = 0  # radius from homeworld
    text_y_loc = -290
    x, y = HOMEWORLD_LOC

    # create oval to display where homeworld is at the centre
    c.create_oval(x-5, y-5, x+5, y+5, fill='red')
    increment = round(MAX_YEARS/10)  # year interval to post circles
    c.create_text(-475, -350, anchor='w', fill='red', text='Increment = {:,}'
                  .format(increment))
    c.create_text(-475, -325, anchor='w', fill='red',
                  text='Velocity as fraction of light = {:,}'.format(SPEED))

    # loop through the number of years
    for years in range(increment, MAX_YEARS + 1, increment):
        time.sleep(0.5)  # delay before posting new expansion circle
        travelled = SPEED * increment / UNIT
        r = r + travelled

        # create circle of expansion from travelling as a certain speed
        # and display how many years you have been travelling
        c.create_oval(x-r, y-r, x+r, y+r, fill='', outline='red', width='2')
        c.create_text(-475, text_y_loc, anchor='w', fill='red',
                      text='Years = {:,}'.format(years))
        text_y_loc += 20

        # update canvas for new circle; no longer need mainloop
        c.update_idletasks()
        c.update()


def main():
    """Generate galaxy display, model empire expansion, run mainloop."""
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=- -2.09, fuz_fac=1, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(disc_radius_scaled, density=8)

    model_expansion()
    root.mainloop()


if __name__ == '__main__':
    main()
