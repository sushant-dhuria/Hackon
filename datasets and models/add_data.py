#importing required libraries
import weaviate
import pandas as pd
from datetime import datetime
import re
#setting up client
client = weaviate.Client("http://localhost:8080")

def convert_to_rfc3339(date_string):
    try:
        # Parse the input date string
        input_date = datetime.strptime(date_string, '%Y-%m-%d')

        # Add the time and format in RFC3339 format
        rfc3339_date = input_date.strftime('%Y-%m-%dT00:00:00Z')
        return rfc3339_date
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."
def convert_to_minutes(time_string):
    # Use regular expressions to extract hours and minutes
    time_parts = re.findall(r'(\d*H)?(\d*M)?', time_string)
    
    if not time_parts or (not time_parts[0][0] and not time_parts[0][1]):
        return "Invalid time format. Please use 'XH' and/or 'XM' where X is the number of hours and minutes."
    
    # Extract hours and minutes
    hours, minutes = 0, 0
    if time_parts[0][0]:
        hours = int(time_parts[0][0].rstrip('H'))
    if time_parts[0][1]:
        minutes = int(time_parts[0][1].rstrip('M'))
    
    # Calculate total minutes
    total_minutes = hours * 60 + minutes
    
    return total_minutes
#Checking if Movies schema already exists, then delete it
current_schemas = client.schema.get()['classes']
for schema in current_schemas:
    if schema['class']=='Movies':
        client.schema.delete_class('Movies')

#creating the schema
movie_class_schema = {
    "class": "Movies",
    "description": "A collection of movies with title, description, director, actors, rating, etc.",
    "properties": [
        {
            "name": "movie_id",
            "dataType": ["number"],
            "description": "The id of the movie", 
        },
        {
            "name": "best_rating",
            "dataType": ["number"],
            "description": "best rating of the movie", 
        },        
        {
            "name": "worst_rating",
            "dataType": ["number"],
            "description": "worst rating of the movie", 
        },
        {
            "name": "url",
            "dataType": ["string"],
            "description": "The IMBD url of the movie", 
        },
        {
            "name": "title",
            "dataType": ["string"],
            "description": "The name of the movie", 
        },
        {
            "name": "poster_link",
            "dataType": ["string"],
            "description": "The poster link of the movie", 
        },
        {
            "name": "genres",
            "dataType": ["text[]"],
            "description": "The genres of the movie", 
        },
        {
            "name": "actors",
            "dataType": ["text[]"],
            "description": "The actors of the movie", 
        },
        {
            "name": "director",
            "dataType": ["string"],
            "description": "Director of the movie", 
        },
        {
            "name": "description",
            "dataType": ["string"],
            "description": "overview of the movie", 
        },
        {
            "name": "date_published",
            "dataType": ["date"],
            "description": "The date on which movie was published", 
        },
        {
            "name": "keywords",
            "dataType": ["text[]"],
            "description": "main keywords of the movie", 
        },
        {
            "name": "rating_count",
            "dataType": ["number"],
            "description": "rating count of the movie", 
        }, 
        {
            "name": "rating_value",
            "dataType": ["number"],
            "description": "rating value of the movie", 
        },
        {
            "name": "review_aurthor",
            "dataType": ["string"],
            "description": "aurthor of the review", 
        },
        {
            "name": "review_date",
            "dataType": ["string"],
            "description": "date of review", 
        },
        {
            "name": "review_body",
            "dataType": ["string"],
            "description": "body of the review", 
        },
        {
            "name": "duration",
            "dataType": ["number"],
            "description": "the duration of the review", 
        }
    ]
}
client.schema.create_class(movie_class_schema)

#Configure batch process - for faster imports 
#see: https://weaviate.io/developers/weaviate/current/restful-api-references/batch.html
client.batch.configure(
  batch_size=10, 
  # dynamically update the `batch_size` based on import speed
  dynamic=True,
  timeout_retries=3,
)

#Change the path to the place where data csv file is present
data=pd.read_csv("final_data.csv")
data = data.dropna(subset=['DatePublished'])
data = data.dropna(subset=['duration'])
#Adding the data
#You can decrease number of objects to be inserted to decrease the amount of time required
for i in range (0,len(data)):
    item = data.iloc[i]
    movie_object = {
        'movie_id':float(item['id']),
        'url':str(item['url']),
        'title': str(item['Name']).lower(),
        'poster_link': str(item['PosterLink']),
        'genres':str(item['Genres']).split(","),
        'actors': (str(item['Actors']).lower()).split(","),
        'director': str(item['Director']).lower(),
        'description':str(item['Description']),
        'date_published':convert_to_rfc3339(item['DatePublished']),
        'keywords': str(item['Keywords']).split(","),
        'worst_rating': float(item['WorstRating']),
        'best_rating': float(item['BestRating']),
        'rating_count': float(item['RatingCount']),
        'rating_value':float(item['RatingValue']),
        'review_aurthor': str(item['ReviewAurthor']),
        'review_body': str(item['ReviewBody']),
        'review_date': str(item['ReviewDate']),
        'duration': float(convert_to_minutes(str(item['duration'])))
    }
    try:
        client.batch.add_data_object(movie_object, "Movies")
    except BaseException as error:
        print("Import Failed at: ",i)
        print("An exception occurred: {}".format(error))
        # Stop the import on error
        break

    print("Status: ", str(i)+"/"+str(len(data)))

client.batch.flush()