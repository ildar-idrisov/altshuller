import re
import ast
import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

GPT_MODEL = "gpt-3.5-turbo-16k" # gpt-3.5-turbo gpt-3.5-turbo-16k gpt-4 gpt-4-32k

MAX_NUM_TECH_CONFLICTS = 2
MAX_NUM_PHIS_CONFLICTS = 2
MAX_NUM_PRINC = 2
MAX_NUM_STAND = 2

triz_content_common = "You are a Certified TRIZ Practitioner. You have experience in problem-solving and possess a visionary outlook towards the future of product development and innovation."
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

TRIZ_principles_IT = {
    1: "Segmentation",
        # Breaking down software into microservices or modules for better manageability and scalability.
    2: "Taking Out",
        # Isolating or extracting specific functions or components to simplify or optimize the system.
    3: "Local Quality",
        # Tailoring solutions to specific parts of the software to address localized issues.
    4: "Asymmetry",
        # Introducing asymmetrical solutions or architectures to address unique challenges.
    5: "Merging",
        # Combining functionalities or modules to reduce redundancy and improve efficiency.
    6: "Universality",
        # Creating universal or generic solutions that can address a range of problems.
    7: "Nested Doll",
        # Implementing nested or hierarchical structures to organize and manage software components.
    8: "Anti-Weight",
        # Reducing the load or computational burden on specific parts of the system.
    9: "Preliminary Anti-Action",
        # Anticipating potential issues and implementing preemptive solutions.
    10: "Preliminary Action",
        # Implementing proactive measures to ensure smoother operations or transitions.
    11: "Beforehand Cushioning",
        # Building in fail-safes or fallback mechanisms to mitigate risks.
    12: "Equipotentiality",
        # Balancing the load or responsibilities among different parts of the system.
    13: "Inversion",
        # Reversing processes or logic to discover new solutions or perspectives.
    14: "Spheroidality",
        # Optimizing the structure or organization of the software for more rounded or flexible operation.
    15: "Dynamicity",
        # Introducing dynamic or adaptive behaviors to respond to changing conditions.
    16: "Partial or Excessive Action",
        # Implementing solutions that are scalable or adjustable to the degree of action required.
    17: "Moving to a New Dimension",
        # Transitioning to new paradigms or architectures, like moving from monolithic to microservices.
    18: "Mechanical Vibration",
        # Implementing monitoring and alerting to detect and respond to system anomalies.
    19: "Periodic Action",
        # Scheduling periodic tasks or maintenance activities to ensure system health.
    20: "Continuity of Useful Action",
        # Ensuring continuous delivery, integration, and deployment for ongoing value delivery.
    21: "Skipping",
        # Bypassing or shortcutting processes to achieve faster results.
    22: "Blessing in Disguise",
        # Leveraging failures or unexpected events as learning opportunities.
    23: "Feedback",
        # Implementing feedback loops for continuous improvement.
    24: "Intermediary",
        # Utilizing intermediary services or APIs to facilitate interactions between components.
    25: "Self-Service",
        # Implementing self-service options for users to reduce operational overhead.
    26: "Copying",
        # Replicating successful solutions or practices across different parts of the system.
    27: "Cheap Short-Living",
        # Utilizing disposable resources or temporary solutions for short-term needs.
    28: "Replacement of Mechanical System",
        # Automating manual processes to improve efficiency and consistency.
    29: "Pneumatics and Hydraulics",
        # This might not have a direct analogy but could be viewed as streamlining data flow.
    30: "Flexible Shells and Thin Films",
        # Implementing flexible interfaces or abstraction layers to accommodate change.
    31: "Porosity",
        # Introducing modularity or openness in the system to allow for extensibility.
    32: "Color Changes",
        # Utilizing meaningful visual indicators or logging to convey system status.
    33: "Homogeneity",
        # Standardizing technologies or practices to reduce complexity.
    34: "Discarding and Recovering",
        # Implementing robust backup and recovery solutions.
    35: "Parameter Changes",
        # Allowing for configurability to adapt to varying requirements.
    36: "Phase Transition",
        # Managing transitions between different states or versions of the software.
    37: "Thermal Expansion",
        # This might be analogous to managing system load and ensuring scalability.
    38: "Strong Oxidants",
        # Identifying and removing impediments or 'corrosive' practices.
    39: "Inert Atmosphere",
        # Maintaining a stable and consistent operational environment.
    40: "Composite Materials",
        # Integrating diverse technologies or practices to create a more robust solution.
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
    # Регулярное выражение для поиска Python List в строке
    pattern = re.compile(r'(\[\s*(?:(?:\d+|"[^"]*"|\'[^\']*\')(?:\s*,\s*(?:\d+|"[^"]*"|\'[^\']*\'))*)?\s*\])')
    match = pattern.search(s)
    if match:
        # Извлечение и преобразование Python List из строки
        python_list_str = match.group(1)
        try:
            # Преобразование строки в фактический Python List с помощью модуля ast
            python_list = ast.literal_eval(python_list_str)
            return python_list
        except (ValueError, SyntaxError):
            return None
    return None

def get_request(content, prompt, check_function=None, temp=0.5):
    try:
        for i in range(10):
            completion = openai.ChatCompletion.create(
                model = GPT_MODEL,
                messages = [
                    {"role": "system", "content": content},
                    {"role": "user", "content": prompt}
                ],
                temperature = temp,
            )
            answer = completion.choices[0].message.content
            answer = summarize(answer, max_num=5000)

            if check_function is not None:
                answer = check_function(answer)
                if answer is not None:
                    return answer
            else:
                return answer
    except Exception as e:
        print(f"An error from GPT occurred: {e}")
    
    print("Error: wrong response")
    print(prompt)
    print('===============')
    #raise Exception("Invalid response from ChatGPT")
    return None

### 1. Анализ входных данных пользователя и формулирование проблемы
def define_problem_statement(user_input):
    user_input = summarize(user_input)
    prompt=f"Based on the provided description, please define and formulate the problem and identify key parameters: {user_input}"
    res = get_request(triz_content_common, prompt)
    return res

def extract_problems(problem_statement):
    problem_statement = summarize(problem_statement)
    prompt=f"Extract the problem from the following problem statement: {problem_statement}"
    res = get_request(triz_content_common, prompt)
    return res

### 2. Идентификация противоречий в проблемном заявлении
def analyze_conflicts(problem_statement):
    # Сначала разберите проблемное заявление на составные части, чтобы выявить ключевые параметры и требования.
    # Это может включать в себя текстовый анализ, анализ данных или даже консультации с экспертами.
    #parameters_and_requirements = extract_parameters_and_requirements(problem_statement)

    # Идентификация технических противоречий:
    # Технические противоречия возникают, когда улучшение одного параметра ведет к ухудшению другого.
    technical_conflicts = identify_technical_conflicts(problem_statement)

    # Идентификация физических противоречий:
    # Физические противоречия возникают, когда один и тот же параметр должен иметь противоположные значения.
    physical_conflicts = identify_physical_conflicts(problem_statement)

    # Сбор и возврат результатов анализа
    conflicts = {
        'technical_conflicts': technical_conflicts,
        'physical_conflicts': physical_conflicts
    }

    conflicts = add_conflict_description(problem_statement, conflicts)
    return conflicts

def extract_parameters_and_requirements(problem_statement):
    problem_statement = summarize(problem_statement)
    prompt=f"Extract the parameters and requirements from the following problem statement: {problem_statement}"
    res = get_request(triz_content_common, prompt)
    return res

def identify_technical_conflicts(problem_statement):
    problem_statement = summarize(problem_statement)
    prompt=f"Based on '{problem_statement}', identify technical conflicts, select up to {MAX_NUM_TECH_CONFLICTS} most suitable options, and write them to a Python List. Don't write anything else, just Python List"
    res = get_request(triz_content_common, prompt, extract_python_list)
    return res

def identify_physical_conflicts(problem_statement):
    problem_statement = summarize(problem_statement)
    prompt=f"Based on '{problem_statement}', identify physical conflicts, select up to {MAX_NUM_PHIS_CONFLICTS} most suitable options, and write them to a Python List. Don't write anything else, just Python List"
    res = get_request(triz_content_common, prompt, extract_python_list)
    return res

def add_conflict_description(problem_statement, identified_conflicts):
    technical_conflicts = []
    physical_conflicts = []

    for conflict in identified_conflicts['technical_conflicts']:
        prompt=f"Based on '{problem_statement}', write short description to '{conflict}'. Don't write anything more, just text of description"
        res = get_request(triz_content_common, prompt)
        technical_conflicts.append(conflict + ": " + res)

    for conflict in identified_conflicts['physical_conflicts']:
        prompt=f"Based on '{problem_statement}', write short description to '{conflict}'. Don't write anything more, just text of description"
        res = get_request(triz_content_common, prompt)
        physical_conflicts.append(conflict + ": " + res)
  
    conflicts = {
        'technical_conflicts': technical_conflicts,
        'physical_conflicts': physical_conflicts
    }
    return conflicts

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

    conflict = summarize(conflict)
    prompt=f"Based on the analysis of technical conflict: '{conflict}', please suggest the most suitable numbers (up to {MAX_NUM_PRINC}) of TRIZ principles from '{TRIZ_principles}' to address this conflict. Don't write anything else, just Python List"
    res = get_request(triz_content_common, prompt, extract_python_list)
    for item in res:
        principle_description.append(TRIZ_principles[int(item)])
    return principle_description

def generate_solution_based_on_principle(principle, conflict):
    # Генерация решения на основе выбранного принципа и конфликта
    principle = summarize(principle)
    conflict = summarize(conflict)
    prompt=f"Given the selected TRIZ principle: '{principle}', and the identified technical conflict: '{conflict}', please generate a solution to resolve the conflict. Provide a detailed explanation of how the principle can be applied to address the issues and achieve a resolution."
    res = get_request(triz_content_common, prompt)
    return res

def choose_standard_solution_based_on_conflict(conflict):
    # Примерный алгоритм выбора Стандартного Решения на основе анализа конфликта
    standard_solution_description = []

    conflict = summarize(conflict)
    prompt=f"Based on the analysis of physical conflict: '{conflict}', please suggest the most suitable numbers (up to {MAX_NUM_STAND}) of TRIZ standard solutions from '{TRIZ_standard_solutions}' to address this conflict. Don't write anything else, just Python List"
    res = get_request(triz_content_common, prompt, extract_python_list)
    for item in res:
        standard_solution_description.append(TRIZ_standard_solutions[int(item)])
    return standard_solution_description

def generate_solution_based_on_standard_solution(standard_solution, conflict):
    # Генерация решения на основе выбранного Стандартного Решения и конфликта
    standard_solution = summarize(standard_solution)
    conflict = summarize(conflict)
    prompt=f"Given the selected TRIZ standard solution: '{standard_solution}', and the identified physical conflict: '{conflict}', please generate a solution to resolve the conflict. Provide a detailed explanation of how the standard solution can be applied to address the issues and achieve a resolution."
    res = get_request(triz_content_common, prompt)
    return res

### 4. Анализ трендов и законов развития технических систем в области проблемы
### https://altshuller.ru/triz/zrts1.asp
def apply_technical_system_evolution_laws(problem_statement):
    analysis_results = {}
    problem_statement = summarize(problem_statement)
    for law_number, law_name in TRIZ_laws_of_technical_system_evolution.items():
        # Analyze the problem_statement with respect to the current law.
        prompt=f"Analyze the current state of my system described as follows: '{problem_statement}' based on the law of technical system evolution: {law_name}"
        res = get_request(triz_content_common, prompt)
        analysis_results[law_name] = res

    return analysis_results

### 5. Оценка потенциальных решений с точки зрения их функциональности и стоимости
def perform_functional_cost_analysis(potential_solutions):
    analyzed_solutions = []

    for solution in potential_solutions:
        solution = summarize(solution)
        prompt = f"""Evaluate the following proposed solution in terms of its Functionality score (0-100) and Cost score (0-100): '{solution}'. Don't write anything more than Functionality, Cost. Write the answer in the form:
        '- Functionality: estimated value
        - Cost: estimated value'
        """

        evaluation = get_request(triz_content_common, prompt, extract_scores)
        if (evaluation == None):
          continue
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
def generate_ideas(evolution_analysis, functional_cost_analysis_result):
    # Prepare a list to collect new ideas
    new_ideas = []

    # Analyze the evolution analysis results to identify opportunities or challenges
    for law_name, analysis_result in evolution_analysis.items():
        # This is a simplified example; you might have more complex analysis logic here
        if 'opportunity' in analysis_result:
            analysis_result = summarize(analysis_result)
            prompt = f"Based on the technical system evolution analysis, provide one innovative solution or improvement to address the identified problem. Here's the summary of the analysis: '{analysis_result}'. Please ensure that the proposed idea aligns with the observed evolution trends and laws, and elaborate on how this idea can mitigate the identified problem."
            res = get_request(triz_content_common, prompt)
            new_ideas.append(res)

    # Analyze the functional cost analysis results to identify high-potential solutions
    for analyzed_solution in functional_cost_analysis_result:
        # For simplicity, let's consider solutions with a balance score of zero as high-potential
        if analyzed_solution['balance_score'] >= 0:
            analyzed_solution['solution'] = summarize(analyzed_solution['solution'])
            formatted_analysis_results = '\n'.join(
                [f"- Solution: {analyzed_solution['solution']}, Functionality Score: {analyzed_solution['functionality_score']}, Cost Score: {analyzed_solution['cost_score']}, Balance Score: {analyzed_solution['balance_score']}" 
                for result in functional_cost_analysis_result]
            )
            prompt = f"Given the Functional Cost Analysis, the solutions evaluated include: '{formatted_analysis_results}'. In light of this analysis, propose one innovative idea to enhance functionality while either maintaining or lowering the cost. Furthermore, elaborate on any additional factors that should be contemplated to forge a balanced solution."
            res = get_request(triz_content_common, prompt)
            new_ideas.append(res)

    # Additional idea generation logic can go here...
    # For example, you might identify and resolve contradictions, apply inventive principles, etc.

    return new_ideas

### 7. Разработка механизмов для сбора обратной связи от пользователей или экспертов по предложенным идеям
def gather_feedback(new_ideas, problem_statement):
    prompt = f"Choose one best idea from the list '{new_ideas}' to solve problem '{problem_statement}'. Only idea"
    res = get_request('You are professional technical writer', prompt)
    return res

### 8. Repeating
def new_problem_statement(problem_statement, topic):
    prompt = f"Based on '{problem_statement}' and the proposed solution '{topic}', write what technological problem has not yet been solved for the successful implementation of this solution. Write briefly up to 15 words. Only problem"
    res = get_request('You are professional technical writer', prompt)
    return res

### 9. Report
def get_report(feedback):
    return report

def get_solutions_summary(feedback):
    summary = []
    for txt in feedback:
        res = get_summary(txt, max_num = 100)
        summary.append(res)
    return summary

### Utils
def get_summary(text, max_num = 10000, prompt = None, content = None):
    if (prompt == None):
        prompt = f"Given the selected text: '{text}', write a summary in {max_num} words"
    if (content == None):
        content = 'You are professional technical writer'
    res = get_request(content, prompt)
    return res

def get_token_num(text):
    word_list = text.split()
    word_count = len(word_list)
    return word_count

def summarize(text, max_num=10000):
    num = get_token_num(text)
    if (num > max_num):
        res = get_summary(text, max_num)
    else:
        res = text
    return res

def naming_ideas(summary):
    prompt = f"Analyze the ideas in the list '{summary}', come up with a name for each idea, and present them as a Python List"
    res = get_request('You are professional technical writer', prompt, extract_python_list)
    return res

### Запуск
user_input = "We need to come up with an effective way to generate energy that will be many times cheaper and easier to implement than all current methods."

problem_statement = define_problem_statement(user_input)
original_problem = extract_problems(problem_statement)

for _ in range(5):
    print("Log: 1.", problem_statement)
    conflicts = analyze_conflicts(problem_statement)
    print("Log: 2.", len(conflicts['technical_conflicts']), len(conflicts['physical_conflicts']))
    solutions = apply_standard_solutions(conflicts)
    print("Log: 3.", len(solutions))
    evolution_analysis = apply_technical_system_evolution_laws(problem_statement)
    print("Log: 4.", len(evolution_analysis))
    functional_cost_analysis_result = perform_functional_cost_analysis(solutions)
    print("Log: 5.", len(functional_cost_analysis_result))
    new_ideas = generate_ideas(evolution_analysis, functional_cost_analysis_result)
    print("Log: 6.", len(new_ideas))
    names = naming_ideas(new_ideas)
    print(names)
    print("===============")
    feedback = gather_feedback(new_ideas, problem_statement)
    print("Log: 7.")
    print(feedback)
    print("===============")
    new_problem = new_problem_statement(original_problem, feedback)
    problem_statement = define_problem_statement(original_problem + ' To do this you need to solve the problem:' + new_problem)
    print("Log: 8.")

for idea in new_ideas:
    print(idea)
    print("===============")