import re
import ast
import time
import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

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

TRIZ_principles_d = {
    3: "Local Quality",
    8: "Anti-Weight",
    14: "Spheroidality",
    17: "Moving to a New Dimension",
    26: "Copying"
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
    1: "Построение и разрушение вепольный систем. Синтез веполей. Синтез веполя",
    2: "Построение и разрушение вепольный систем. Синтез веполей. Переход к внутреннему комплексному веполю",
    3: "Построение и разрушение вепольный систем. Синтез веполей. Переход к внешнему комплексному веполю",
    4: "Построение и разрушение вепольный систем. Синтез веполей. Переход к веполю на внешней среде",
    5: "Построение и разрушение вепольный систем. Синтез веполей. Переход к веполю на внешней среде с добавками",
    6: "Построение и разрушение вепольный систем. Синтез веполей. Минимальный режим действия на вещество",
    7: "Построение и разрушение вепольный систем. Синтез веполей. Максимальный режим действия на вещество",
    8: "Построение и разрушение вепольный систем. Синтез веполей. Избирательно-максимальный режим",
    9: "Построение и разрушение вепольный систем. Разрушение веполей. Устранение вредной связи введением постороннего вещества",
    10: "Построение и разрушение вепольный систем. Разрушение веполей. Устранение вредной связи видоизменением имеющихся веществ",
    11: "Построение и разрушение вепольный систем. Разрушение веполей. Оттягивание вредного действия поля",
    12: "Построение и разрушение вепольный систем. Разрушение веполей. Противодействие вредным связям с помощью поля",
    13: "Построение и разрушение вепольный систем. Разрушение веполей. 'Отключение' магнитных связей",
    14: "Развитие вепольных систем. Переход к сложным веполям. Переход к цепному веполю",
    15: "Развитие вепольных систем. Переход к сложным веполям. Переход к двойному веполю",
    16: "Развитие вепольных систем. Форсирование веполей. Переход к более управляемым полям",
    17: "Развитие вепольных систем. Форсирование веполей. Дробление инструмента",
    18: "Развитие вепольных систем. Форсирование веполей. Переход к капиллярно-пористому веществу",
    19: "Развитие вепольных систем. Форсирование веполей. Динамизация веполя",
    20: "Развитие вепольных систем. Форсирование веполей. Структуризация поля",
    21: "Развитие вепольных систем. Форсирование веполей. Структуризация вещества",
    22: "Развитие вепольных систем. Форсирование согласования ритмики. Согласование ритмики поля и изделия (или инструмента)",
    23: "Развитие вепольных систем. Форсирование согласования ритмики. Согласование ритмики используемых полей",
    24: "Развитие вепольных систем. Форсирование согласования ритмики. Согласование несовместимых или ранее независимых действий",
    25: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Переход к 'протофеполю'",
    26: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Переход к феполю",
    27: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Использование магнитной жидкости",
    28: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Использование капиллярно-пористой структуры феполя",
    29: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Переход к комплексному феполю",
    30: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Переход к феполю на внешней среде",
    31: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Использование физэффектов",
    32: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Динамизация феполя",
    33: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Структуризация феполя",
    34: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Согласование ритмики в феполе",
    35: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Переход к эполю - веполю с взаимодействующими токами",
    36: "Развитие вепольных систем. Феполи (Комплексно-форсированные веполи). Использование электрореологической жидкости",
    37: "Переход к надсистеме и на микроуровень. Переход к бисистемам и полисистемам. Переход к бисистемам и полисистемам",
    38: "Переход к надсистеме и на микроуровень. Переход к бисистемам и полисистемам. Развитие связей в бисистемах и полисистемах",
    39: "Переход к надсистеме и на микроуровень. Переход к бисистемам и полисистемам. Увеличение различия между элементами бисистем и полисистем",
    40: "Переход к надсистеме и на микроуровень. Переход к бисистемам и полисистемам. Свертывание бисистем и полисистем",
    41: "Переход к надсистеме и на микроуровень. Переход к бисистемам и полисистемам. Несовместимые свойства системы и ее частей",
    42: "Переход к надсистеме и на микроуровень. Переход на микроуровень. Переход на микроуровень",
    43: "Стандарты на обнаружение и измерение систем. Обходные пути. Вместо обнаружения и измерения - изменение системы",
    44: "Стандарты на обнаружение и измерение систем. Обходные пути. Использование копий",
    45: "Стандарты на обнаружение и измерение систем. Обходные пути. Последовательное обнаружение изменений",
    46: "Стандарты на обнаружение и измерение систем. Синтез измерительных систем. Синтез измерительного веполя",
    47: "Стандарты на обнаружение и измерение систем. Синтез измерительных систем. Переход к комплексному измерительному веполю",
    48: "Стандарты на обнаружение и измерение систем. Синтез измерительных систем. Переход к измерительному веполю на внешней среде",
    49: "Стандарты на обнаружение и измерение систем. Синтез измерительных систем. Получение добавок во внешней среде",
    50: "Стандарты на обнаружение и измерение систем. Форсирование измерительных веполей. Использование физэффектов",
    51: "Стандарты на обнаружение и измерение систем. Форсирование измерительных веполей. Использование резонанса контролируемого объекта",
    52: "Стандарты на обнаружение и измерение систем. Форсирование измерительных веполей. Использование резонанса присоединенного объекта",
    53: "Стандарты на обнаружение и измерение систем. Переход к фепольным измерительным системам. Переход к измерительному 'протофеполю'",
    54: "Стандарты на обнаружение и измерение систем. Переход к фепольным измерительным системам. Переход к измерительному феполю",
    55: "Стандарты на обнаружение и измерение систем. Переход к фепольным измерительным системам. Переход к комплексному измерительному феполю",
    56: "Стандарты на обнаружение и измерение систем. Переход к фепольным измерительным системам. Переход к измерительному феполю на внешней среде",
    57: "Стандарты на обнаружение и измерение систем. Переход к фепольным измерительным системам. Использование физэффектов",
    58: "Стандарты на обнаружение и измерение систем. Направление развития измерительных систем. Переход к измерительным бисистемам и полисистемам",
    59: "Стандарты на обнаружение и измерение систем. Направление развития измерительных систем. Переход к измерению производных",
    60: "Стандарты на применение стандартов. Особенности введения веществ. Обходные пути",
    61: "Стандарты на применение стандартов. Особенности введения веществ. Разделение изделия на взаимодействующие части",
    62: "Стандарты на применение стандартов. Особенности введения веществ. Самоустранение отработанных веществ",
    63: "Стандарты на применение стандартов. Особенности введения веществ. Использование надувных конструкций и пены",
    64: "Стандарты на применение стандартов. Введение полей. Использование поля по совместительству",
    65: "Стандарты на применение стандартов. Введение полей. Использование поля внешней среды",
    66: "Стандарты на применение стандартов. Введение полей. Использование веществ-источников полей",
    67: "Стандарты на применение стандартов. Использование фазовых переходов. Замена фазового состояния вещества",
    68: "Стандарты на применение стандартов. Использование фазовых переходов. 'Двойственное' фазовое состояние вещества",
    69: "Стандарты на применение стандартов. Использование фазовых переходов. Использование явлений, сопутствующих фазовому переходу",
    70: "Стандарты на применение стандартов. Использование фазовых переходов. Переход к двухфазному состоянию вещества",
    71: "Стандарты на применение стандартов. Использование фазовых переходов. Использование взаимодействия между частями (фазами) системы",
    72: "Стандарты на применение стандартов. Особенности применения физэффектов. Использование обратимых физических превращений",
    73: "Стандарты на применение стандартов. Особенности применения физэффектов. Усиление поля на выходе",
    74: "Стандарты на применение стандартов. Экспериментальные стандарты. Получение частиц вещества разложением",
    75: "Стандарты на применение стандартов. Экспериментальные стандарты. Получение частиц вещества объединением",
    76: "Стандарты на применение стандартов. Экспериментальные стандарты. Простейшие способы получения частиц вещества"
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

evaluation_criteria = [
    "Technical Feasibility: How technically achievable is the idea considering current technologies and available resources?",
    "Economic Viability: What is the cost of implementing the idea and what are the potential economic benefits?",
    "Innovativeness: How novel is the idea and how does it differ from existing solutions in the market?",
    "Market Potential: What is the size of the potential market or audience for this idea? How quickly can the idea be introduced to the market?",
    "Environmental Impact: What are the potential environmental consequences of implementing the idea? Will it reduce the impact on the environment?",
    "Social Significance: To what extent can the idea positively influence society, improve the quality of life, or address social issues?",
    "Risks: What potential risks are associated with implementing the idea, and how likely are they to occur?",
    "Implementation Time: Over what period can the idea be fully realized and implemented?",
    "Integration with Existing Systems: How easily can the idea be integrated into existing systems or infrastructure?",
    "Scalability: How easily can the idea be scaled or adapted for different conditions or markets?"
]


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

def extract_criteria_scores(s):
    criteria_scores = []
    criterias = ["Technical Feasibility", "Economic Viability", "Innovativeness", "Market Potential", "Environmental Impact", "Social Significance", "Risks", "Implementation Time", "Integration with Existing Systems", "Scalability"]
    try:
        for criteria in criterias:
            match = re.search(rf"{criteria}: (\d+)", s)
            if match:
                score = int(match.group(1))
                score = max(0, min(score, 1))
                criteria_scores.append(score)
            else:
                return None
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

def get_request(content, prompt, gpt_model = "gpt-3.5-turbo-1106", check_function=None, temp=0.5):
    for i in range(5):
        try:
            #start_time = time.time()
            #print("start")
            completion = openai.ChatCompletion.create(
                model = gpt_model, # gpt-3.5-turbo-16k gpt-3.5-turbo gpt-3.5-turbo-1106 gpt-4 gpt-4-32k gpt-4-1106-preview
                messages = [
                    {"role": "system", "content": content},
                    {"role": "user", "content": prompt}
                ],
                temperature = temp,
                request_timeout = 30,
            )
            #end_time = time.time()
            #print("end", end_time - start_time)
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
            #time.sleep(30)
    
    print("Error: wrong response")
    print(prompt)
    print('===============')
    #raise Exception("Invalid response from ChatGPT")
    return None

### 1. Анализ входных данных пользователя и формулирование проблемы
def describe_input(text):
    prompt=f"Analyze and write a more detailed description of the user's problem in 100-300 words: {text}"
    res = get_request(triz_content_common, prompt)
    return res

def define_problem_statement(text):
    text = summarize(text)
    prompt=f"Based on the provided description, please define and formulate the problem and identify key parameters: {text}"
    res = get_request(triz_content_common, prompt)
    return res

def extract_problems(text):
    text = summarize(text)
    prompt=f"Extract the problem from the following problem statement: {text}"
    res = get_request(triz_content_common, prompt)
    return res

def define_problem(text):
    text = summarize(text)
    prompt=f"Based on the provided description, please define and formulate the problem: '{text}'. Write briefly up to 50 words. Only problem"
    res = get_request(triz_content_common, prompt)
    return res

def define_key_parameters(text):
    text = summarize(text)
    prompt=f"Based on the provided description, please identify key parameters: {text}"
    res = get_request(triz_content_common, prompt)
    return res

def transfer_to_abstract(text):
    text = summarize(text)
    prompt=f"Transfer the problem to the abstract domain: '{text}'. Write only the formulation of the problem"
    res = get_request(triz_content_common, prompt, gpt_model="gpt-4-1106-preview")
    return res

def transfer_from_abstract(problem, solutions):
    ideas_from_abstract = []
    problem = summarize(problem)

    for solution in solutions:
        prompt=f"I have an abstract solution: '{solution}', apply it to the problem: {problem}. Write only the formulation of the solution"
        res = get_request(triz_content_common, prompt)
        ideas_from_abstract.append(res)
    
    return ideas_from_abstract

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
    physical_conflicts = []#identify_physical_conflicts(problem_statement)

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
    res = get_request(triz_content_common, prompt, check_function=extract_python_list)
    return res

def identify_physical_conflicts(problem_statement):
    problem_statement = summarize(problem_statement)
    prompt=f"Based on '{problem_statement}', identify physical conflicts, select up to {MAX_NUM_PHIS_CONFLICTS} most suitable options, and write them to a Python List. Don't write anything else, just Python List"
    res = get_request(triz_content_common, prompt, check_function=extract_python_list)
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
    
    for conflict in identified_conflicts['technical_conflicts']:
        # Применение Стандартных Решений ТРИЗ к техническим противоречиям
        standard_solution_descriptions = choose_standard_solution_based_on_conflict(conflict)
        for standard in standard_solution_descriptions:
            solution = generate_solution_based_on_standard_solution(standard, conflict)
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
    res = get_request(triz_content_common, prompt, check_function=extract_python_list)
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
    res = get_request(triz_content_common, prompt, check_function=extract_python_list)
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

def generate_solution(text):
    text = summarize(text)
    possible_solutions = []

    for key, value in TRIZ_principles.items():
        prompt=f"Given the selected TRIZ principle: '{value}', and the problem: '{text}', please generate 1-2 best solutions to resolve the problem. Do not offer solutions based on intelligent systems, Artificial Intelligence, Internet of things, sensor monitoring and any other smart systems. Write solutions into Python List. Don't write anything else, just Python List"
        res = get_request(triz_content_common, prompt, check_function=extract_python_list, gpt_model="gpt-4-1106-preview")
        if (res != None):
            for item in res:
                possible_solutions.append(item)

    #for key, value in TRIZ_standard_solutions.items():
    #    prompt=f"Given the selected TRIZ standard solution: '{value}', and the problem: '{text}', please generate 1-2 best solutions to resolve the problem. Do not offer solutions based on intelligent systems, Artificial Intelligence, Internet of things, sensor monitoring and any other smart systems. Write solutions into Python List. Don't write anything else, just Python List"
    #    res = get_request(triz_content_common, prompt, check_function=extract_python_list, gpt_model="gpt-4-1106-preview")
    #    if (res != None):
    #        for item in res:
    #            possible_solutions.append(item)
    
    return possible_solutions

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
        prompt = f"""Evaluate the following proposed solution in terms of its Functionality score (0-1) and Cost score (0-1): '{solution}'. Don't write anything more than Functionality, Cost. Write the answer in the form:
        '- Functionality: estimated value
        - Cost: estimated value'
        """

        evaluation = get_request(triz_content_common, prompt, check_function=extract_scores)
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

def evaluate_solutions_old(problem, solutions):
    evaluated_solutions = []

    for solution in solutions:
        solution = summarize(solution)
        prompt = f"To solve the problem: '{problem}', a solution is proposed: '{solution}', give a rating of the solution from 0 to 1 for each of the criteria: '{evaluation_criteria}'. Represent the result as a Python List in the same order. Only Python List with 10 numbers if rating"
        res = get_request(triz_content_common, prompt, check_function=extract_python_list)
        if (res == None or (len(res) != len(evaluation_criteria))):
            continue
        evaluated_solutions.append((solution, res))

    return evaluated_solutions

def evaluate_solutions(solutions):
    evaluated_solutions = []

    for solution in solutions:
        func = None
        cost = None
        solution = summarize(solution)
        
        prompt = f"Write the field of activity in which the employee who formulated this solution works? '{solution}'. Don't write anything else, just the field of activity"
        field = get_request(triz_content_common, prompt)
        field_content = f"You are a certified professional in {field}"

        # cost estimation
        prompt = f"I have this solution: '{solution}'. Write down briefly what criteria can be used to estimate the cost of implementing this solution. Don't write anything else, just a list"
        criteria = get_request(field_content, prompt)
        for i in range(5):
            prompt = f"I have this solution: '{solution}'. Estimate the approximate rough cost of implementing the solution in dollars for each criterion from the list below: '{criteria}'. Don't write anything else, just criteria and evaluation"
            estimation = get_request(field_content, prompt)
            prompt = f"Does this answer include a dollar estimate for the cost of the solution? '{estimation}'. Just write yes or no"
            answer = get_request(field_content, prompt)
            pattern = r'\byes\b'
            answer_bool = bool(re.search(pattern, answer, re.IGNORECASE))
            if (answer_bool == True):
                prompt = f"Write down the maximum cost of the project and write the result as a number. Do not write anything else, just the rating as a number without separators, signs or text. '{estimation}'. "
                score_str = get_request(triz_content_common, prompt)
                score_int = safe_int(score_str)
                if (score_int != None and score_int > 100):
                    cost = score_int
                    break
        
        # functionality score
        prompt = f"I have this solution: '{solution}'. Write down briefly what criteria can be used to estimate the functionality score of this solution. Don't write anything else, just a list"
        criteria = get_request(field_content, prompt)
        for i in range(5):
            prompt = f"I have this solution: '{solution}'. Please rate the functionality (from 0 to 1000) of the solution for each criterion in the list below: '{criteria}'. Don't write anything else, just criterion and score"
            estimation = get_request(field_content, prompt)
            prompt = f"Is there a score for each criterion in the answer? '{estimation}'. Just write yes or no"
            answer = get_request(field_content, prompt)
            pattern = r'\byes\b'
            answer_bool = bool(re.search(pattern, answer, re.IGNORECASE))
            if (answer_bool == True):
                prompt = f"Write down the average score for the project's functionality and write the result as a number. Do not write anything else, just the rating as a number without separators, signs or text. '{estimation}'. "
                score_str = get_request(triz_content_common, prompt)
                score_int = safe_int(score_str)
                if (score_int != None and score_int > 100):
                    func = score_int
                    break

        if (func != None and cost != None):
            evaluated_solutions.append((solution, func, cost))

    return evaluated_solutions

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

def choose_ideas(evaluated_solutions, num):
    max_value_1 = max(evaluated_solutions, key=lambda x: x[1])[1]
    max_value_2 = max(evaluated_solutions, key=lambda x: x[2])[2]
    evaluated_solutions = [(item[0], (normalize(item[1], 0, max(1, max_value_1))) * (1 - normalize(item[2], 0, max_value_2))) for item in evaluated_solutions]
    evaluated_solutions = sorted(evaluated_solutions, key=lambda x: x[1], reverse=True)
    evaluated_solutions = evaluated_solutions[:num]
    
    return evaluated_solutions

def choose_best_idea(ideas):
    ideas = [item[0] for item in evaluated_solutions]
    prompt = f"which of these ideas is the most reasonable: '{ideas}'. Only idea"
    res = get_request('You are professional technical writer', prompt)
    return res

### 7. Разработка механизмов для сбора обратной связи от пользователей или экспертов по предложенным идеям
def gather_feedback(new_ideas, problem_statement):
    prompt = f"Choose one best idea from the list '{new_ideas}' to solve problem '{problem_statement}'. Only idea"
    res = get_request('You are professional technical writer', prompt)
    return res

### 8. Repeating
def deeper_problem(problem):
    prompt = f"Write what the problem might be when implementing the task: '{problem}'. Just write the problem statement"
    res = get_request('You are professional technical writer', prompt)
    return res

### 9. Report
def get_report(feedback):
    pass

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

def summarize(input_data, max_num=10000):
    if isinstance(input_data, str):
        return _summarize_text(input_data, max_num)
    elif isinstance(input_data, list):
        return [_summarize_text(text, max_num) for text in input_data]
    else:
        raise ValueError("Unsupported input type. Only string or list of strings are allowed.")

def _summarize_text(text, max_num):
    num = get_token_num(text)
    if num > max_num:
        return get_summary(text, max_num)
    else:
        return text

def naming_ideas(summary):
    prompt = f"Analyze the ideas in the list '{summary}', come up with a name for each idea, and present them as a Python List"
    res = get_request('You are professional technical writer', prompt, check_function=extract_python_list)
    return res

def safe_int(s):
    try:
        cleaned_s = re.sub(r'\D', '', s)
        return int(cleaned_s)
    except ValueError:
        return None

def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value) if max_value != min_value else 0

