from flask import request, redirect, send_from_directory
import controller

def create_route(app):

    @app.route("/json", methods=["GET","POST"])
    def json():
        if "data" in request.args:
            d = request.args.get("data")
            if d in ["user","item","category","dept"]:
                return controller.get_json(d)
        return("GETパラメータを指定してください")
