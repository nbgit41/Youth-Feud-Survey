import threading, keyboard, json, time
from flask import Flask, jsonify, request, render_template
from play_sound_plz import play_sound
from TTS_this import say_this
import eventlet
import eventlet.wsgi
from flask_socketio import SocketIO

deb = False  # Print debugging stuff
port_poggies = 8400
app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")  # Use eventlet for WebSocket


#---------------------------------------------------Sound Effects-------------------------------------------------------

buzzer_playable = True  # Prevent multiple buzzes
toggle_sounds = True  # Toggle sound effects
toggle_who_asked = True

def play_sound_thread(sound_name):
    """Plays sound in a separate thread to prevent lag."""
    if deb:
        print("-------------------------------------------play_sound_thread-------------------------------------------")
    if toggle_sounds:
        sound_thread = threading.Thread(target=play_sound, args=(sound_name,), daemon=True)
        if deb:
            print(f"PLAYING {sound_name} !!!!!!!!!!!!!!!!!!!!!")
        sound_thread.start()

def say_tts_thread(say_this_thing_plz):
    if deb:
        print("-------------------------------------------tts_thread-------------------------------------------")
    if toggle_sounds:
        tts_thread = threading.Thread(target=say_this, args=(say_this_thing_plz,), daemon=True)
        if deb:
            print(f"---------------------About to say: {say_this_thing_plz} !!!!!!!!!!!!!!!!!!!!!---------------------")
        tts_thread.start()

def play_we_asked():
    if toggle_who_asked:
        play_sound_thread(f"{current_question}")

#---------------------------------------------------Buzzer--------------------------------------------------------------

def on_t():
    """Handles reset key press."""
    global buzzer_playable
    if deb:
        print("--------------------------------------pressed t, resetting buzzer--------------------------------------")
    reset_buzzer()
    buzzer_playable = True

def reset_buzzer():
    """Resets the buzzer state."""
    global player_buzzed
    if deb:
        print("--------------------------------------------reset buzzer def--------------------------------------------")
    with buzz_lock:
        player_buzzed = None

def update_buzzer_status():
    """Updates the buzzer status."""
    global player_buzzed
    # if deb:
    #     print("-----------------------------------------update buzzer status-----------------------------------------")

player_buzzed = None
buzz_lock = threading.Lock()\

@app.route("/buzz", methods=["POST"])
def buzz():
    """Handles a player buzz."""
    global player_buzzed
    if deb:
        print("-------------------------------------------------/buzz-------------------------------------------------")
        say_tts_thread("buzz")
    with buzz_lock:
        if player_buzzed is None:
            data = request.json
            player_buzzed = data.get("player")
    return jsonify({"status": "success"})

@app.route("/status", methods=["GET"])
def status():
    """Returns the current buzzer status."""
    global player_buzzed
    # if deb:
    #     print("------------------------------------------------/status------------------------------------------------")
    return jsonify({"player": player_buzzed})

#to reset the buzzer by clicking on the buzzed player text element
@app.route("/reset-buzzer", methods=["GET"])
def reset_the_buzzer_plz():
    if deb:
        print("---------------------------------------------Reset Buzzer Plz---------------------------------------------")
        play_sound_thread("reset-buzz")
    reset_buzzer()
    return jsonify({"status": "success"})


#---------------------------------------------------Game Start----------------------------------------------------------

@app.route("/start-game", methods=["POST"])
def start_game():
    if deb:
        print("----------------------------------------------/start-game----------------------------------------------")
    """Plays the game start sound."""
    play_sound_thread("intro")
    return jsonify({"status": "success"})


#---------------------------------------------------Update Score--------------------------------------------------------

