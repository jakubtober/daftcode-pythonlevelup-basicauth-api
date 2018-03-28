from flask import Flask, request, make_response, redirect, render_template, session, jsonify, json

app = Flask(__name__)
app.secret_key = 'pracadomowasesjeirybki'

username = 'Akwarysta69'
password = 'J3si07r'

user_login = ''
user_password = ''


fishes = {
    1: {
        "who": "Znajomy",
        "where": {
            "lat": 0.001,
            "long": 0.002
        },
        "mass": 34.56,
        "length": 23.67,
        "kind": "szczupak"
    },
    2: {
        "who": "Kolega kolegi",
        "where": {
            "lat": 34.001,
            "long": 52.002
        },
        "mass": 300.12,
        "length": 234.56,
        "kind": "sum olimpijczyk"
    }
}


def get_user_data():
    authorization_data = request.authorization

    global user_login
    user_login = authorization_data['username']

    global user_password
    user_password = authorization_data['password']


def is_password_and_login_correct(login_to_check, password_to_check):
    return login_to_check == username and password_to_check == password



@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return 'Homepage'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'Login page'

    elif request.method == 'POST':
        get_user_data()

        if username in session.values():
            return redirect('/hello')
        else:
            if is_password_and_login_correct(user_login, user_password):
                session['username'] = user_login
                return redirect('/hello')
            else:
                return '403', 403


@app.route('/logout', methods=['POST'])
def logout():
    if username in session.values():
        session.pop('username')
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/hello', methods=['GET'])
def hello():
    if username in session.values():
        return render_template('hello.html', username = session['username'])
    else:
        return redirect('/login')


@app.route('/fishes', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def fishes_details():
    if username in session.values():
        if request.method == 'GET':
            return jsonify(fishes)

        elif request.method =='POST':
            data = request.get_json()
            keys = list(fishes.keys())
            new_fish_id = len(keys) + 1


            new_fish = {
                "who": data.get("who"),
                "where": {
                    "lat": data.get('where').get('lat'),
                    "long": data.get('where').get('long'),
                },
                "mass": data.get("mass"),
                "lenght": data.get("length"),
                "kind": data.get("kind"),
            }

            fishes[new_fish_id] = new_fish

            return redirect('/fishes/{}'.format(new_fish_id))
    else:
        return redirect('/login{}?format=json'.format(new_fish_id))


@app.route('/fishes/<fish_id>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def fish_details(fish_id):
    if username in session.values():
        if request.method == 'GET':
            fish = fishes.get(int(fish_id))
            return jsonify(fish)

        elif request.method == 'DELETE':
            fishes.pop(int(fish_id), None)
            return 'Rybka usunięta!'

        elif request.method == 'PUT':
            data = request.get_json()

            new_fish = {
                "who": data.get("who"),
                "where": {
                    "lat": data.get('where').get('lat'),
                    "long": data.get('where').get('long'),
                },
                "mass": data.get("mass"),
                "lenght": data.get("length"),
                "kind": data.get("kind"),
            }

            fishes[int(fish_id)] = new_fish
            return 'Rybka podmieniona!'

        elif request.method == 'PATCH':
            data = request.get_json()
            all_keys = list(data.keys())

            for key in all_keys:
                if key == 'where':
                    fishes[int(fish_id)]['where'] = data.get('where')
                else:
                    fishes[int(fish_id)][key] = data.get(key)

            return 'Rybka zaktualizowana!'


if __name__ == '__main__':
    app.run(debug=True)

