#%%
def get_start_grid(input):
    pass
def get_position():
    pass
actions = []

def get_state(position, action):
    pass

def set_pos(pos, action, n_steps):
    if action=='^': pos = (pos[0]-n_steps, pos[1])
    elif action=='>': pos = (pos[0], pos[1]+n_steps)
    elif action=='v': pos = (pos[0]+n_steps, pos[1])
    elif action=='<': pos = (pos[0], pos[1]-n_steps)
    
    return pos

def move_left(pos):
    count = 3
    state = grid[(pos[0], pos[1]-count)]
    while state in ('[', ']'):
        count += 1
        state = grid[(pos[0], pos[1]-count)]
    if state=='#':
        return pos
    else:
        for i in range(count, 1, -1):
            grid[(pos[0], pos[1]-i)] = grid[(pos[0], pos[1]-i+1)]
        grid[(pos[0], pos[1])] = '.'

def move_up(pos):
    pass
        
#%%
grid = get_start_grid(input)
position = get_position()

for action in actions:
    symbol = get_state(position, action)
    while not symbol=='#':

        if symbol=='.':
            grid[position] = '.'
            position = set_pos(position, action, 1)
            grid[position] = '@'
            break

        else:
            if (action=='<'):
                position = move_left(position)
            if action=='>':
                pass
            if action=='^':
                position = move_up(position)
            if action=='v':
                pass

gps_sum = compute_gps_sum(grid)


