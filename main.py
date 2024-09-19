import os
import pandas as pd
from copy import deepcopy
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

#Dimensions of Window
MAX_W = 1920
MAX_H = 1020
PAD = 10

#Tombla Grid Specifications
GRID_X=5
GRID_Y=3
GRID_W = 0.75*MAX_W - 45
GRID_H = 0.50*MAX_W
CELL_TEXT_INDENT=30

GREEN   = [000,200,  0,255]
L_GREEN = [105,186,101,255]
RED     = [200,  0,  0,255]
PINK    = [200, 36,209,255]
GREY    = [115,112,113,255]
ORANGE  = [217,162, 11,255]

kwargs = dict(
    label="Boozy Bingo Manager - (c)Gabriel_Freeze",
    no_bring_to_front_on_focus=True,
    no_scrollbar = True,menubar      = False,
    no_move      = True,no_resize    = True,
    no_collapse  = True,no_close     = True,
)

#Load songs and number them
with open(os.path.join("assets","songs","songs_1.txt"), 'r', encoding='utf-8') as f:
    songs_1 = [song[:-1] for song in f.readlines()]

with open(os.path.join("assets","songs","songs_2.txt"), 'r', encoding='utf-8') as f:
    songs_2 = [song[:-1] for song in f.readlines()]


song2idx_1 = {song:i for i,song in enumerate(songs_1)}
song2idx_2 = {song:i for i,song in enumerate(songs_2)}
song2idx = [song2idx_1,song2idx_2]

songs_1 = [f"{str(i+1).zfill(3)}. {song}" for i,song in enumerate(songs_1)]
songs_2 = [f"{str(i+1).zfill(3)}. {song}" for i,song in enumerate(songs_2)]
songs = [songs_1,songs_2]


#TODO: To make round choosing via GUI

df_1 = pd.read_csv(os.path.join("assets","grids",f"grids_1","data.csv"))
df_2 = pd.read_csv(os.path.join("assets","grids",f"grids_2","data.csv"))
dfs = [df_1,df_2]



def load_grid(grid_idx:int):
    round_n = dpg.get_value("round_n")

    grid = pd.read_csv(os.path.join("assets","grids",f"grids_{round_n+1}",f'{grid_idx}.csv'),
                       sep=';',header=None)
    grid = grid.to_numpy().tolist()
    return grid
def highlight_table_row(grid,row,color):
    for x in range(GRID_X):
        dpg.highlight_table_cell(grid,row,x, color)
def _search_btn_callback(sender,app_data,user_data):
    search_btn_callback(
        user_data['sender'],
        dpg.get_value(user_data['sender']),
        user_data['user_data']
    )
def search_btn_callback(sender,app_data,user_data):
    
    key_idx = app_data    
    display = user_data['display']
    display_cells = user_data['grid_cells']
    round_n = dpg.get_value("round_n")


    info = user_data['info']
    song_counter = dpg.get_value("song_counter")%len(songs[round_n])
    df = dfs[round_n]


    if key_idx == "":
        return
    else:
        key_idx = int(key_idx)


    #Retrieve key grid
    if not (0 <= key_idx < len(df)):
        dpg.set_value(info,f"[ERROR]: `{key_idx}` is not a valid grid. Grids must be in the range [0-{len(df)-1}]")
        dpg.configure_item(info, color=RED)
        return
    
    key_info = df.iloc[key_idx]
    key_grid = load_grid(key_idx)
    status_text = f"Currently viewing Grid {key_idx}\n"

    #Display key grid on display grid and mark valid cells
    for y in range(GRID_Y):
        for x in range(GRID_X):

            song = key_grid[y][x]
            dpg.set_value(display_cells[y][x], song)

            if song2idx[round_n][song] <= song_counter:
                dpg.highlight_table_cell(display,y,x, ORANGE)
            else:
                dpg.highlight_table_cell(display,y,x, GREY)
    

    has_vers  = False
    has_kaxxa = False
    color = ORANGE
    vers_text = ""
    #Display any valid versi by consulting the winner sheet
    for vers_n in [1,2,3]:
        if key_info[f'Vers {vers_n}'].item() <= song_counter:
            #Highlight row in light green
            highlight_table_row(display, vers_n-1, L_GREEN)
            vers_text += f"[VERS]: Grid {key_idx} has matched the {['top','middle','bottom'][vers_n-1]} verse with the following songs:\n"
            has_vers = True
            for x in range(GRID_X):
                vers_text += f"\t& {dpg.get_value(display_cells[vers_n-1][x])}\n"
    
    if not has_vers:
        status_text += "[VERS]: NONE\n"
    else:
        status_text += '\n'
        color = L_GREEN
        
    #Highlight entire table in L_ 
    if key_info['Kaxxa'].item() <= song_counter:
        has_kaxxa = True
        highlight_table_row(display, 0, GREEN)
        highlight_table_row(display, 1, GREEN)
        highlight_table_row(display, 2, GREEN)

    if not has_kaxxa:
        status_text += "[KAXXA]: NONE\n"
    else:
        vers_text = ""
        status_text += f"[KAXXA]: Grid {key_idx} has got a tombla!!!11!1!\n"
        color=L_GREEN

    status_text += vers_text

    dpg.set_value(info,status_text)
    dpg.configure_item(info, color=color)

