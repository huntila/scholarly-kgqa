from SPARQLWrapper import SPARQLWrapper, JSON
import json
import utils

count = 0
prefix = "PREFIX orkgc: <http://orkg.org/orkg/class/> PREFIX orkgp: <http://orkg.org/orkg/predicate/> PREFIX orkgsh: <http://orkg.org/orkg/shapes/>"


def write_predicted_answer_to_file(answer_results, file_name):
    newarr = []
    for item in answer_results:
        newanswer = []
        if not item['answer']:
            newarr.append({"id": item["id"], "answer": []})
        else:
            answer = item["answer"]
            # if 'results' in item['answer']:
            if 'bindings' in answer['results']:
                for ans in answer['results']['bindings']:
                    for k, v in ans.items():
                        newanswer.append(ans[k]["value"])
                newarr.append({"id": item["id"], "answer": newanswer})
    with open(file_name, 'w') as f:
        json.dump(newarr, f, indent=2)
    print('Saved to file!')


def error_analysis(answer_results):
    for item in answer_results:
        if not item['answer']:
            print(item['id'])


def answer_extraction(query):
    post_processed_query = utils.post_process_query(query)
    prefixed_query = prefix + " " + post_processed_query
    # print(prefixed_query)
    try:
        sparql = SPARQLWrapper("https://ltdemos.informatik.uni-hamburg.de/orkg/sparql")
        sparql.setQuery(prefixed_query)
        sparql.setReturnFormat(JSON)
        answer = sparql.query().convert()
        return answer
    except Exception as e:
        print(f"An error occurd: {str(e)}")
        return None
