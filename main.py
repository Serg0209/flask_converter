from flask import Flask, render_template
import os.path
import requests

app = Flask(__name__, template_folder='template')


def converter_rates(currency_type):
    response = requests.get('https://api.exchangeratesapi.io/latest')
    response_json = response.json()
    rates = response_json['rates'][currency_type]
    return float(rates)


def converter_result(amount, convert_rates, currency_by):
    result = round(amount * convert_rates, 2)
    data_to_file = '{},{},{},{}'.format(currency_by, convert_rates, amount, result)
    write_to_file('history', data_to_file)
    return f'Result: <b>{result}</b>'


def write_to_file(name_file, data):
    with open(name_file, 'a') as file:
        file.write('{}\n'.format(data))


@app.route('/')
def index():
    return 'Converter with Euro'


@app.route('/eur_to_usd/<float:amount>')
@app.route('/eur_to_usd/<int:amount>')
def eur_to_usd(amount):
    currency_by = 'USD'
    convert_rates = converter_rates(currency_by)
    return converter_result(amount, convert_rates, currency_by)


@app.route('/eur_to_gbp/<float:amount>')
@app.route('/eur_to_gbp/<int:amount>')
def eur_to_gbp(amount):
    currency_by = 'GBP'
    convert_rates = converter_rates(currency_by)
    return converter_result(amount, convert_rates, currency_by)


@app.route('/eur_to_php/<float:amount>')
@app.route('/eur_to_php/<int:amount>')
def eur_to_php(amount):
    currency_by = 'PHP'
    convert_rates = converter_rates(currency_by)
    return converter_result(amount, convert_rates, currency_by)


@app.route('/history/')
def show_file_history():
    name_file = 'history'
    if os.path.isfile(name_file) is False:
        return f'File not found!'
    if os.path.isfile(name_file) is True:
        with open(name_file, "r") as file:
            content = file.readlines()
            return render_template('history.html', content=content)


if __name__ == '__main__':
    app.run()
