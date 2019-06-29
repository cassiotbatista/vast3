from bokeh.layouts import widgetbox, layout, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Div, Button, RadioButtonGroup, Select, Slider
from bokeh.events import ButtonClick
import io
import base64
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, WheelZoomTool

file_source = ColumnDataSource({'file_contents':[], 'file_name':[]})
data = {}

def file_callback():
    layout = curdoc().get_model_by_name('mainLayout')
#    raw_contents = file_source.data['file_contents'][0]
#    name = file_source.data['file_name'][0]
#    prefix, b64_contents = raw_contents.split(",", 1)
#    file_contents = base64.b64decode(b64_contents)
#    file_io = io.BytesIO(file_contents)
    curdoc().title = "File Uploading....."
    layout.children.pop()
    layout.children.append(notification)
#    if name.endswith('.csv'):
#        df = pd.read_csv(file_io, delimiter="\t")
#        df.to_csv('%s'%name, index=False)
#        print("csv downloaded successfully")
#    else:
#        df = pd.read_excel(file_io)
#        df.to_excel('%s'%name, index=False)
#        print("excell downloaded successfully")
#    data['df'] = df
#    layout.children.pop()
#    layout.children.append(f)
#    curdoc().title = "Word Count"    
#
## file_source.on_change('data', file_callback)

## create widgets
#button_1 = Button(label="Browse...", button_type="success")
#upload = Button(label="Upload File", button_type="success")
#button_1.js_on_click(CustomJS(args=dict(file_source=file_source), code = """
#function read_file(filename) {
#    var reader = new FileReader();
#    reader.onload = load_handler;
#    reader.onerror = error_handler;
#    // readAsDataURL represents the file's data as a base64 encoded string
#    reader.readAsDataURL(filename);
#}
#
#function load_handler(event) {
#    var b64string = event.target.result;
#    file_source.data = {'file_contents' : [b64string], 'file_name':[input.files[0].name]};
#    file_source.change.emit();
#}
#
#function error_handler(evt) {
#    if(evt.target.error.name == "NotReadableError") {
#        alert("Can't read file!");
#    }
#}
#
#var input = document.createElement('input');
#input.setAttribute('type', 'file');
#input.onchange = function(){
#    if (input.files[0].name.endsWith(".xlsx") || input.files[0].name.endsWith(".csv")) {
#        console.log(input.files)
#        read_file(input.files[0]);
#    } else {
#        alert('Please Upload CSV or Excel file');
#    }
#}
#input.click();
#"""))
#
#upload.on_click(file_callback)
button_2 = Button(label="Plot")
button_2.on_click(file_callback)

# put the results in a row
box = widgetbox(button_2, width=300)
notification = Div(text="""<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0" width="550px" height="500px" viewBox="-430 -430 1000 1000" xml:space="preserve"><g xmlns="http://www.w3.org/2000/svg"><path fill="#000000" d="M109.25 55.5h-36l12-12a29.54 29.54 0 0 0-49.53 12H18.75A46.04 46.04 0 0 1 96.9 31.84l12.35-12.34v36zm-90.5 17h36l-12 12a29.54 29.54 0 0 0 49.53-12h16.97A46.04 46.04 0 0 1 31.1 96.16L18.74 108.5v-36z"/><animateTransform attributeName="transform" type="rotate" from="0 64 64" to="360 64 64" dur="720ms" repeatCount="indefinite"/></g></svg>""",width=550,height=500) # display Processing...
f = figure(x_range = [], plot_height=250, title="Some Plot", toolbar_location=None, tools="",name = 'plot')
f.vbar([], top=[], width=0.9, color=Spectral6)
f.y_range.start = 0
f.tools = [PanTool(),ResetTool()]
f.toolbar_location = 'above'
f.plot_width=800
f.plot_height=500

lay = row(box, f, width=800,name='mainLayout')

curdoc().add_root(lay)
curdoc().title = "Word Count"
