from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

tasks = []

@app.route('/')
def health():
    return "OK", 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', '')
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def mark_task_done(id):
    task = next((t for t in tasks if t['id'] == id), None)
    if task:
        task['done'] = True
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/metrics')
def metrics_endpoint():
    return metrics.generate_latest()

@app.route('/error')
def error():
    return 1 / 0  # Division par zéro pour simuler une panne

if __name__ == '__main__':
    app.run(debug=True)
