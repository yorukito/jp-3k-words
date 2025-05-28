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
            "meaning": ['to go', 'see, look at', 'a lot of, many', 'home, household', 'this, this one', 'that, that one', 'I, me', '	work, job', 'when', 'do, make']
        },
        "2": {
            "kanji": ['出る', '使う', '所', '作る', '思う', '持つ', '買う', '時間', '知る', '同じ'],
            "pronunciation": ['deru', 'tsukau', 'tokoro', 'tsukuru', 'omou', 'motsu', 'kau', 'jikan', 'shiru', 'onaji'],
            "meaning": ['go out, leave', 'use, make use of', 'place', 'make, create', 'think', 'have, possess', 'buy', 'time, hour', 'know', 'same, identical']
        },
        "3": {
            "kanji": ['今', '新しい', 'なる', 'まだ', 'あと', '聞く', '言う', '少ない', '高い', '子供'],
            "pronunciation": ['ima', 'atarashii', 'naru', 'mada', 'ato', 'kiku', 'iu', 'sukunai', 'takai', 'kodomo'],
            "meaning": ['now', 'new', 'become', '(not) yet, still', 'after', 'hear, ask', 'say, tell', 'few, little', 'high, tall', 'child']
        },
        "4": {
            "kanji": ['そう', 'もう', '学生', '熱い', 'どうぞ', '午後', '長い', '本', '今年', 'よく'],
            "pronunciation": ['sou', 'mou', 'gakusei', 'atsui', 'douzo', 'gogo', 'nagai', 'hon', 'kotoshi', 'yoku'],
            "meaning": ['so, that way', 'already, yet', 'student', 'hot (to touch)', 'please', 'afternoon, p.m.', 'long', 'book, volume', 'this year (colloquial)', 'often, well']
        },
        "5": {
            "kanji": ['彼女', 'どう', '言葉', '顔', '終わる', '一つ', 'あげる', 'こう', '学校', 'くれる'],
            "pronunciation": ['kanojo', 'dou', 'kotoba', 'kao', 'owaru', 'hitotsu', 'ageru', 'kou', 'gakkou', 'kureru'],
            "meaning": ['she, one’s girlfriend', 'how, what', 'word, language', 'face', 'finish, end', 'one (thing)', 'give, offer (colloquial)', 'like this, such', 'school', 'be given']
        },
        "6": {
            "kanji": ['始める', '起きる', '春', '午前', '別', 'どこ', '部屋', '若い', '車', '置く'],
            "pronunciation": ['hajimeru', 'okiru', 'haru', 'gozen', 'betsu', 'doko', 'heya', 'wakai', 'kuruma', 'oku'],
            "meaning": ['start (something)', 'get up, get out of bed', 'spring', 'morning, a.m.', 'another, different', 'where', 'room', 'young', 'car, automobile', 'put, place']
        },
        "7": {
            "kanji": ['住む', '働く', '難しい', '先生', '立つ', '呼ぶ', '大学', '安い', 'もっと', '帰る'],
            "pronunciation": ['sumu', 'hataraku', 'muzukashii', 'sensei', 'tatsu', 'yobu', 'daigaku', 'yasui', 'motto', 'kaeru'],
            "meaning": ['live, reside', 'work', 'difficult', 'teacher', 'stand, rise', 'call, name', 'university, college', 'cheap, inexpensive', 'more', 'go back home']
        }
    }
}

# Página inicial: seleção de semana e dia
@app.route('/', methods=['GET', 'POST'])
def select_day():
    # Se o usuário enviar o formulário (POST), verifica se a semana e o dia existem em kanji_data
    if request.method == 'POST':
        week = request.form.get('week')
        day = request.form.get('day')
        # Se semana e dia válidos, salva na sessão e vai para o jogo
        if week in kanji_data and day in kanji_data[week]:
            session['week'] = week
            session['day'] = day
            return redirect(url_for('kanji_game'))
        else:
            # Se inválido, mostra erro
            return render_template('select.html', error="Invalid week or day.", kanji_data=kanji_data)
    # Se GET, só mostra o formulário
    return render_template('select.html', error=None, kanji_data=kanji_data)

# Página do jogo Kanji
@app.route('/kanji', methods=['GET', 'POST'])
def kanji_game():
    # Recupera semana e dia da sessão
    week = session.get('week')
    day = session.get('day')

    # Se não houver semana/dia válidos, volta para seleção
    if not week or not day or week not in kanji_data or day not in kanji_data[week]:
        return redirect(url_for('select_day'))

    # Obtém listas de kanji, pronúncia e significado para o dia/semana escolhidos
    kanji_list = kanji_data[week][day]["kanji"]
    pronunciation_list = kanji_data[week][day]["pronunciation"]
    meaning_list = kanji_data[week][day]["meaning"]

    # Sorteia um índice para o kanji atual, se ainda não existir na sessão
    if 'index' not in session:
        session['index'] = random.randint(0, len(kanji_list) - 1)

    index = session['index']
    kanji = kanji_list[index]
    correct_pronunciation = pronunciation_list[index]
    meaning = meaning_list[index]

    feedback = None  # Mensagem de acerto/erro para mostrar ao usuário

    if request.method == 'POST':
        # Lê a resposta do usuário
        user_input = request.form.get('pronunciation', '').strip().lower()
        # Se o usuário clicar em "Exit", volta para a tela de seleção
        if user_input == 'exit':
            session.pop('index', None)
            return redirect(url_for('select_day'))
        # Se acertou, prepara mensagem de acerto
        elif user_input == correct_pronunciation:
            session['feedback'] = (
                f"<span style='color: #2ecc40; font-weight:bold;'>✅ Correct!</span> 🎉<br>"
                f"Great job!<br>"
                f"The meaning of <span style='color: #2a5298; font-weight:bold;'>{kanji}</span> is "
                f"<span style='color: #2980b9;'>{meaning}</span>."
            )
        # Se errou, prepara mensagem de erro
        else:
            session['feedback'] = (
                f"<span style='color: #e74c3c; font-weight:bold;'>❌ Incorrect.</span><br>"
                f"The correct pronunciation of <span style='color: #2a5298; font-weight:bold;'>{kanji}</span> is "
                f"<span style='color: #f39c12;'>{correct_pronunciation}</span>.<br>"
                f"The meaning is <span style='color: #2980b9;'>{meaning}</span>.<br>"
            )
        # Sorteia novo índice para o próximo desafio
        session['index'] = random.randint(0, len(kanji_list) - 1)
        # Redireciona para GET para evitar reenvio de formulário
        return redirect(url_for('kanji_game'))

    # GET: mostra feedback se existir e limpa depois
    feedback = session.pop('feedback', None)

    # Renderiza a página do jogo com o kanji atual e o feedback (se houver)
    return render_template(
        'kanji.html',
        kanji=kanji,
        feedback=feedback
    )

if __name__ == '__main__':
    app.run(debug=True)
