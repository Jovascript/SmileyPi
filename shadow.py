import ephem
import math
import time

#https://celestrak.com/columns/v03n01/

tle = """ISS (ZARYA)             
1 25544U 98067A   16361.25108796  .00002357  00000-0  43144-4 0  9992
2 25544  51.6423 180.3972 0006614  16.8508 319.5828 15.53941827 34859"""

def au_to_m(au):
    '''Convert astronomical units to metres'''
    return au*149597870700

def coord_dist(c1, c2):
    '''Find the distance between two sets of coords'''
    sqrsum = 0
    for diff in coord_diff(c1, c2): # For every dimension(could be 1, could be 5!)
        sqrsum += diff**2 # Do a pythogoras
    return math.sqrt(math.fabs(sqrsum))

def coord_diff(c1, c2):
    '''Find the diffrence between two sets of coords'''
    diff = []
    for i in range(len(c1)): # Any number of coord dimensions
        diff.append(c2[i] - c1[i])
    return tuple(diff)

    
def dot_product(c1,c2):
    '''Find the dot product of two vectors, given their end point(start point is the origin)'''
    dot = 0
    for i in range(len(c1)):
        dot += c1[i]*c2[i]
    return dot

def get_eci(ra, dec, dist):
    '''Get the Earth Centered Inertial Coords, given dist and spherical'''
    x = dist * math.cos(dec) * math.cos(ra)
    y = dist * math.cos(dec) * math.sin(ra)
    z = dist * math.sin(dec)
    return (x,y,z)

def load_tle(tle):
    '''Load a tle'''
    # The pyephem readtle function is so annoying, using argument spread.
    return ephem.readtle(*tle.split("\n"))

def calculate_shadow():
    '''Calculates properties of the shadow on the ISS.
    Returns: penumbra, umbra, light_percentage'''

    # Calculate earth centered coords of sun.
    sun = ephem.Sun()
    sun.compute()
    sun_coords = get_eci(sun.a_ra, sun.a_dec, au_to_m(sun.earth_distance))

    # Calculate earth centered coords of ISS 
    iss = load_tle(tle)
    iss.compute()
    iss_dist = iss.elevation+ephem.earth_radius
    iss_coords = get_eci(iss.a_ra, iss.a_dec, iss_dist)

    # Earth Centered coords of Earth :)
    earth_coords = (0,0,0)

    # Let us begin the maths

    # Distance between sun and ISS
    sun_dist = coord_dist(sun_coords, iss_coords)

    # The amount(angle) the earth's radius takes up from the ISS
    theta_earth = math.asin(ephem.earth_radius/iss_dist)
    # The amount(angle) the sun's radius takes up from the ISS
    theta_sun = math.asin(ephem.sun_radius/sun_dist)
    # The percieved angle between the sun's and the earth's centers
    theta = math.acos(dot_product(coord_diff(iss_coords, earth_coords), coord_diff(iss_coords, sun_coords))/(sun_dist*iss_dist))

    # Whether the ISS is in the umbra(if the earth is seen to fully eclipse the sun)
    umbra = (theta_earth > theta_sun) and theta < (theta_earth - theta_sun)
    # Whether the ISS is in the penumbra(if the earth is seen to partially eclipse the sun)
    penumbra = (theta_earth - theta_sun) < theta < (theta_earth + theta_sun)

    # Only worth calculating while in penumbra
    if penumbra:
        # Minimum and maximum theta can be for penumbra(bounds of penumbra)
        theta_min = theta_earth - theta_sun
        theta_max = theta_earth + theta_sun
        # Range of possible theta values
        theta_range = theta_max = theta_min
        if (theta_range == 0):
            # Unlikely
            percent_value = 0
        else:
            percent_range = (100 - 0)  # From 0 to 100
            # Transform theta value into percentage, given the two ranges
            percent_value = (((theta - (theta_earth - theta_sun)) * percent_range) / theta_range) + 0
    elif umbra:
        percent_value = 0 # No light in umbra
    else:
        percent_value = 100 # Lots of light without shadow

    return penumbra, umbra, round(percent_value)

def is_umbra():
    penumbra, umbra, light = calculate_shadow()
    return umbra
def is_penumbra():
    penumbra, umbra, light = calculate_shadow()
    return penumbra
def get_light_intensity():
    penumbra, umbra, light = calculate_shadow()
    return light
def is_shadow():
    penumbra, umbra, light = calculate_shadow()
    return (penumbra or umbra)
