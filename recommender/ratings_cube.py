from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv
from cubes import Workspace, PointCut, Cell


def create_ratings():
    engine = create_engine('sqlite:///data.sqlite')
    create_table_from_csv(engine,
                       "syntetic_ratings.csv",
                       table_name="ratings",
                       fields=[
                             ("user_id", "integer"),
                             ("item_id", "integer"),
                             ("rating", "float"),
                             ("time", "integer")
                       ],
                       create_id=False
                   )

def create_movies():
    engine = create_engine('sqlite:///data.sqlite')
    create_table_from_csv(engine,
                       "sample_movies.csv",
                       table_name="movies",
                       fields=[
                             ("id", "integer"),
                             ("title", "string"),
                             ("genres", "string")
                       ],
                       create_id=False
                   )


def create_browser():
    #workspace = Workspace(config="slicer.ini")
    print("Creating Workspace and model")
    workspace = Workspace()
    workspace.register_default_store("sql", url="sqlite:///data.sqlite")
    
    workspace.import_model("movie_ratings_model.json")
    browser = workspace.browser("ratings")
    return browser

def execute_aggregations(browser):
    
    print()
    result = browser.aggregate()
    print("General aggregations")
    print("Record count: %s" % result.summary["record_count"])
    print()
    
    print("Drilldown by year")
    result = browser.aggregate(drilldown=["time"])
    for record in result:
        print(record)
    print("Drilldown by item")
    result = browser.aggregate(drilldown=["item"])
    for record in result:
        print(record)
    print("Drilldown by user")
    result = browser.aggregate(drilldown=["user"])
    for record in result:
        print(record)

def cslice(browser):
    print("Slicing by time")
    cut = PointCut("time", [5])
    cell = Cell(browser.cube, [cut])
    print ("dir cell")
    print(dir(cell))
    print(cell)
    result = browser.aggregate(cell, drilldown=["item"])
    print("result")
    print(result.summary)
    print(result.to_dict())
    for record in result:
        print(record)
    print("result cells")
    print(result.cell)
    print(browser.facts(cell))
    for cell in browser.facts(cell):
        print(cell)

def main():
    browser = create_browser()
    execute_aggregations(browser)
    cslice(browser)

if __name__== '__main__':
    print("Starting")
    #create_ratings()
    #create_movies()
    main()
