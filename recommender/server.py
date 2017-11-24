import time, sys, cherrypy, os
from paste.translogger import TransLogger
from app import create_app



def init_cubes():
    # load spark context
    #conf = SparkConf().setAppName("movie_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
   # sc = SparkContext(conf=conf, pyFiles=['engine.py', 'app.py'])
    print("TODO: init cube")
    #return sc
 
 
def run_server(app):
 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 4321,
        'server.socket_host': '0.0.0.0'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
 
 
if __name__ == "__main__":
    # Init spark context and load libraries
    #dataset_path = os.path.join('datasets', 'ml-latest')
    dataset_path = os.path.join('datasets', 'ml-latest-small')
    app = create_app( dataset_path)
 
    # start web server
    run_server(app)

