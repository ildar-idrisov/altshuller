import re
import ast
import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

GPT_MODEL = "gpt-3.5-turbo-16k" # gpt-3.5-turbo gpt-3.5-turbo-16k gpt-4 gpt-4-32k

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

# Определение 40 принципов ТРИЗ
TRIZ_principles = {
    1: "Segmentation",
    2: "Taking Out",
    3: "Local Quality",
    4: "Asymmetry",
    5: "Merging",
    6: "Universality",
    7: "Nested Doll",
    8: "Anti-Weight",
    9: "Preliminary Anti-Action",
    10: "Preliminary Action",
    11: "Beforehand Cushioning",
    12: "Equipotentiality",
    13: "Inversion",
    14: "Spheroidality",
    15: "Dynamicity",
    16: "Partial or Excessive Action",
    17: "Moving to a New Dimension",
    18: "Mechanical Vibration",
    19: "Periodic Action",
    20: "Continuity of Useful Action",
    21: "Skipping",
    22: "Blessing in Disguise",
    23: "Feedback",
    24: "Intermediary",
    25: "Self-Service",
    26: "Copying",
    27: "Cheap Short-Living",
    28: "Replacement of Mechanical System",
    29: "Pneumatics and Hydraulics",
    30: "Flexible Shells and Thin Films",
    31: "Porosity",
    32: "Color Changes",
    33: "Homogeneity",
    34: "Discarding and Recovering",
    35: "Parameter Changes",
    36: "Phase Transition",
    37: "Thermal Expansion",
    38: "Strong Oxidants",
    39: "Inert Atmosphere",
    40: "Composite Materials"
}

# Определение Стандартных Решений ТРИЗ
TRIZ_standard_solutions = {
    1: "Синтез веполя",
    2: "Переход к внутреннему комплексному веполю",
    3: "Переход к внешнему комплексному веполю",
    4: "Переход к веполю на внешней среде",
    5: "Переход к веполю на внешней среде с добавками",
    6: "Минимальный режим действия на вещество",
    7: "Максимальный режим действия на вещество",
    8: "Избирательно-максимальный режим",
    9: "Устранение вредной связи введением постороннего вещества",
    10: "Устранение вредной связи видоизменением имеющихся веществ",
    11: "Оттягивание вредного действия поля",
    12: "Противодействие вредным связям с помощью поля",
    13: '"Отключение" магнитных связей',
    14: "Переход к цепному веполю",
    15: "Переход к двойному веполю",
    16: "Переход к более управляемым полям",
    17: "Дробление инструмента",
    18: "Переход к капиллярно-пористому веществу",
    19: "Динамизация веполя",
    20: "Структуризация поля",
    21: "Структуризация вещества",
    22: "Согласование ритмики поля и изделия (или инструмента)",
    23: "Согласование ритмики используемых полей",
    24: "Согласование несовместимых или ранее независимых действий",
    25: "Переход к 'протофеполю'",
    26: "Переход к феполю",
    27: "Использование магнитной жидкости",
    28: "Использование капиллярно-пористой структуры феполя",
    29: "Переход к комплексному феполю",
    30: "Переход к феполю на внешней среде",
    31: "Использование физэффектов",
    32: "Динамизация феполя",
    33: "Структуризация феполя",
    34: "Согласование ритмики в феполе",
    35: "Переход к эполю - веполю с взаимодействующими токами",
    36: "Использование электрореологической жидкости",
    37: "Переход к бисистемам и полисистемам",
    38: "Развитие связей в бисистемах и полисистемах",
    39: "Увеличение различия между элементами бисистем и полисистем",
    40: "Свертывание бисистем и полисистем",
    41: "Несовместимые свойства системы и ее частей",
    42: "Переход на микроуровень",
    43: "Вместо обнаружения и измерения - изменение системы",
    44: "Использование копий",
    45: "Последовательное обнаружение изменений",
    46: "Синтез измерительного веполя",
    47: "Переход к комплексному измерительному веполю",
    48: "Переход к измерительному веполю на внешней среде",
    49: "Получение добавок во внешней среде",
    50: "Использование физэффектов",
    51: "Использование резонанса контролируемого объекта",
    52: "Использование резонанса присоединенного объекта",
    53: "Переход к измерительному 'протофеполю'",
    54: "Переход к измерительному феполю",
    55: "Переход к комплексному измерительному феполю",
    56: "Переход к измерительному феполю на внешней среде",
    57: "Использование физэффектов",
    58: "Переход к измерительным бисистемам и полисистемам",
    59: "Переход к измерению производных",
    60: "Обходные пути",
    61: "Разделение изделия на взаимодействующие части",
    62: "Самоустранение отработанных веществ",
    63: "Использование надувных конструкций и пены",
    64: "Использование поля по совместительству",
    65: "Использование поля внешней среды",
    66: "Использование веществ-источников полей",
    67: "Замена фазового состояния вещества",
    68: "'Двойственное' фазовое состояние вещества",
    69: "Использование явлений, сопутствующих фазовому переходу",
    70: "Переход к двухфазному состоянию вещества",
    71: "Использование взаимодействия между частями (фазами) системы",
    72: "Использование обратимых физических превращений",
    73: "Усиление поля на выходе",
    74: "Получение частиц вещества разложением",
    75: "Получение частиц вещества объединением",
    76: "Простейшие способы получения частиц вещества"
}

