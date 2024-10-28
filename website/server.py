from flask import Flask, render_template

app = Flask(__name__)

@app.route('/player_count')
def player_count():
    with open('/home/players.txt', 'r') as file:
        content = file.read()
    return render_template('player_count.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
