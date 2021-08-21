#The import that allows for server connections to Mongo
from pymongo import MongoClient

#The import that allows for querying with an ObjectID
from bson.objectid import ObjectId

#The class that contains all the definitions needed for CRUD
class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient using the specified path to my port 
        self.client = MongoClient('mongodb://%s:%s@localhost:37366/AAC' % (username, password))
        #Setting the AAC database to be worked from
        self.database = self.client['AAC']

# The method to implement the C in CRUD.
 
    def create(self, data: dict) -> bool:
        """A method to create documents in the database"""
        if data:
            # This will check if the animal_id is a Separate variable
            if "animal_id" in data.keys():
                check = list(self.database.animals.find(data))
                if check:
                    raise Exception("The ID is not available.")

            # Inserts document
            if self.database.animals.insert_one(data):
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save because the data parameter is empty.")

    def read(self, data: dict) -> list:
        """A method to read documents in the database"""
        if data:
            result = list(self.database.animals.find(data,{"_id":False}))
            # Check if the query returned results
            if len(result) > 0:
                return result
            else:
                raise Exception("No such document is in the database.")
        else:
             raise Exception("Nothing to find because this data parameter is empty.")
                
    def read_all(self, data: dict) -> object:
        """A method that will read all documents"""
        result = self.database.animals.find(data, {"_id":False})
        return result
    
    def filtered_rescue_dogs(self, rescue_type: str) -> object:
        """A filter method for rescue dog types"""
        if rescue_type == "Water":
            water_filter == {"animal_type":"Dog",
                           "breed":{"$in":["Labrador Retriever Mix","Chesapeake Bay Retriever","Newfoundland"]}, 
                           "sex_upon_outcome":"Intact Female",
                           "age_upon_outcome_in_weeks":{"$gte":26, "$lte":156}}
            result = self.database.animals.find(water_filter, {"_id":False})
        elif rescue_type == "Mountain":
            mountain_filter = {"animal_type":"Dog",
                              "breed":{"$in":["German Shephard","Alaskan Malamute","Old English Sheepdog",
                                       "Siberian Husky", "Rottweiler"]}, 
                              "sex_upon_outcome":"Intact Male",
                              "age_upon_outcome_in_weeks":{"$gte":26, "$lte":156}}
            result = self.database.animals.find(mountain_filter, {"_id":False})
        elif rescue_type == "Disaster":
            disaster_filter = {"animal_type":"Dog",
                              "breed":{"$in":["Doberman Pinscher", "German Shephard","Golden Retriever","Bloodhound",
                                       "Rottweiler"]}, 
                              "sex_upon_outcome":"Intact Male",
                              "age_upon_outcome_in_weeks":{"$gte":20, "$lte":300}}
            result = self.database.animals.find(disaster_filter, {"_id":False})
        else:
            raise Exception("Please enter a valid rescue type: Water, Mountain, or Disaster")
        return result
        
# The method to implement the U in CRUD.
    def update(self, search: dict, update: dict) -> object:
        """A method to update documents in the database"""
        update = {"$set":update}
        # Confirm that search and update data were provided
        if search and update:
            check = list(self.database.animals.find(search))
            # Check if the search data is in the database
            if check:
                result = self.database.animals.update_many(search, update)
            else:
                raise Exception("No documents match the search.")
        else:
            raise Exception("Data needed for search.")
        return result

    def delete(self, data: dict) -> object:
        """A method to delete documents in the database."""
        if data:
            check = list(self.database.animals.find(data))
            # Check if the query returned results
            if check:
                result = self.database.animals.delete_many(data)
            else:
                raise Exception("No data in database.")
        else:
            raise Exception("Data parameter is empty and there is nothing to delete.")
        return result