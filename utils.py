import json
import re


def read_questions(file_name):
    f = open(file_name)
    questions = json.load(f)
    f.close()
    return questions


def post_process_query(sparql_query):
    # remove_special_characters_and_extra_spaces and add_space_before_question_mark
    # Replace '\n' with a space
    cleaned_sparql_query = sparql_query.replace("\n", ' ')
    cleaned_sparql_query = cleaned_sparql_query.replace("\'", '')
    # Replace '\\' with a single '\'
    cleaned_sparql_query = cleaned_sparql_query.replace("\\", '')
    # Replace '\' with an empty string
    cleaned_sparql_query = cleaned_sparql_query.replace("\\", '')
    # Remove extra spaces using regular expressions
    cleaned_sparql_query = re.sub(r'\s+', ' ', cleaned_sparql_query)
    cleaned_string = re.sub(r'\\.', '', cleaned_sparql_query)
    # Use regular expressions to add a space before '?'
    modified_sparql_query = re.sub(r'(\S)\?', r'\1 ?', cleaned_string)
    return modified_sparql_query
