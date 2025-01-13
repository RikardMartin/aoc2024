"""
Load all positions and velocities to a list.
For each robot:
    Get the starting position.
    Add to its position its velocity multiplied by the number of seconds and save as destination.
    Divide the x-destination by the length of the grid and save the remainder.
    Set its x-endpoint as the remainder.
    Do the same but for the y-axis.

Find the median in x and y on the "grid".
For all endpoints:
    If y is less than med-y:
        If x is less than med-x:
            count +1 in first quadrant.
        elif x is more than med-x:
            count +1 in second quadrant.
    elif Y is more than med-y:
        If x is less than med-x:
            count +1 in third quadrant.
        elif x is more than med-x:
            count +1 in fourth quadrant.

multiply the four quadrant numbers together.
"""
#%%
