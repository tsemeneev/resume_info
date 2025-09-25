import pandas as pd

def create_sample_excel():
    """Создает пример Excel файла с резюме для тестирования"""
    
    # Пример данных
    data = {
        'Номер': [1, 2, 3],
        'Ссылка': [
            'https://hh.ru/resume/a7360168000b48809c000022b2643576416445',
            'https://hh.ru/resume/b8471279111c59910d111133c3754687527556', 
            'https://hh.ru/resume/c9582380222d60021e222244d4865798638667'
        ],
        'Комментарий': ['Кандидат 1', 'Кандидат 2', 'Кандидат 3']
    }
    
    df = pd.DataFrame(data)
    df.to_excel('sample_resumes.xlsx', index=False)
    print("Создан файл sample_resumes.xlsx для тестирования")

if __name__ == "__main__":
    create_sample_excel()