# EchoEcho takehome project

## How to run the Code

To run this solution follow these steps:

- Install `pipenv` using the instructions from [here](https://github.com/pypa/pipenv#installation).
- Clone the project's repository from [https://github.com/josernestodavila/echoecho-data-ingest.git](https://github.com/josernestodavila/echoecho-data-ingest.git).
- Install the project's dependencies running `pipenv install`.
- Run the data ingestion with `pipenv run python ingest_data.py`.

## Technical Specification

I tried to implement the solution as simple as possible using the standard library as much as possible. The only extra package
I used is `requests` which provides an elengant interface to make HTTP requests. The main problem I found on this project was to
parse the data files based on the specification coming in another schema file, in the end I decided to use the schema file to define
slice's boundaries that will be used to extract the information from the data files using python string slicing. The data transformation
to python native types is being done using a mapping from the accepted data types in the database to native python types, this goal is achieved
in the `_make_data_parser()` method on the `PerformanceDataParser` class. The `PerformanceDataParser` also encapsulates the ability to push the
data to the API in the `_push_to_api()` method that is called from the `ingest()` method.

### Another Possible Approaches

Originally I wanted to build a RegEx expression using the schema specification from the schema files, but I'm not fond of using regular expression since
they tend to be not easy to read for everyone.
 
Another possible solution could have come from the Python's `struct` module, since it allows to define a string format to the parse a binary object, but 
I've never used it before and didn't want to invest much time unraveling how it works.

## Bonus question:

To ensure that the contents of the API's database match the data files the API must provide an endpoint to query the data stored in the API's database so that
we can use the `measure_id` from the data files to make a call to the API and compare the data coming from the API with the corresponding data in the file.