TRIZ_laws_of_technical_system_evolution = {
    1: "Law of Completeness of the Parts of the System",
    2: "Law of 'Energy Conductivity' of the System",
    3: "Law of Coordination of the Rhythm of Parts of the System",
    4: "Law of Increasing the Degree of Ideality of the System",
    5: "Law of Uneven Development of Parts of the System",
    6: "Law of Transition to a Supersystem",
    7: "Law of Transition from Macro-level to Micro-level",
    8: "Law of Increasing the Degree of Substance-Field Interaction",
}

def extract_scores(s):
    try:
        match_func = re.search(r"Functionality: (\d+)", s)
        match_cost = re.search(r"Cost: (\d+)", s)
        if match_func and match_cost:
            functionality_score = int(match_func.group(1))
            cost_score = int(match_cost.group(1))
            return (functionality_score, cost_score)
    except (ValueError, IndexError, AttributeError) as e:
        return None
    return None

def extract_python_list(s):
    # Регулярное выражение для поиска Python list в строке
    pattern = re.compile(r'(\[\s*(?:(?:\d+|"[^"]*"|\'[^\']*\')(?:\s*,\s*(?:\d+|"[^"]*"|\'[^\']*\'))*)?\s*\])')
    match = pattern.search(s)
    if match:
        # Извлечение и преобразование Python list из строки
        python_list_str = match.group(1)
        try:
            # Преобразование строки в фактический Python list с помощью модуля ast
            python_list = ast.literal_eval(python_list_str)
            return python_list
        except (ValueError, SyntaxError):
            return None
    return None

def get_request(content, prompt, check_function=None, temp=0.5):
    for i in range(5):
        completion = openai.ChatCompletion.create(
            model = GPT_MODEL,
            messages = [
                {"role": "system", "content": content},
                {"role": "user", "content": prompt}
            ],
            temperature = temp,
        )
        answer = completion.choices[0].message.content

        if check_function is not None:
            answer = check_function(answer)
            if answer is not None:
                return answer
        else:
            return answer

    print("Error: wrong response")
    raise Exception("Invalid response from ChatGPT")
    return None

### 1. Анализ входных данных пользователя и формулирование проблемы
def define_problem(user_input):
    prompt=f"Based on the provided description, please define and formulate the problem, identify key parameters, and explore possible solutions: {user_input}"
    res = get_request(triz_content["problem_definition"], prompt)
    return res

### 2. Идентификация противоречий в проблемном заявлении
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
    prompt=f"Identify technical conflicts in the following parameters and requirements and write them to a Python list: '{parameters_and_requirements}'. Don't write anything else, just python list"
    res = get_request(triz_content["conflict_analysis"], prompt, extract_python_list)
    return res