### Запуск
input = """ABOUT THE CHALLENGE
Each year, over 1 billion tires around the world reach their End of Life. These tires are not just waste that it is polluting the environment, but a gold-mine of reusable materials. However, tires are made of several components (rubber, metal, polymers, textile fabrics, etc.) that are linked via chemical reactions occurring during the vulcanization process. These components must first be separated and sorted, before devulcanization of the rubber can take place.
THE BRIEF
There is a dire need for a modular tire that allows easy disassembly and reassembly of components to ensure their re-usability, thereby closing the circularity loop for End-of-Life tires. Continental, through this INAM Open Innovation Challenge, is looking for solutions to the challenges to develop the world’s first modular and circular tire.
Separating the component materials at the tire’s end of life is necessary before recycling to ensure that the reclaimed material is of high quality. This is highly challenging especially in the case of textile fabrics as the sulphur links formed during vulcanization process are not reversable.
Our goal is to find a new chemical and/or mechanical link that is able to provide reversible bonding (a bonding that endures under normal tire service conditions, but can be broken on purpose under certain conditions), maintaining the original physical characteristics. Solutions that enable separation of the current bonding system, are also welcomed. Solutions must not compromise the strength and endurance of the tire.
Alternatively, recycling processes that do not require separation at all may also be considered, provided that the recycled material can match the properties of the original material."""

