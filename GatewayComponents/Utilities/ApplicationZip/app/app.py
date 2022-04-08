from flask import Flask, render_template, request
import platform_utility as pf


app = Flask(__name__)


@app.route("/")
def fun():
    prec = pf.getsensordata(1)

    max_temp = pf.getsensordata(2)
    min_temp = pf.getsensordata(3)
    wind = pf.getsensordata(4)
    data = {
        "arg1":prec,
        "arg2":max_temp,
        "arg3":min_temp,
        "arg4":wind
    }
    res = pf.getmodeldata(1,data)

    # prec = 0.2
    # max_temp = 0.3
    # min_temp = 0.5
    # wind = 0.6

    # res = 90

    fres = interpret(res)
    return render_template("./index.html", context={'prec': prec, 'max_temp': max_temp, 'min_temp': min_temp, 'wind': wind, 'res': res})


def interpret(res):
    if res == 0:
        return "Drizzle"
    elif res == 1:
        return "Fog"
    elif res == 2:
        return "Rain"
    elif res == 3:
        return "snow"
    else:
        return "Sun"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

