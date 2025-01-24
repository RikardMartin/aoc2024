#%%
def get_start_grid(input):
    pass
def get_position():
    pass
actions = []

def get_state(position, action):
    pass

def set_pos(pos, action, n_steps):
    grid[pos] = '.'
    pass


def take_action(action):
    symbol = get_state(position, action)
    while not symbol=='#':
        if symbol=='.':
            position = set_pos(position, action, 1)
            break

        else:
            if action=='<':
                pass
            if action=='>':
                pass
            if action=='^':
                pass
            if action=='v':
                pass
            
    return position







#%%
grid = get_start_grid(input)
position = get_position()

for action in actions:
    position = take_action(action)

gps_sum = compute_gps_sum(grid)


