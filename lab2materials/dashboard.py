import base64
import os
import io
import pandas as pd
from urllib.parse import quote as urlquote
import plotly.graph_objs as go
from flask import Flask, send_from_directory
import dash
import heapq
from scipy.signal import find_peaks
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from get_data import get_freq_and_amp

UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.Div([
        html.H1("Upload a file for plotting")

        ],style={"color":"gray", "textAlign": "center","font-size": "20px",}),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                "color":"white",
                "font-family": "Times New Roman, Times, serif",
                "font-size": "20px",
                "background-color":"coral",
            },
            multiple=True,
        ),

        html.Div([
        html.H2("File List")

        ],style={"color":"gray"}),
        html.Div([
                    dcc.Checklist(
                options=[
                    {'label': 'BPFO', 'value': 'BPFO'},
                    {'label': 'BPFI', 'value': 'BPFI'},
                    {'label': 'BSF', 'value': 'BSF'},
                    {'label': 'STF', 'value': 'STF'},
                ],
                value=['MTL', 'SF'],
                labelStyle={'display': 'inline-block'}
            )

        ],style={"textAlign": "center","color":"gray"}),

        html.Ul(id="file-list"),
        html.Div([
        dcc.Graph(
        id="freq-plot"
        )
        ])
    ],
    style={"max-width": "1500px"},


)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def get_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    content_type, content_string = contents.split(',')
    return content_string


def get_data_from_file(file_name):
    df = pd.read_csv(file_name)
    freq = df["frequency"].values
    amp = df["amplitude"].values
    return freq, amp


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    dash.dependencies.Output('freq-plot', 'figure'),
    [dash.dependencies.Input('upload-data', 'filename'),Input("upload-data", "contents")]
    )


###############################################################################
# This is the function you need to update
###############################################################################
def update_freq(uploaded_filenames,contents):
    if contents is not None:
        _,content_string = contents[0].split(",")
        table  = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        # call your functions bellow this line
        frequency, amplitude = [], []
        x_label, y_label = " ", " "
        figure = {
            "data": [{
                    "x": frequency, # add frequency here
                    "y": amplitude, # add amplitude here
                    'type': 'line',
                }],
            "layout":go.Layout(
            xaxis={ 'title': x_label}, # add xlabel
            yaxis={'title': y_label}, # add ylabel
        )
        }
        return figure
    else:
        return {}
################################################################################
################################################################################






@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

#
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
