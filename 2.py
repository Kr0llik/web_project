from flask import Flask, url_for, request, render_template

app = Flask(__name__)


def main():
    app.run()


@app.route('/')
def start():
    return render_template('tst.html', title='Ae')


if __name__ == '__main__':
    main()
