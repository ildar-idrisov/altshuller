import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

GPT_MODEL = "gpt-3.5-turbo-16k", # gpt-3.5-turbo gpt-3.5-turbo-16k gpt-4 gpt-4-32k

triz_content_common = "You are a Certified TRIZ Practitioner, proficient in TRIZ tools such as the Contradiction Matrix, Function Analysis, Root Cause Analysis, and the Ideality Concept. You are familiar with modern software development practices and agile methodologies. You have experience in problem-solving and algorithm development. You possess a visionary outlook towards the future of product development and innovation."
triz_content = {
    "problem_definition": triz_content_common + "You are tasked with gathering and articulating the problem or the area of innovation based on user input.",
    "conflict_analysis": triz_content_common + "You identify technical and physical contradictions within the current scenario based on the defined problem.",
    "standard_solutions": triz_content_common + "You employ TRIZ standard solutions to address the identified contradictions.",
    "laws_of_technical_system_evolution": triz_content_common + "You analyze the current trends and laws of technical system evolution in the area of the problem.",
    "functional_cost_analysis": triz_content_common + "You evaluate potential solutions in terms of their functionality and cost, offering a balanced approach to problem-solving.",
    "idea_generation": triz_content_common + "You generate and document new ideas based on the analyses and solutions derived from previous steps.",
    "feedback_gathering": triz_content_common + "You develop mechanisms for gathering feedback from users or experts on the proposed ideas, iterating and improving upon the generated ideas based on the feedback."
}



def get_request(content, prompt):
    completion = openai.ChatCompletion.create(
        model = GPT_MODEL
        messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
    )
    answer = completion.choices[0].message.content
    return answer

# 1. Анализ входных данных пользователя и формулирование проблемы
def define_problem(user_input):
    problem_statement = user_input  # Это простое присваивание, в реальности может потребоваться анализ текста
    return problem_statement

# 2. Идентификация противоречий в проблемном заявлении
def analyze_conflicts(problem_statement):
    # Сначала разберите проблемное заявление на составные части, чтобы выявить ключевые параметры и требования.
    # Это может включать в себя текстовый анализ, анализ данных или даже консультации с экспертами.
    parameters_and_requirements = extract_parameters_and_requirements(problem_statement)

    # Идентификация технических противоречий:
    # Технические противоречия возникают, когда улучшение одного параметра ведет к ухудшению другого.
    technical_conflicts = identify_technical_conflicts(parameters_and_requirements)

    # Идентификация физических противоречий:
    # Физические противоречия возникают, когда один и тот же параметр должен иметь противоположные значения.
    physical_conflicts = identify_physical_conflicts(parameters_and_requirements)

    # Сбор и возврат результатов анализа
    conflicts = {
        'technical_conflicts': technical_conflicts,
        'physical_conflicts': physical_conflicts
    }
    return conflicts

def extract_parameters_and_requirements(problem_statement):
    prompt=f"Extract the parameters and requirements from the following problem statement: {problem_statement}"
    res = get_request(triz_content["conflict_analysis"], prompt)
    return res

def identify_technical_conflicts(parameters_and_requirements):
    prompt=f"Identify technical conflicts in the following parameters and requirements: {parameters_and_requirements}"
    res = get_request(triz_content["conflict_analysis"], prompt)
    return res

def identify_physical_conflicts(parameters_and_requirements):
    prompt=f"Identify physical conflicts in the following parameters and requirements: {parameters_and_requirements}"
    res = get_request(triz_content["conflict_analysis"], prompt)
    return res

# 3. Применение стандартных решений ТРИЗ для разрешения противоречий
def apply_standard_solutions(conflicts):
    solutions = ["solution1", "solution2"]
    return solutions

# 4. Анализ трендов и законов развития технических систем в области проблемы
def apply_technical_system_evolution_laws(problem_statement):
    evolution_analysis = "analysis_result"  # Это простой пример, в реальности может потребоваться сложный анализ
    return evolution_analysis

# 5. Оценка потенциальных решений с точки зрения их функциональности и стоимости
def perform_functional_cost_analysis(potential_solutions):
    analysis_result = "analysis_result"  # Это простой пример, в реальности может потребоваться сложный анализ
    return analysis_result

# 6. Генерация и документирование новых идей на основе проведенных анализов и решений
def generate_ideas(analyses):
    new_ideas = ["idea1", "idea2"]  # Это простой пример, в реальности может потребоваться сложный процесс генерации идей
    return new_ideas

# 7. Разработка механизмов для сбора обратной связи от пользователей или экспертов по предложенным идеям
def gather_feedback(new_ideas):
    feedback = ["feedback1", "feedback2"]  # Это простой пример, в реальности может потребоваться сложный процесс сбора обратной связи
    return feedback



user_input = "Нам нужно улучшить эффективность нашего производственного процесса."

problem_statement = define_problem(user_input)
conflicts = analyze_conflicts(problem_statement)
solutions = apply_standard_solutions(conflicts)
evolution_analysis = apply_technical_system_evolution_laws(problem_statement)
functional_cost_analysis_result = perform_functional_cost_analysis(solutions)
new_ideas = generate_ideas([evolution_analysis, functional_cost_analysis_result])
feedback = gather_feedback(new_ideas)
