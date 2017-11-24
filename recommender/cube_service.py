from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv
from cubes import Workspace, PointCut, Cell


class CubeService(object):

    def __init__(self):
        print("Creating Workspace and model")
        workspace = Workspace()
        workspace.register_default_store("sql", url="sqlite:///data.sqlite")

        workspace.import_model("movie_ratings_model.json")
        browser = workspace.browser("ratings")

        self.browser = browser
    

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
    
    def execute_aggregations(self):
        
        print()
        result = self.browser.aggregate()
        print("General aggregations")
        print("Record count: %s" % result.summary["record_count"])
        print()
        
        print("Drilldown by year")
        result = self.browser.aggregate(drilldown=["time"])
        for record in result:
            print(record)
        print("Drilldown by item")
        result = self.browser.aggregate(drilldown=["item"])
        for record in result:
            print(record)
        print("Drilldown by user")
        result = self.browser.aggregate(drilldown=["user"])
        for record in result:
            print(record)
    
    def cslice(self, dimension, values):
        print("Slicing by %s" % dimension)
        cut = PointCut("time", [5])
        cell = Cell(self.browser.cube, [cut])
        result = self.browser.aggregate(cell, drilldown=["item"])
        print("result")
        print(result.summary)
        print(result.to_dict())
        for record in result:
            print(record)
        print("result cells")
        print(result.cell)
        print(self.browser.facts(cell))
        #for cell in self.browser.facts(cell):
        #    print(cell)
        ratings = [rating for rating in self.browser.facts(cell)]
        result = []
        for rating in self.browser.facts(cell):
           print("Before")
           print(rating)
           rating["rating"]=float(rating["rating"])
           print("After")
           print(rating)
           result.append(rating)
        print(result)
        return result

def main():
    cube = CubeService()
    #browser = create_browser()
    cube.execute_aggregations()
    cube.cslice("time", [5])

if __name__== '__main__':
    print("Starting")
    #create_ratings()
    #create_movies()
    main()
