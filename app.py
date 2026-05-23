from flask import Flask, render_template, request
import pickle

# LOAD MODEL

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# LOAD ACCURACY

with open("accuracy.txt", "r") as f:
    model_accuracy = f.read()

# CREATE FLASK APP

app = Flask(__name__)

# HISTORY STORAGE

history = []

# HOME PAGE

@app.route("/")
def login():
    return render_template("login.html")


# MAIN PAGE

@app.route("/home", methods=["POST"])
def home():
    return render_template(
        "index.html",
        accuracy=model_accuracy + "%",
        history=history
    )


# PREDICTION

@app.route("/predict", methods=["POST"])
def predict():

    text = request.form["text"]

    text_lower = text.lower()

    # POSITIVE WORDS

    positive_words = [

        "good",
        "nice",
        "beautiful",
        "happy",
        "great",
        "awesome",
        "amazing",
        "excellent",
        "fantastic",
        "wonderful",
        "cool",
        "best",
        "brilliant",
        "smart",
        "kind",
        "helpful",
        "sweet",
        "love",
        "lovely",
        "friend",
        "friends",
        "hello",
        "hi",
        "hey",
        "morning",
        "evening",
        "birthday",
        "congratulations",
        "congrats",
        "thank you",
        "thanks",
        "welcome",
        "peace",
        "respect",
        "success",
        "winner",
        "enjoy",
        "fun",
        "positive",
        "perfect",
        "beautiful day",
        "have a nice day",
        "good job",
        "well done"

    ]

    # NEGATIVE WORDS

    negative_words = [

        "stupid",
        "idiot",
        "hate",
        "loser",
        "ugly",
        "dumb",
        "fool",
        "moron",
        "nonsense",
        "crazy",
        "mad",
        "useless",
        "worst",
        "trash",
        "garbage",
        "annoying",
        "disgusting",
        "pathetic",
        "shut up",
        "kill",
        "die",
        "kill yourself",
        "bastard",
        "jerk",
        "fake",
        "cheater",
        "noob",
        "bot",
        "terrorist",
        "psycho",
        "criminal",
        "bully",
        "abuse",
        "abusive",
        "racist",
        "ugliest",
        "failure",
        "weak",
        "worthless",
        "crybaby",
        "nobody likes you",
        "go away",
        "stupid fellow",
        "dirty",
        "bad person",
        "evil"

    ]

    # POSITIVE CHECK

    for word in positive_words:

        if word in text_lower:

            result = "No Cyberbullying Detected ✅"

            history.append((text, result))

            return render_template(
                "index.html",
                prediction_text=result,
                history=history,
                accuracy=model_accuracy + "%"
            )

    # NEGATIVE CHECK

    for word in negative_words:

        if word in text_lower:

            result = "Cyberbullying Detected 🚨"

            history.append((text, result))

            return render_template(
                "index.html",
                prediction_text=result,
                history=history,
                accuracy=model_accuracy + "%"
            )

    # ML PREDICTION

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    if int(prediction) == 1:
        result = "Cyberbullying Detected 🚨"

    else:
        result = "No Cyberbullying Detected ✅"

    history.append((text, result))

    return render_template(
        "index.html",
        prediction_text=result,
        history=history,
        accuracy=model_accuracy + "%"
    )


# RUN APP

if __name__ == "__main__":
    app.run(debug=True)