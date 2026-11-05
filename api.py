from flask import Flask, jsonify, request
app = Flask(__name__)
events = [
    {"id": 1, "title": "Quizaften", "date": "2026-11-13", "capacity": 3, "participants": ["Anna", "Bo"]},
    {"id": 2, "title": "Brætspilsaften", "date": "2026-11-20", "capacity": 5, "participants": []},
    {"id": 3, "title": "Beerpong", "date": "2026-11-27", "capacity": 4, "participants": ["Sara"]}
]

@app.get("/events")
def get_events():
    return jsonify(events), 200

@app.get("/events/<int:event_id>")
def get_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return jsonify(event), 200
    return jsonify({"error": "Eventet findes ikke"}), 404

@app.post("/events")
def create_event():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    date = data.get("date")
    capacity = data.get("capacity")

    if not title or not date or type(capacity) is not int or capacity <= 0:
        return jsonify({"error": "Ugyldig titel, dato eller antal pladser"}), 400

    new_event = {
        "id": max(event["id"] for event in events) + 1 if events else 1,
        "title": title,
        "date": date,
        "capacity": capacity,
        "participants": []
    }

    events.append(new_event)
    return jsonify(new_event), 201

@app.post("/events/<int:event_id>/signups")
def signup(event_id):
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict): return jsonify({"error": "Send et JSON-objekt med et navn"}), 400
    
    name = data.get("name")

    if not name:
        return jsonify({"error": "Du skal skrive et navn"}), 400

    for event in events:
        if event["id"] == event_id:

            if name in event["participants"]:
                return jsonify({"error": "Personen er allerede tilmeldt"}), 409

            if len(event["participants"]) >= event["capacity"]:
                return jsonify({"error": "Eventet er fuldt"}), 409

            event["participants"].append(name)
            return jsonify(event), 201

    return jsonify({"error": "Eventet findes ikke"}), 404

@app.delete("/events/<int:event_id>/signups/<name>")
def cancel_signup(event_id, name):
    for event in events:
        if event["id"] == event_id:
            if name not in event["participants"]:
                return jsonify({"error": "Tilmeldingen findes ikke"}), 404

            event["participants"].remove(name)
            return "", 204

    return jsonify({"error": "Eventet findes ikke"}), 404

@app.delete("/events/<int:event_id>")
def delete_event(event_id):
    for event in events:
        if event["id"] == event_id:
            events.remove(event)
            return "", 204
    return jsonify({"error": "Eventet findes ikke"}), 404

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5001, debug=True)
