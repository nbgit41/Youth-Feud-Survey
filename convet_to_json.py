import json


def convert_to_json(input_filename="Formatted_Answers.txt", output_filename="questions.json"):
    """Reads the formatted text file and saves the data as a JSON file."""
    questions = {}
    current_question = None

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Detect question lines
                if line.startswith("Question"):
                    if ": " in line:
                        current_question = line.split(": ", 1)[1]
                        questions[current_question] = []
                    else:
                        print(f"ERROR: Malformed Question Line -> {repr(line)}")
                        continue

                # Detect answer lines
                elif current_question:
                    answer_entries = line.split(",")  # Split by commas
                    for entry in answer_entries:
                        parts = entry.strip().rsplit(";", 1)  # Split at last ';'
                        if len(parts) == 2:
                            answer, points = parts
                            answer = answer.strip()
                            points = points.strip()

                            if points.isdigit():
                                questions[current_question].append({
                                    "text": answer,
                                    "points": int(points)
                                })
                            else:
                                print(f"ERROR: Invalid points value -> {repr(parts)}")
                        else:
                            print(f"ERROR: Malformed answer entry -> {repr(entry)}")

        # Save to JSON file
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(questions, json_file, indent=4)
        print(f"Successfully saved questions to {output_filename}")

    except Exception as e:
        print(f"Error converting to JSON: {e}")


# Run the conversion
if __name__ == "__main__":
    convert_to_json()