def highlight_active_song(user_data):

    display_songs = deepcopy(songs[dpg.get_value("round_n")])
    curr_idx = dpg.get_value("song_counter")%len(display_songs)

    display_songs[curr_idx] = display_songs[curr_idx][:5]+ "[PLAYING] " + display_songs[curr_idx][5:]

    return display_songs   
def next_btn_callback(sender,app_data,user_data):
    n = dpg.get_value("song_counter")
    dpg.set_value("song_counter", n:=n+1)

    display_songs = highlight_active_song(user_data)
    dpg.set_value(user_data['song_counter_text'], f"Song: {(n%len(display_songs))+1}")
    
    #Highlight movement of playlist
    dpg.configure_item("playlist",
        items=display_songs,
        default_value=display_songs[n%len(songs[dpg.get_value("round_n")])]
    )
def prev_btn_callback(sender,app_data,user_data):
    n = dpg.get_value("song_counter")
    dpg.set_value("song_counter", n:=n-1)

    display_songs = highlight_active_song(user_data)
    dpg.set_value(user_data['song_counter_text'], f"Song: {(n%len(display_songs))+1}")
    
    #Highlight movement of playlist
    dpg.configure_item("playlist",
        items=display_songs,
        default_value=display_songs[n%len(songs[dpg.get_value("round_n")])]
    )
def clear_btn_callback(sender,app_data,user_data):
    display = user_data['display']
    display_cells = user_data['grid_cells']
    info = user_data['info']

    #Clear table
    for y in range(GRID_Y):
        for x in range(GRID_X):
            dpg.set_value(display_cells[y][x], "")
            dpg.highlight_table_cell(display,y,x, GREY)

    #Clear status info output box
    dpg.set_value(info,"Status info will show up here..")
    dpg.configure_item(info, color=GREY)
def round_btn_callback(sender,app_data,user_data):
    
    #Clear grid and textbox
    clear_btn_callback(sender,app_data,user_data)

    #Update round number
    round_n = (dpg.get_value("round_n")+1)%2
    dpg.set_value("round_n", round_n)
    dpg.set_value(user_data['round_counter_text'], f"Round: {round_n+1}")

    #Update song counter
    dpg.set_value("song_counter", 0)
    dpg.set_value(user_data['song_counter_text'],  f"Song: 0")

    #Update playlist
    dpg.configure_item("playlist", items=songs[round_n])

dpg.create_context()
dpg.create_viewport(title='Bingo Booze BBQ Manager', width=MAX_W,height=MAX_H+60)

#Prepare Global Values
with dpg.value_registry():
    song_counter = dpg.add_int_value(default_value=0, tag="song_counter")
    round_n = dpg.add_int_value(default_value=0, tag="round_n") #1st round = 0, 2nd round = 1

#Prepare Fonts
with dpg.font_registry():
    default_font = dpg.add_font(os.path.join("assets","fonts","JetBrainsMonoNL-Regular.ttf"), 30)
    input_font   = dpg.add_font(os.path.join("assets","fonts","JetBrainsMonoNL-Regular.ttf"), 45)
    list_font    = dpg.add_font(os.path.join("assets","fonts","JetBrainsMonoNL-Italic.ttf" ), 23)
    grid_font    = dpg.add_font(os.path.join("assets","fonts","JetBrainsMonoNL-Regular.ttf"), 25)
    label_font   = dpg.add_font(os.path.join("assets","fonts","JetBrainsMonoNL-Italic.ttf" ), 20)