def identify_physical_conflicts(parameters_and_requirements):
    prompt=f"Identify physical conflicts in the following parameters and requirements and write them to a Python list: '{parameters_and_requirements}'. Don't write anything else, just Python List"
    res = get_request(triz_content["conflict_analysis"], prompt, extract_python_list)
    return res

### 3. Применение стандартных решений ТРИЗ для разрешения противоречий
### https://altshuller.ru/triz/technique1.asp
### https://altshuller.ru/triz/standards.asp
def apply_standard_solutions(identified_conflicts):
    # Список для хранения возможных решений
    possible_solutions = []

    for conflict in identified_conflicts['technical_conflicts']:
        # Применение принципов ТРИЗ к техническим противоречиям
        principle_descriptions = choose_principle_based_on_conflict(conflict)
        for principle in principle_descriptions:
            solution = generate_solution_based_on_principle(principle, conflict)
            possible_solutions.append(solution)

    for conflict in identified_conflicts['physical_conflicts']:
        # Применение Стандартных Решений ТРИЗ к физическим противоречиям
        standard_solution_descriptions = choose_standard_solution_based_on_conflict(conflict)
        for standard in standard_solution_descriptions:
            solution = generate_solution_based_on_standard_solution(standard, conflict)
            possible_solutions.append(solution)

    return possible_solutions

def choose_principle_based_on_conflict(conflict):
    # Примерный алгоритм выбора принципа на основе анализа конфликта
    principle_description = []

    prompt=f"Based on the analysis of technical conflict: '{conflict}', please suggest the most suitable numbers of TRIZ principles from '{TRIZ_principles}' to address this conflict. Don't write anything else, just Python List"
    res = get_request(triz_content["standard_solutions"], prompt, extract_python_list)
    for item in res:
        principle_description.append(TRIZ_principles[int(item)])
    return principle_description

def choose_standard_solution_based_on_conflict(conflict):
    # Примерный алгоритм выбора Стандартного Решения на основе анализа конфликта
    standard_solution_description = []

    prompt=f"Based on the analysis of physical conflict: '{conflict}', please suggest the most suitable numbers of TRIZ standard solutions from '{TRIZ_standard_solutions}' to address this conflict. Don't write anything else, just Python List"
    res = get_request(triz_content["standard_solutions"], prompt, extract_python_list)
    for item in res:
        standard_solution_description.append(TRIZ_standard_solutions[int(item)])
    return standard_solution_description

def generate_solution_based_on_principle(principle, conflict):
    # Генерация решения на основе выбранного принципа и конфликта
    prompt=f"Given the selected TRIZ principle: '{principle}', and the identified technical conflict: '{conflict}', please generate a solution to resolve the conflict. Provide a detailed explanation of how the principle can be applied to address the issues and achieve a resolution."
    res = get_request(triz_content["standard_solutions"], prompt)
    return res

def generate_solution_based_on_standard_solution(standard_solution, conflict):
    # Генерация решения на основе выбранного Стандартного Решения и конфликта
    prompt=f"Given the selected TRIZ standard solution: '{standard_solution}', and the identified physical conflict: '{conflict}', please generate a solution to resolve the conflict. Provide a detailed explanation of how the standard solution can be applied to address the issues and achieve a resolution."
    res = get_request(triz_content["standard_solutions"], prompt)
    return res

### 4. Анализ трендов и законов развития технических систем в области проблемы
### https://altshuller.ru/triz/zrts1.asp
def apply_technical_system_evolution_laws(problem_statement):
    analysis_results = {}
    for law_number, law_name in TRIZ_laws_of_technical_system_evolution.items():
        # Analyze the problem_statement with respect to the current law.
        prompt=f"Analyze the current state of my system described as follows: '{problem_statement}' based on the law of technical system evolution: {law_name}"
        res = get_request(triz_content["laws_of_technical_system_evolution"], prompt)
        analysis_results[law_name] = res

    return analysis_results

