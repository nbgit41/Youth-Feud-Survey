import time

from playsound import playsound

sounds_dir = "SFX"

sound_effects = {
    "buzz": "buzzed-in.mp3",
    "correct" : "correct.mp3",
    "strike" : "strike.mp3",
    "intro" : "Introduction Casey_mixdown_01.mp3",
    "run" : "ElevenLabs_Frederick Surrey_program running.mp3",
    "stop" : "ElevenLabs_Frederick_Surrey_Program_Stopping.mp3",
    "broke" : "ElevenLabs_Frederick Surrey_rip something broke.mp3",
    "reset-buzz": "ElevenLabs_Frederick Surrey_resetting-buzzer.mp3",
    "starting-game": "ElevenLabs_Frederick Surrey_starting-game.mp3",
    "add-one-to-q-num": "ElevenLabs_Frederick Surrey_adding-one-to-current-question-number.mp3",
    "sub-one-from-q-num": "ElevenLabs_Frederick Surrey_subtracting-one-from-current-question-number.mp3",
    "add-boys": "ElevenLabs_Frederick Surrey_the boys have scored a point.mp3",
    "add-girls":"ElevenLabs_Frederick Surrey_the girls have scored a point.mp3",
    "sub-boys":"ElevenLabs_Frederick Surrey_oops boys.mp3",
    "sub-girls":"ElevenLabs_Frederick Surrey_oops girls.mp3",
    "2": "ElevenLabs_Frederick Surrey_question 2.mp3",
    "3": "ElevenLabs_Frederick Surrey_question 3.mp3",
    "4": "ElevenLabs_Frederick Surrey_question 4.mp3",
    "5": "ElevenLabs_Frederick Surrey_question 5.mp3",
    "6": "ElevenLabs_Frederick Surrey_question 6.mp3",
    "7": "ElevenLabs_Frederick Surrey_question 7.mp3",
    "8": "ElevenLabs_Frederick Surrey_question 8.mp3",
    "9": "ElevenLabs_Frederick Surrey_question 9.mp3",
    "10": "ElevenLabs_Frederick Surrey_question 10.mp3",
    "11": "ElevenLabs_Frederick Surrey_question 11.mp3"
}

def play_sound(sound_name):
    try:
        sound_file = sound_effects.get(sound_name)
        if sound_file:
            playsound(f"{sounds_dir}/{sound_file}")
            time.sleep(2)
        else:
            print(f"Error: Sound '{sound_name}' not found in sound_effects dictionary")
            return
    except Exception as e:
        print(f"Failed to play {sound_name}: {e}")

#usage
#---------------------------------------------------Sound Effects-------------------------------------------------------
# toggle_sounds = True  # Toggle sound effects
#
# def play_sound_thread(sound_name):
#     """Plays sound in a separate thread to prevent lag."""
#     if deb:
#         print("-------------------------------------------play_sound_thread-------------------------------------------")
#     if toggle_sounds:
#         sound_thread = threading.Thread(target=play_sound, args=(sound_name,), daemon=True)
#         if deb:
#             print(f"PLAYING {sound_name} !!!!!!!!!!!!!!!!!!!!!")
#         sound_thread.start()