with dpg.window(width=MAX_W, height=MAX_H,**kwargs):
    dpg.bind_font(default_font) #Set Font
    user_data = {}


    with dpg.group(horizontal=True):
        #PlayList Window
        with dpg.child_window(width=0.25*MAX_W + PAD):
            with dpg.group(horizontal=False):
                playlist_label = dpg.add_text("Playlist",indent=PAD)

                playlist = dpg.add_listbox(
                    num_items=32,
                    width=0.25*MAX_W,
                    items=songs[dpg.get_value("round_n")],enabled=False,
                    tag="playlist")
                dpg.bind_item_font(playlist,list_font)
                dpg.bind_item_font(playlist_label,label_font)
                
                with dpg.child_window(width=0.25*MAX_W + PAD,no_scroll_with_mouse=True):
                    with dpg.group(horizontal=True):     
                        prev_btn = dpg.add_button(
                            enabled=True, label="« PREV",
                            callback=prev_btn_callback,
                            user_data=user_data,
                            width=MAX_W//8,
                            pos=(0,0),
                        )
                        next_btn = dpg.add_button(
                            enabled=True, label="NEXT »",
                            callback=next_btn_callback,
                            user_data=user_data,
                            width=MAX_W//8,
                            pos=(MAX_W//8,0),
                        )

        #Grid Search Window
        with dpg.child_window(width=GRID_W):
            
            table_kwargs = dict(
                header_row=False,    row_background=False,
                borders_innerH=True, borders_outerH=True,
                borders_innerV=True, borders_outerV=True,
                delay_search=True,
            )
            
            #Tombla Label
            grid_label = dpg.add_text("Tombla View",indent=PAD)
            grid_cells = [[None for _ in range(GRID_X)] for _ in range(GRID_Y)]
            dpg.bind_item_font(grid_label,label_font)

            with dpg.table(**table_kwargs) as grid:
                dpg.bind_item_font(grid,grid_font)

                #Add Columns
                for _ in range(GRID_X):
                    dpg.add_table_column()
                
                #Add placeholder text in cells
                for i in range(GRID_Y):
                    with dpg.table_row(height= GRID_H//GRID_X):
                        for j in range(GRID_X):
                            dpg.highlight_table_cell(grid, i, j, GREY)
                            grid_cells[i][j] = dpg.add_text(
                                f"\n\n",
                                wrap=(GRID_W//GRID_X) - CELL_TEXT_INDENT*1.55,
                                indent=CELL_TEXT_INDENT
                            )
            
            #Dashbaord Section
            with dpg.child_window(width=GRID_W-15,autosize_y=True):
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=0.25*GRID_W,autosize_y=True):        
                        with dpg.group(horizontal=False):
                            search_label = dpg.add_text("Search Menu",indent=PAD)
                            dpg.bind_item_font(search_label,label_font)

                            user_data["display"]    = grid
                            user_data["grid_cells"] = grid_cells

                            #Grid Input + Search Button
                            with dpg.group(horizontal=True):
                                dpg.add_text("Enter Grid:")
                                grid_input = dpg.add_input_text(
                                    callback=search_btn_callback,
                                    user_data=user_data,
                                    decimal=True,on_enter=True,
                                    width=MAX_W//12,
                                    hint="")
                                dpg.bind_item_font(grid_input,input_font)
                            
                            search_btn = dpg.add_button(
                                enabled=True, label="SEARCH",
                                callback =_search_btn_callback,
                                user_data = {
                                    "sender": grid_input,
                                    "user_data":user_data,
                                },
                                width=GRID_W//4 - 15,
                            )

                            dpg.add_spacer(height=PAD)
                            
                            #Show round and song number information
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=PAD*3)
                                round_counter_text = dpg.add_text(label="round_counter_text",
                                                                    default_value="Round: 1")
                                dpg.add_text("|")
                                song_counter_text = dpg.add_text(label="song_counter_text",
                                                                    default_value="Song: 1")

                                #So they can be modified by the navigation button callbacks
                                user_data['round_counter_text'] = round_counter_text
                                user_data['song_counter_text']  = song_counter_text
                            
                            
                            clear_btn = dpg.add_button(
                                enabled=True, label="CLEAR",
                                callback = clear_btn_callback,
                                user_data = user_data,
                                width=GRID_W//4 - 15,
                            )
                            round_btn = dpg.add_button(
                                enabled=True, label="NEXT ROUND",
                                callback = round_btn_callback,
                                user_data = user_data,
                                width=GRID_W//4 - 15,
                            )

                    #Output Section
                    with dpg.child_window(width=0.75*GRID_W - 40,autosize_y=True):
                        output_label = dpg.add_text("Output",indent=PAD,color=PINK)
                        dpg.bind_item_font(output_label,label_font)

                        info = dpg.add_text(
                            "Status info will show up here..",
                            wrap=0.75*GRID_W - 40,
                            color=GREY,
                        )
                        dpg.bind_item_font(info,grid_font)
                        user_data["info"] = info


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()



