from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
from cube_service import CubeService
from sqlite_helper import SQLiteHelper

@main.route("/context/<int:context>", methods=["get"])
def cube_slice_by_context(context):
    logger.debug("cube slice by context", context)
    cube_slice = cube.cslice("time",[context])
    logger.debug("\n\n\n\n cubeslice:%s" % cube_slice)
    print("\n\n\n\n cubeslice:%s" % cube_slice)
    return json.dumps({"context":context, "slice":cube_slice})
 
@main.route("/context/<int:context>/item/<int:item>", methods=["get"])
def item_in_context(context,item):
    logger.debug("Count of item %s in context %s", (item, context))
    count = dbhelper.item_in_context(item, context)
    return json.dumps({"context":context, "item": item, "count":count})
 
 
def create_app(dataset_path):
    global cube 
    global dbhelper

    cube = CubeService()    
    dbhelper = SQLiteHelper()
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 
