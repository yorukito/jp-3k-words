# JP 3K Words - Kanji Guessing Game

Este é um projeto Flask para praticar kanji e vocabulário japonês de forma interativa.

## Como usar

1. **Clone o repositório:**
   ```
   git clone https://github.com/yorukito/jp-3k-words.git
   cd jp-3k-words
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```
   python -m venv env
   # Ative o ambiente:
   # Windows:
   env\Scripts\activate
   # Linux/Mac:
   source env/bin/activate
   ```

3. **Instale as dependências:**
   ```
   pip install flask
   ```

4. **Execute o servidor Flask:**
   ```
   python jp_app.py
   ```

5. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

## Funcionalidades

- Pratique a pronúncia de kanjis de diferentes semanas e dias.
- Feedback instantâneo para respostas corretas ou incorretas.
- Interface web simples e responsiva.

## Estrutura

- `jp_app.py` — Código principal Flask.
- `templates/` — Templates HTML (base, seleção, jogo).
- `static/css/main.css` — Estilos visuais do site.

## Personalização

- Adicione mais kanjis, pronúncias e significados em `jp_app.py` no dicionário `kanji_data`.

## Licença

MIT