from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv
from cubes import Workspace

engine = create_engine('sqlite:///data.sqlite')
create_table_from_csv(engine,
                   "IBRD_Balance_Sheet__FY2010.csv",
                   table_name="ibrd_balance",
                   fields=[
                         ("category", "string"),
                         ("category_label", "string"),
                         ("subcategory", "string"),
                         ("subcategory_label", "string"),
                         ("line_item", "string"),
                         ("year", "integer"),
                         ("amount", "integer")],
                   create_id=True
               )



#workspace = Workspace(config="slicer.ini")
print("Creating Workspace and model")
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///data.sqlite")

workspace.import_model("tutorial_model.json")
browser = workspace.browser("ibrd_balance")

print()
result = browser.aggregate()
print("General aggregations")
print("Record count: %s" % result.summary["record_count"])
print("Amount sum: %s" % result.summary["amount_sum"])
print()

print("Drilldown by year")
result = browser.aggregate(drilldown=["year"])
for record in result:
    print(record)
print("Drilldown by item")
result = browser.aggregate(drilldown=["item"])
for record in result:
    print(record)
