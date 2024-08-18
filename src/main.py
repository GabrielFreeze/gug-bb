import os
from copy import deepcopy
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

MAX_WIDTH = 1920
MAX_HEIGHT = 1020

dpg.create_context()
dpg.create_viewport(title='Boozy Bingo Manager', width=MAX_WIDTH,height=MAX_HEIGHT+60)

kwargs = dict(
    label="Boozy Bingo Manager",
    no_bring_to_front_on_focus=True,
    no_scrollbar = True,menubar      = False,
    no_move      = True,no_resize    = True,
    no_collapse  = True,no_close     = True,
)

songs = [f"{str(i+1).zfill(3)}. Name of a Song by Artist" for i in range(200)]

song_counter = -1

def highlight_active_song(user_data):

    songs = deepcopy(user_data['songs'])
    curr_idx = user_data['song_counter']
    # next_idx = (curr_idx+1)%len(songs)

    songs[curr_idx] = songs[curr_idx][:5]+ "[PLAYING] " + songs[curr_idx][5:]
    # songs[next_idx] = songs[next_idx][:5]+ "[NEXT] "    + songs[next_idx][5:]

    return songs

def next_btn_callback(sender,app_data,user_data):
    user_data['song_counter'] += 1
    
    display_songs = highlight_active_song(user_data)
    
    #Highlight movement of playlist
    dpg.configure_item("playlist",
        items=display_songs,
        default_value=display_songs[user_data['song_counter']]
    )

def prev_btn_callback(sender,app_data,user_data):
    raise NotImplementedError()

#Prepare Fonts
with dpg.font_registry():
    default_font = dpg.add_font(os.path.join("..","fonts","Roboto-Regular.ttf"), 30)
    list_font    = dpg.add_font(os.path.join("..","fonts","JetBrainsMonoNL-Italic.ttf"), 25)
    label_font   = dpg.add_font(os.path.join("..","fonts","JetBrainsMonoNL-Italic.ttf"), 20)

#Prepare Images
width, height, channels, data = dpg.load_image(os.path.join("..","imgs","test.jpg"))
with dpg.texture_registry():
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="ichika")



with dpg.window(width=MAX_WIDTH, height=MAX_HEIGHT,**kwargs):
    dpg.bind_font(default_font) #Set Font


    with dpg.group(horizontal=True):
        #PlayList Window
        with dpg.child_window(width=MAX_WIDTH//4):
            with dpg.group(horizontal=False):
                playlist_label = dpg.add_text("Playlist")

                playlist = dpg.add_listbox(
                    num_items=30,
                    width=MAX_WIDTH//4,
                    items=songs,enabled=False,
                    tag="playlist")
                dpg.bind_item_font(playlist,list_font)
                dpg.bind_item_font(playlist_label,label_font)
                
                
                with dpg.child_window(width=MAX_WIDTH//4,no_scroll_with_mouse=True):
                    with dpg.group(horizontal=True):
                        
                        next_btn = dpg.add_button(
                            enabled=True, label="« PREV",
                            callback=prev_btn_callback,
                            width=MAX_WIDTH//8,
                            pos=(0,0),
                            user_data={
                                "songs":songs,
                                "song_counter":song_counter
                            }
                        )
                        next_btn = dpg.add_button(
                            enabled=True, label="NEXT »",
                            callback=next_btn_callback,
                            width=MAX_WIDTH//8,
                            pos=(MAX_WIDTH//8,0),
                            user_data={
                                "songs":songs,
                                "song_counter":song_counter
                            })
                        
        #Grid Search Window
        dpg.add_image("ichika")

        
        


    
    


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()