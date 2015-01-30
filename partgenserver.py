from flask import Flask
from flask import render_template
from flask import request,session
from flask import make_response
import traceback
import StringIO
import gen_part
from werkzeug.routing import BaseConverter

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html',parts=gen_part)


@app.route("/jquery.js")
def jquery():
    return app.send_static_file('jquery-2.1.0.min.js')


@app.route("/jsfunc.js")
def jsfunc():
    return render_template('jsfunc.js',parts=gen_part)


@app.route(r'/preview.svg',methods=["GET"])
def get_preview():
    try:

        options=dict()
        for key in request.args.keys():
            options[key]=request.args[key]

        if 'partname' in options:
            options.pop('partname')
        options.pop('package')
        raw=gen_part.make_part_preview(
            package=request.args['package'],
            options=options)
            

        resp = make_response(raw)

        resp.content_type = "image/svg+xml"
        resp.headers.add('Cache-Control', 'no-cache')

        return resp
    except Exception,exh:
        print "Exception:",exh
        print traceback.format_exc()
        raise
        


@app.route(r'/<partname>.fzpz',methods=["POST","GET"])
def get_image(partname):
    try:
        print request.form

        io=StringIO.StringIO()

        options=dict()
        for key in request.form.keys():
            options[key]=request.form[key]
        options.pop('package')
        options.pop('partname')
        
        
        gen_part.make_part(
            partfilename=io,
            partname=partname,
            version=1,
            package=request.form['package'],
            options=options)
        raw=io.getvalue()

        resp = make_response(raw)



        resp.content_type = "application/binary"
        resp.headers.add('Cache-Control', 'no-cache')

        return resp
    except Exception,exh:
        print "Exception:",exh
        print traceback.format_exc()
        raise
        
if __name__ == '__main__':
    #app.debug=True
    app.run(host="0.0.0.0",port=8011)