### 5. Оценка потенциальных решений с точки зрения их функциональности и стоимости
def perform_functional_cost_analysis(potential_solutions):
    analyzed_solutions = []
    
    for solution in potential_solutions:
        prompt = f"""Evaluate the following proposed solution in terms of its functionality score (0-100) and cost score (0-100): '{solution}'
        - Functionality: 
        - Cost: 
        """

        evaluation = get_request(triz_content["functional_cost_analysis"], prompt, extract_scores)
        functionality_score = evaluation[0]
        cost_score = evaluation[1]

        analyzed_solution = {
            'solution': solution,
            'functionality_score': functionality_score,
            'cost_score': cost_score,
            'balance_score': functionality_score - cost_score  # A simple measure of balance
        }
        
        analyzed_solutions.append(analyzed_solution)
    
    return analyzed_solutions

### 6. Генерация и документирование новых идей на основе проведенных анализов и решений
def generate_ideas(analyses):
    # Prepare a list to collect new ideas
    new_ideas = []

    # Analyze the evolution analysis results to identify opportunities or challenges
    for law_name, analysis_result in evolution_analysis.items():
        # This is a simplified example; you might have more complex analysis logic here
        if 'opportunity' in analysis_result:
            prompt = f"Based on the analysis of technical system evolution, suggest innovative solutions or improvements for the problem at hand. Here's the analysis summary: '{analysis_result}'. Please provide ideas that align with the observed evolution trends and laws, and suggest how these ideas can address the identified problem. Write all solutions as a Python List"
            res = get_request(triz_content["idea_generation"], prompt)
            new_ideas.append(res)

    # Analyze the functional cost analysis results to identify high-potential solutions
    for analyzed_solution in functional_cost_analysis_result:
        # For simplicity, let's consider solutions with a balance score of zero as high-potential
        if analyzed_solution['balance_score'] >= 0:
            formatted_analysis_results = '\n'.join(
                [f"- Solution: {analyzed_solution['solution']}, Functionality Score: {analyzed_solution['functionality_score']}, Cost Score: {analyzed_solution['cost_score']}, Balance Score: {analyzed_solution['balance_score']}" 
                for result in functional_cost_analysis_result]
            )
            prompt = f"Based on the Functional Cost Analysis, the following solutions were evaluated: '{formatted_analysis_results}'. Given this analysis, what might be some innovative ideas to improve the functionality while maintaining or reducing the cost? Additionally, what other aspects should be considered to create a balanced solution? Write all solutions as a Python List"
            res = get_request(triz_content["idea_generation"], prompt)
            new_ideas.append(new_idea)

    # Additional idea generation logic can go here...
    # For example, you might identify and resolve contradictions, apply inventive principles, etc.

    return new_ideas

### 7. Разработка механизмов для сбора обратной связи от пользователей или экспертов по предложенным идеям
def gather_feedback(new_ideas):
    feedback = ["feedback1", "feedback2"]  # Это простой пример, в реальности может потребоваться сложный процесс сбора обратной связи
    return feedback


### Запуск
user_input = "На Кипре проблема с поливом растений. Очень много морской воды, но при этом очень мало пресной воды для полива. Додей тоже очень мало. Как можно решить проблемы с поливом растений, чтоб можно было повсеместно иметь газоны и низкой стоимость полива"

problem_statement = define_problem(user_input)
print("Log: 1")
conflicts = analyze_conflicts(problem_statement)
print("Log: 2")
solutions = apply_standard_solutions(conflicts)
print("Log: 3")
evolution_analysis = apply_technical_system_evolution_laws(problem_statement)
print("Log: 4")
functional_cost_analysis_result = perform_functional_cost_analysis(solutions)
print("Log: 5")
new_ideas = generate_ideas([evolution_analysis, functional_cost_analysis_result])
print("Log: 6")
feedback = gather_feedback(new_ideas)
print("Log: 7")
for idea in new_ideas:
    print(idea)
    print("===============")