import random
from flask import Flask, render_template, url_for, request, redirect, session

# Inicialização do Flask
app = Flask(__name__)
app.secret_key = "kanji_secret"

# Dicionário com os dados dos kanjis, pronúncias e significados organizados por semana e dia
kanji_data = {
    "1": {
        "1": {
            "kanji": ['行く', '見る', '多い', '家', 'これ', 'それ', '私', '仕事', 'いつ', 'する'],
            "pronunciation": ['iku', 'miru', 'ooi', 'ie', 'kore', 'sore', 'watashi', 'shigoto', 'itsu', 'suru'],
            "meaning": ['to go', 'to see', 'many', 'house', 'this', 'that', 'I/me', 'work/job', 'when', 'to do']
        }
        # ...adicione mais dias/semanas se quiser...
    }
    # ...adicione mais semanas se quiser...
}

# Rota principal: seleção de semana e dia
@app.route('/', methods=['GET', 'POST'])
def select_day():
    # Se o usuário enviar o formulário (POST), verifica se a semana e o dia existem em kanji_data
    if request.method == 'POST':
        week = request.form.get('week')
        day = request.form.get('day')
        if week in kanji_data and day in kanji_data[week]:
            session['week'] = week
            session['day'] = day
            return redirect(url_for('kanji_game'))
        else:
            # Se inválido, mostra erro
            return render_template('select.html', error="Invalid week or day.", kanji_data=kanji_data)
    # Se GET, só mostra o formulário
    return render_template('select.html', error=None, kanji_data=kanji_data)

# Rota do jogo Kanji
@app.route('/kanji', methods=['GET', 'POST'])
def kanji_game():
    
    week = session.get('week')
    day = session.get('day')
    
    if not week or not day or week not in kanji_data or day not in kanji_data[week]:
        return redirect(url_for('select_day'))

    kanji_list = kanji_data[week][day]["kanji"]
    pronunciation_list = kanji_data[week][day]["pronunciation"]
    meaning_list = kanji_data[week][day]["meaning"]

    # Garante que existe um índice sorteado para o kanji atual do usuário na sessão.
    if 'index' not in session:
        session['index'] = random.randint(0, len(kanji_list) - 1)

    index = session['index']
    kanji = kanji_list[index]
    correct_pronunciation = pronunciation_list[index]
    meaning = meaning_list[index]

    feedback = None

    if request.method == 'POST':
        user_input = request.form.get('pronunciation', '').strip().lower()
        if user_input == 'exit':
            session.pop('index', None)
            return redirect(url_for('select_day'))
        elif user_input == correct_pronunciation:
            session['feedback'] = (
                f"<span style='color: #2ecc40; font-weight:bold;'>✅ Correct!</span> 🎉<br>"
                f"Great job!<br>"
                f"The meaning of <span style='color: #2a5298; font-weight:bold;'>{kanji}</span> is "
                f"<span style='color: #2980b9;'>{meaning}</span>."
            )
        else:
            session['feedback'] = (
                f"<span style='color: #e74c3c; font-weight:bold;'>❌ Incorrect.</span><br>"
                f"The correct pronunciation of <span style='color: #2a5298; font-weight:bold;'>{kanji}</span> is "
                f"<span style='color: #f39c12;'>{correct_pronunciation}</span>.<br>"
                f"The meaning is <span style='color: #2980b9;'>{meaning}</span>.<br>"
            )
        # Sorteie novo índice para o próximo desafio
        session['index'] = random.randint(0, len(kanji_list) - 1)
        return redirect(url_for('kanji_game'))  # Redireciona para GET

    # GET: mostra feedback se existir e limpa depois
    feedback = session.pop('feedback', None)

    return render_template(
        'kanji.html',
        kanji=kanji,
        feedback=feedback
    )

if __name__ == '__main__':
    app.run(debug=True)
