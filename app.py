# from flask import Flask, render_template, request, redirect
import flask
import quandl
from bokeh import plotting as plt
from bokeh import models as mdl
from bokeh import resources
from bokeh import embed

app = flask.Flask(__name__)
app.vars = {}
color_list = ["blue", "red", "green", "purple"]


def quandl_init(ticker):
    quandl.ApiConfig.api_key = "zzoURudWbRHgR_SEH_gj"

    quandl_cols = ["ticker", "date", "open", "close", "adj_open", "adj_close"]
    data = quandl.get_table(
        "WIKI/PRICES",
        qopts={"columns": quandl_cols},
        date={"gte": "2018-01-01", "lte": "2018-02-01"},
        ticker=ticker,
    )
    return data


def bokeh_plot(data, ticker):
    plot = plt.figure(
        plot_width=400, plot_height=400, x_axis_type="datetime", title=ticker
    )
    plot.background_fill_color = "beige"
    plot.background_fill_alpha = 0.5

    dates = data["date"]
    open_price = data["open"]
    close_price = data["close"]
    for i, feature in enumerate(app.vars["features"]):
        plot.line(
            dates,
            data[feature],
            legend=feature,
            alpha=0.5,
            line_width=2,
            line_color=color_list[i],
        )
    plot.toolbar.autohide = True

    plot.yaxis.axis_label = "Price"
    plot.xaxis.axis_label = "Date"
    plot.legend.location = "bottom_right"

    return plot


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        print("what")
        return flask.render_template("index.html")
    else:
        app.vars["features"] = flask.request.form.getlist("features")

        app.vars["ticker"] = flask.request.form["ticker"]
        app.vars["data"] = quandl_init(app.vars["ticker"])
        print(app.vars["features"])
        return flask.redirect("/plot")


@app.route("/plot", methods=["GET"])
def plot_page():
    plot = bokeh_plot(app.vars["data"], app.vars["ticker"])

    js_resources = resources.INLINE.render_js()
    css_resources = resources.INLINE.render_css()
    script, div = embed.components(plot)
    return flask.render_template(
        "plot.html",
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )


@app.route("/about")
def about():
    return flask.render_template("about.html")


def main():
    # ticker = "GOOG"
    # data = quandl_init(ticker)
    # bokeh_plot(data, ticker)
    app.run(port=33507)


if __name__ == "__main__":
    main()