@app.route("/update_score/<team>/<amount>", methods=["POST"])
def update_score(team, amount):
    if deb:
        print(f"------------------------------------/update-score/{team}/{amount}------------------------------------")
    """Updates the score for the given team and saves it to the file."""
    try:
        amount = int(amount)  # Convert the amount to an integer
        if team not in ["boys", "girls"]:
            return jsonify({"success": False, "error": "Invalid team"}), 400

        score_file = f"{team}_score.txt"

        #play funny narrator sounds for each team
        if deb:
            if amount >= 1 and team == "boys":
                play_sound_thread("add-boys")
            elif amount <= 0 and team == "boys":
                play_sound_thread("sub-boys")
            elif amount >= 1 and team == "girls":
                play_sound_thread("add-girls")
            elif amount <= 0 and team == "girls":
                play_sound_thread("sub-girls")

        # Read the current score
        with open(score_file, "r", encoding="utf-8") as file:
            current_score = int(file.read().strip())

        # Update the score, ensuring it doesn't go below 0
        new_score = current_score + amount

        # Save the new score
        with open(score_file, "w", encoding="utf-8") as file:
            file.write(str(new_score))

        return jsonify({"success": True, "new_score": new_score})

    except Exception as e:
        print(f"Error updating {team} score: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


#---------------------------------------------------Strikes-------------------------------------------------------------

current_strikes = 0

def add_tuah_the_strikes():
    global current_strikes
    with open("strikes.txt", "w", encoding="utf-8") as strikes_file:
        print("-----------------------------------------Incrementing Strikes-----------------------------------------")
        current_strikes += 1
        strikes_file.write(f"{current_strikes}")

def sub_from_the_strikes():
    global current_strikes
    with open("strikes.txt", "w", encoding="utf-8") as strikes_file:
        print("-----------------------------------------Decrementing Strikes-----------------------------------------")
        current_strikes -= 1
        strikes_file.write(f"{current_strikes}")

def reset_uh_the_strikes():
    global current_strikes
    with open("strikes.txt", "w", encoding="utf-8") as strikes_file:
        print("-------------------------------------------Resetting Strikes-------------------------------------------")
        current_strikes = 0
        strikes_file.write("0")

#to update the strikes with a max of 3, by clicking on the strikes text element
@app.route("/add-strike")
def add_strike_plz():
    if deb:
        print("----------------------------------------------/add-strike----------------------------------------------")
    add_tuah_the_strikes()
    return jsonify({"status": "success"})

@app.route("/subtract-strike")
def subtract_a_strike_plz():
    if deb:
        print("--------------------------------------------/subtract-strike--------------------------------------------")
    sub_from_the_strikes()
    return jsonify({"status": "success"})

@app.route("/reset-strikes")
def reset_strikes():
    if deb:
        print("---------------------------------------------/reset-strikes---------------------------------------------")
    reset_uh_the_strikes()
    return jsonify({"status": "success"})


#---------------------------------------------------Flipping Tiles Stuff------------------------------------------------

flipped_states = {i: False for i in range(1, 10)}  # Track flipped state for each number


@app.route("/flip/<int:number>", methods=["POST"])
def flip_thingy(number):
    if deb:
        print(f"--------------------------------------------/flip/{number}--------------------------------------------")

    """Toggles a specific board item based on the number."""
    data = request.json
    current_state = flipped_states.get(number, False)  # Get current state (default to False)
    new_flip_state = data.get("flip_state", not flipped_states.get(number, False))  # Default to toggling

    # Play sound **only when flipping to reveal the answer (True)**
    if not current_state and new_flip_state:
        play_sound_thread("correct")

    flipped_states[number] = new_flip_state  # Set flip state based on request

    # Retrieve the correct answer for this tile
    questions, _, _, _ = load_questions()
    question_list = list(questions.keys())
    current_question_text = question_list[current_question - 1]  # Get current question
    answers = questions[current_question_text]  # Get answers

    if 1 <= number <= len(answers):
        answer_text = answers[number - 1]["text"]  # Get answer text
    else:
        answer_text = "Unknown"  # Fallback

    # Emit update event to frontend **and** backend
    socketio.emit("flip_update", {
        "tile": number,
        "flipped": flipped_states[number],
        "answer": answer_text
    })

    return jsonify({"status": "success", "flipped_states": flipped_states})


@app.route("/flip/update", methods=["GET"])
def get_latest_flip():
    # if deb:
    #     print(f"---------------------------------------------/flip/update---------------------------------------------")
    """Returns the current flipped states of all items."""
    return jsonify({"flipped_states": flipped_states})


#---------------------------------------------------Questions Stuff-----------------------------------------------------

def load_questions():
    """Reads the questions and answers from the JSON file."""
    # if deb:
    #     print(f"------------------------------------------load questions def------------------------------------------")
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            questions = json.load(file)  # Load JSON data
    except Exception as e:
        print(f"Error loading questions: {e}")
        return {}, 0, 0, 0  # Return empty data if an error occurs

    try:
        with open("boys_score.txt", "r", encoding="utf-8") as boys_file:
            boys_score = int(boys_file.read().strip())
        with open("girls_score.txt", "r", encoding="utf-8") as girls_file:
            girls_score = int(girls_file.read().strip())
        with open("strikes.txt", "r", encoding="utf-8") as strikes_file:
            strikes = int(strikes_file.read().strip())
    except Exception as e:
        print(f"Error loading scores: {e}")
        boys_score, girls_score, strikes = 0, 0, 0  # Default values

    return questions, boys_score, girls_score, strikes

@app.route("/question/<int:num>", methods=["GET"])
def get_question(num):
    if deb:
        print(f"-------------------------------------------/question/{num}-------------------------------------------")
    """Returns a specific question, answers, and game status (scores & strikes)."""
    questions, boys_score, girls_score, strikes = load_questions()

    question_list = list(questions.keys())  # Get list of question texts

    if 1 <= num <= len(question_list):
        question_text = question_list[num - 1]  # Get the question by index
        return jsonify({
            "question": question_text,
            "answers": questions[question_text],  # Get answers from JSON
            "boys_score": boys_score,
            "girls_score": girls_score,
            "strikes": strikes
        })
    else:
        if deb:
            play_sound_thread("broke")
        return jsonify({"error": "Invalid question number"}), 400

def get_question_for_tts(num):
    if deb:
        print(f"-------------------------------------------get question {num} for tts-------------------------------------------")
    """Returns a specific question, answers, and game status (scores & strikes)."""
    questions, boys_score, girls_score, strikes = load_questions()

    question_list = list(questions.keys())  # Get list of question texts

    if 1 <= num <= len(question_list):
        question_text = question_list[num - 1]  # Get the question by index
        return jsonify({
            "question": question_text,
        })
    else:
        if deb:
            play_sound_thread("broke")
        return jsonify({"error": "Invalid question number"}), 400


current_question = 1
@app.route("/next-question-plz-bro")
def next_question_plz_bro():
    global current_question, flipped_states

    if current_question >= 12:
        current_question = 11
        return

    if 9 > current_question > 0:
        current_question=9

    if deb:
        print("-----------------------------------------/next question plz bro-----------------------------------------")
        play_sound_thread("add-one-to-q-num")

    current_question +=1

    if deb: #to give time for the sound effect to play before next thing
        time.sleep(3.1)

    if current_question <= 11:
        play_we_asked()

    #reset flipped states
    flipped_states = {i: False for i in range(1, 10)}

    # Notify frontend to reset flips
    socketio.emit("reset_flips")

    return jsonify({"status": "success", "flipped_states_reset": True})

@app.route("/wait-no-go-back-bro")
def last_question_plz_bro():
    global current_question, flipped_states
    if deb:
        print("------------------------------------------/wait no go back bro------------------------------------------")
        play_sound_thread("sub-one-from-q-num")
    current_question -=1
    # reset flipped states
    flipped_states = {i: False for i in range(1, 10)}
    return jsonify({"status": "success",})

#-------------------------------------------Update All The Things-------------------------------------------------------

@app.route("/update-all-the-things")
def update_all_the_things():
    # if deb:
    #     print("-----------------------------------------/update-all-the-things-----------------------------------------")

    questions, boys_score, girls_score, strikes = load_questions()

    question_list = list(questions.keys())  # Get list of question texts

    if 1 <= current_question <= len(question_list):
        question_text = question_list[current_question - 1]  # Get the question by index

        return jsonify({
            "question": question_text,
            "answers": questions[question_text],  # Get answers from JSON
            "boys_score": boys_score,
            "girls_score": girls_score,
            "strikes": strikes
        })
    else:
        if deb:
            play_sound_thread("broke")
        return jsonify({"error": "Invalid question number"}), 400


#---------------------------------------------------Sites---------------------------------------------------------------

@app.route("/")
def index():
    # if deb:
    #     print("---------------------------------------------------/---------------------------------------------------")
    return render_template("display.html")

@app.route(f"/backend")
def backend_site():
    # if deb:
    #    print("------------------------------------------------/backend------------------------------------------------")
    return render_template("backend.html")

@app.route(f"/backend-answers")
def backend_answers_site():
    # if deb:
    #    print("------------------------------------------------/backend------------------------------------------------")
    return render_template("backend_answers.html")

@app.route("/buzzer")
def buzzer_site():
    # if deb:
    #     print("------------------------------------------------/buzzer------------------------------------------------")
    return render_template("buzzer.html")


#---------------------------------------------------Running Stuff-------------------------------------------------------

def start_flask():
    if deb:
        print("----------------------------------------------start_flask----------------------------------------------")
        print("this time with socket io")
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", port_poggies)), app)

def on_y():
    global deb
    if deb:
        print("----------------------------------------pressed y, changing deb----------------------------------------")
    if deb:
        print(f"setting deb to false bc its {deb} atm")
        deb = False
        print(f"deb now: {deb}")
    else:
        print(f"setting deb to true bc its {deb} atm")
        deb = True
        print(f"deb now: {deb}")

def on_u():
    global toggle_sounds
    if deb:
        print("---------------------------------------pressed u, toggling sounds---------------------------------------")
    if toggle_sounds:
        if deb:
            print(f"----------------------toggle sounds currently {toggle_sounds} making it false----------------------")
        toggle_sounds = False
        if deb:
            print(f"---------------------------------toggle sounds now {toggle_sounds}---------------------------------")
    else:
        if deb:
            print(f"-----------------------toggle sounds currently {toggle_sounds} making it true-----------------------")
        toggle_sounds = True
        if deb:
            print(f"---------------------------------toggle sounds now {toggle_sounds}---------------------------------")


def main():
    try:
        if deb:
            print("-------------------------------------------------main-----------------------------------------------")
        """Main function to run the game board."""
        global buzzer_playable

        if deb:
            play_sound_thread("run")

        # Start Flask server in a separate thread
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        print("Starting Flask server...")
        flask_thread.start()

        keyboard.add_hotkey('ctrl + t', on_t)
        keyboard.add_hotkey('ctrl + y', on_y)
        keyboard.add_hotkey('ctrl + u', on_u)

        while True:
            update_buzzer_status()
            if player_buzzed is not None and toggle_sounds and buzzer_playable:
                if deb:
                    print("--------player not buzzed and toggle sounds true and buzzer playable true, playing buzz--------")
                play_sound_thread("buzz")
                buzzer_playable = False

    except KeyboardInterrupt:
        if deb:
            play_sound_thread("stop")
            time.sleep(2)
        print("\nCtrl+C detected! Exiting program...")
    finally:
        print("Cleaning up resources if necessary.")
        exit(0)

if __name__ == "__main__":
    if deb:
        print("------------------------------------------------running------------------------------------------------")
    main()