#problem_description = describe_input(input)
#problem = extract_problems(problem_description)
#original_problem = problem

report = []
for i in range(2):
    problem_description = describe_input(input)
    print(f"=========== {i}-1")
    problem = extract_problems(problem_description)
    print(f"=========== {i}-2")
    abstract_problem = transfer_to_abstract(problem)
    print(f"=========== {i}-3")
    solutions = generate_solution(abstract_problem)
    print(f"=========== {i}-4")
    ideas_from_abstract = transfer_from_abstract(problem, solutions)
    #ideas_from_abstract = [
    #    'Formulation of the solution: Implement a parachute system on ships to increase air resistance and decelerate the ship quickly and efficiently, thereby reducing the braking distance.',
    #    'Formulation of Solution: Implement a hydraulic braking system on ships that can generate a powerful force to rapidly decelerate the vessel, thereby reducing the braking distance.',
    #    'Abstract Solution: Implementing parachutes or airbags to create air resistance and decelerate the ship, thereby reducing the braking distance.',
    #    'Formulation of the solution: Implement a system of advanced friction pads or brake shoes specifically designed for ships, which gradually reduces the speed and brings the large mass of the ship to a stop in a shorter braking distance.',
    #    'Formulation of the solution: Implement a spheroidal shape, such as a sphere or an ellipsoid, for the large mass of ships to decrease air resistance and improve aerodynamics during deceleration, thereby reducing the braking distance for ships.',
    #    'Formulation of the solution: Implement a magnetic braking system using strong magnets to rapidly decelerate ships, thereby reducing their braking distance.',
    #    'Formulation of the solution: Develop a pneumatic braking system for ships that utilizes compressed air to generate resistance and decelerate the vessel, thereby reducing the braking distance required for stopping.',
    #    "Implement a mechanical braking system for ships that utilizes a series of copied and synchronized mechanisms to distribute the braking force evenly across the entire ship's mass, thereby reducing the braking distance required for deceleration.",
    #    'Formulation of the solution: \nDevelop a network of interconnected copied and synchronized hydraulic or pneumatic dampers that can absorb and dissipate the kinetic energy of the ship, enabling rapid deceleration and minimizing the required space for braking.'
    #]
    print(f"=========== {i}-5")
    evaluated_solutions = evaluate_solutions(ideas_from_abstract)
    print(f"=========== {i}-6")
    best_ideas = choose_ideas(evaluated_solutions, 20)
    print(f"=========== {i}-7")
    print(best_ideas)
    best_idea = choose_best_idea(best_ideas)
    print(f"=========== {i}-8")
    report.append(best_idea)
    input = deeper_problem(best_idea)
    print(f"=========== {i}-9")

print('===========')
print(report)
print('===========')