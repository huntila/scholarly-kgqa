import json
import requests
import utils
import answer_extraction


def construct_prompt(question, sim_questions, shots):
    example = ''
    if shots != 1:
        for item in sim_questions[:shots]:
            sim_question = item['similar_question']
            sparql = utils.post_process_query(item['similar_question_sparql'])
            example += (f"Question: {sim_question}\n"
                        f"Sparql: {sparql}\n")
    else:
        item = sim_questions[0]
        sim_question = item['similar_question']
        sparql = utils.post_process_query(item['similar_question_sparql'])
        example += (f"Question: {sim_question}\n"
                    f"Sparql: {sparql}\n")
    return f"""
          Task: Generate SPARQL queries to query the ORKG knowledge graph based on the provided schema definition.
          Instructions:
          If you cannot generate a SPARQL query based on the provided examples, explain the reason to the user.
          {example}
          Question: {question}
          Sparql:
          Note: Do not include any explanations or apologies in your responses.
          Output only the Sparql query.
        """


def generate_sparql(question_list, shot):
    results = []
    for questions in question_list:
        question = questions['question']
        question_id = questions['id']
        prompt = construct_prompt(question, questions['top_n_similar_questions'], shot)  # pass 1, for 1 shot
        # print(prompt)
        sparql = run_llm(prompt)
        cleaned_sparql = utils.post_process_query(sparql)
        temp = {}
        temp.update({"id": question_id, "sparql": cleaned_sparql})
        print(temp)
        results.append(temp)
    return results


def run_llm(prompt):
    key = " "  # key to access the LLM
    response = requests.post(
        url='https://turbo.skynet.coypu.org/',
        headers={"content-type": "application/json"},
        json={
            "model": 'vicuna-13b-v1.5',
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "key": key,
        },
    )
    response.raise_for_status()
    return response.json()[0]["choices"][0]["message"]["content"]


def query_generation(top_n_similar_questions_path, save_generated_sparql_to, shot):
    test_questions_similar_questions = utils.read_questions(top_n_similar_questions_path)
    result = generate_sparql(test_questions_similar_questions, shot)
    with open(save_generated_sparql_to, 'w') as outfile:
        json.dump(result, outfile, indent=2)
    print(f'Generated queries saved to {save_generated_sparql_to} successfully!')


def answer_generation(sparql_file_path, save_predicted_answer_to):
    count = 0
    fin_queries = utils.read_questions(sparql_file_path)
    answer_results = []
    for query in fin_queries:
        sparql_q = query['sparql']
        result = answer_extraction.answer_extraction(sparql_q)
        if not result:
            count += 1
            print(count)
        answer_results.append({'id': query['id'], 'answer': result})
    # print(answer_results)
    answer_extraction.write_predicted_answer_to_file(answer_results, save_predicted_answer_to)
    print(f'Predicted answers saved to {save_predicted_answer_to} successfully!')


if __name__ == '__main__':
    top_n_similar_questions = "data/dev/dev_questions_top_n_similar_questions.json"
    sparql_query_path = 'data/dev/sparql.json' # specify the sparql path here
    query_generation(top_n_similar_questions, sparql_query_path, 1)  # 1, 3, 5 for one|three|five-shot
    predicted_answer = 'data/dev/sample_answer.json'
    answer_generation(sparql_query_path, predicted_answer)
