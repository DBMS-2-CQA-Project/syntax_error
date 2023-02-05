def find(tag, str):
    """ A helper function which will helps in finding 
        if a tag is present in a list of tags 
        of the form  "<tag1> <tag2> ... " 
        Returns True if present
                                            """
    tag_list = str[1:-1].split('> <')   # splits the sting into list of tags
    if(tag in tag_list):
        return True
         
    return False


def find_using_tags(d , *tags):
    """
        Arguments: d = list of dictionaries,
               *tags = variable number of tags which the user is searching for
    
    Function to print all the rows in the list of dict
    which contains all the tags which the user is searching for(intersection)
                                                                                """
    is_present = False
    for row in d:
        for tag in tags:
            if(find(tag, row['tags'])):
                is_present = True
            else:
                is_present = False
                break
        
        if(is_present):
            print(row['id'], row['owner_id'], row['tags'])



def find_using_xyz(d, attribute, value):
    """ Function to print all the rows in the list 
        of dicts which contains the value which the user 
        is searching for according to the attribute he/she chose. 
                                                                 """
    for i in range(len(d)):
        if(d[i][attribute] == value):
            print(d[i])

# Sample list of dictionaries
d = [{'id': 1, 'owner_id': 8802, 'tags': "<python> <c++>"}, 
{'id': 2, 'owner_id': 123, 'tags': "<python> <c>"}, 
{'id': 3, 'owner_id': 1234, 'tags': "<javascript> <cp>"}, 
{'id': 4, 'owner_id': 1234, 'tags': "<java> <c#>"}, 
{'id': 5, 'owner_id': 1234, 'tags': "<django> <flask>"}, 
{'id': 6, 'owner_id': 1234, 'tags': "<python> <latex>"},
{'id': 7, 'owner_id': 211, 'tags': "<c--> <c++>"}, 
{'id': 8, 'owner_id': 211, 'tags': "<python> <cpp>"}]


# Test 1
find_using_tags(d, 'python')

# Test2
find_using_tags(d, 'c', 'python')

# Test3 
find_using_xyz(d, 'owner_id', 1234)