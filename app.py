from flask import Flask, render_template, request, flash
import pandas as pd
import io
import requests

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def apply_symbol(symbol, text):
    """
    선택한 색상 기호를 문자열에 적용하여 반환합니다.
    """
    symbol_dict = {"@": f"@{text}@", "#": f"#{text}#", "&": f"&{text}&", "$": f"${text}$"}
    return symbol_dict.get(symbol, text)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 구글 시트에서 도시 좌표 가져오기
        sheet_id = '1Nw8tCyNPqVXhvvjPEwDCbjf0mCqgXrzpshDYxUNTXd4'
        sheet_name = 'city'
        city_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        cities = {}
        response = requests.get(city_url)
        content = response.content.decode('utf-8')
        csv_file = io.StringIO(content)
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            city_name = row['도시명']
            coordinates = row['좌표']
            cities[city_name] = coordinates

        date_choice = request.form['date']
        time_choice = request.form['time']
        datetime_choice = f"{date_choice} {time_choice}"
        start_city = request.form['start_city']
        end_city = request.form['end_city']
        participants = request.form['participants']
        objective = request.form['objective']

        datetime_choice = apply_symbol(request.form['time_symbol'], datetime_choice)
        start_city_text = apply_symbol(request.form['location_symbol'], f"{start_city} 좌표 {cities.get(start_city, '')}")
        end_city_text = apply_symbol(request.form['relocation_symbol'], f"{end_city} 좌표 {cities.get(end_city, '')}")
        participants = apply_symbol(request.form['participation_symbol'], participants)
        objective = apply_symbol(request.form['objective_symbol'], objective)

        letter = f"""공성 안내

시간: {datetime_choice}

위치: {start_city_text}

재배치:  {end_city_text}

참여: {participants}

목적: {objective}

중요한 공성입니다. 맹우 여러분들의 많은 참여 부탁드립니다."""

        flash('서신이 생성되었습니다.')
        return render_template('result.html', letter=letter)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
