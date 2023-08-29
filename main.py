import streamlit as st
import pandas as pd
from scipy import stats
import plotly.express as px

# Загрузка датасета
st.title('Исследование данных и проверка гипотез')
uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write('Первые строки датасета:')
    st.write(data.head())

    # Выбор переменных
    st.subheader('Выберите переменные для исследования')
    column1 = st.selectbox('Первая переменная:', data.columns)
    column2 = st.selectbox('Вторая переменная:', data.columns)

    # Визуализация распределения
    st.subheader('Визуализация распределения переменных')
    if data[column1].dtype == 'object':
        fig = px.pie(data, names=column1, title=f'Распределение {column1}')
        st.plotly_chart(fig)
    else:
        fig = px.histogram(data, x=column1, title=f'Распределение {column1}')
        st.plotly_chart(fig)

    if data[column2].dtype == 'object':
        fig = px.pie(data, names=column2, title=f'Распределение {column2}')
        st.plotly_chart(fig)
    else:
        fig = px.histogram(data, x=column2, title=f'Распределение {column2}')
        st.plotly_chart(fig)

    st.subheader('Выберите алгоритм проверки гипотез')
    test_algorithm = st.selectbox('Выберите алгоритм:',
                                  ['t-тест', 'Критерий Манна-Уитни', 'Тест Хи-квадрат'])
    # , 'Критерий Краскела-Уоллиса',

    if test_algorithm == 't-тест' or test_algorithm == 'Критерий Манна-Уитни':
        if data[column1].dtype == 'object' or data[column2].dtype == 'object':
            result = 'Для выбранного теста данные должны быть числовыми'
        else:
            if test_algorithm == 't-тест':
                result = stats.ttest_ind(data[column1], data[column2])
            else:
                result = stats.mannwhitneyu(data[column1], data[column2])

    # elif test_algorithm == 'Критерий Краскела-Уоллиса':
    #     result = stats.kruskal(data[column1], data[column2])

    elif test_algorithm == 'Тест Хи-квадрат':
        if data[column1].dtype == 'object' and data[column2].dtype == 'object':
            observed_freq = pd.crosstab(data[column1], data[column2])
            chi2, p, dof, expected = stats.chi2_contingency(observed_freq)
            result = {'chi2': chi2, 'p-value': p, 'dof': dof}
        else:
            result = 'Для теста Хи-квадрат обе переменные должны быть категориальными'

    # Отображение результата теста
    st.subheader(f'Результаты теста c помощью {test_algorithm}:')
    st.write(result)
