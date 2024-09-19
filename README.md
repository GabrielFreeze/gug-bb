# GUG Boozy Bingo Manager
![image](https://github.com/user-attachments/assets/ebf85885-0076-4af6-b9f7-9f6b4fe87ddc)

A Python application for managing a "Boozy Bingo" event, where songs replace traditional bingo numbers. Implemented in Python using `DearPyGui` GUI Library:


## Features

1. Playlist Management:
   - Displays song lists for two rounds
   - Manual song navigation

2. Grid Verification:
   - Checks grid status based on input code
   - Shows grid layout in "Tombla View"
   - Highlights winning combinations

3. Status Updates:
   - Displays current round and song number
   - Shows status of checked grids

4. User Interface:
   - Sections for playlist, grid view, and controls

## Functionality

- Two rounds with separate playlists
- Grid verification for winning verses or full grid
- Manual song progression using next/previous buttons
- Real-time status updates for checked grids

## Technical Components

1. Data Management:
   - Uses pandas for CSV file handling
   - Loads song lists from text files

2. User Interface:
   - Built with DearPyGui
   - Main elements: playlist window, grid view, search menu, output display

3. Callbacks:
   - `search_btn_callback`: Grid verification
   - `next_btn_callback`, `prev_btn_callback`: Song navigation
   - `clear_btn_callback`: Resets view
   - `round_btn_callback`: Round switching

4. Grid Verification:
   - Checks winning conditions based on current song

5. Visual Feedback:
   - Color-coded grid cells and status information
   - Custom fonts for UI elements
