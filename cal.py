
import subprocess
import os
import time

import streamlit as st

st.set_page_config(layout="centered")

st.title('간단한 Streamlit 계산기')
st.write('환영합니다! 아래에서 계산기 기능을 사용해 보세요.')

st.header("계산하기")

operation = st.radio(
    "원하는 연산을 선택하세요:",
    ('더하기 (+)', '빼기 (-)', '곱하기 (*)', '나누기 (/)', '수식 직접 입력')
)

result = None
calculation_str = ""

if operation == '수식 직접 입력':
    expression_str = st.text_input("수식을 입력하세요 (예: (10+20)*3):")
    if st.button("계산"):
        if expression_str:
            try:
                # Security warning: eval() can be dangerous if input is untrusted.
                # For a simple calculator where user input is controlled/understood, it's fine.
                result = eval(expression_str)
                calculation_str = f"{expression_str} = {result}"
                st.success(f"결과: {calculation_str}")
            except (SyntaxError, TypeError, NameError, ZeroDivisionError, ValueError) as e:
                st.error(f"오류: 잘못된 수식입니다. {e}")
            except Exception as e:
                st.error(f"오류: 알 수 없는 오류가 발생했습니다. {e}")
        else:
            st.warning("수식을 입력해주세요.")
else:
    col1, col2 = st.columns(2)
    with col1:
        num1_str = st.text_input("첫 번째 숫자를 입력하세요:", key="num1")
    with col2:
        num2_str = st.text_input("두 번째 숫자를 입력하세요:", key="num2")

    if st.button("계산", key="calculate_button"):
        if num1_str and num2_str:
            try:
                num1 = float(num1_str)
                num2 = float(num2_str)

                if operation == '더하기 (+)':
                    result = num1 + num2
                    calculation_str = f"{num1} + {num2} = {result}"
                elif operation == '빼기 (-)':
                    result = num1 - num2
                    calculation_str = f"{num1} - {num2} = {result}"
                elif operation == '곱하기 (*)':
                    result = num1 * num2
                    calculation_str = f"{num1} * {num2} = {result}"
                elif operation == '나누기 (/)':
                    if num2 == 0:
                        st.error("오류: 0으로 나눌 수 없습니다!")
                        calculation_str = "오류: 0으로 나눌 수 없습니다!"
                    else:
                        result = num1 / num2
                        calculation_str = f"{num1} / {num2} = {result}"
                
                if result is not None and "오류" not in calculation_str:
                    st.success(f"결과: {calculation_str}")
                    # Log to calculation_log.txt as per original code's functionality
                    try:
                        with open('calculation_log.txt', 'a', encoding='utf-8') as f:
                            f.write(calculation_str + '\\n') # Corrected: double-escape \n
                        st.info("계산 결과가 'calculation_log.txt'에 저장되었습니다.")
                    except Exception as log_e:
                        st.warning(f"로그 파일 저장 중 오류 발생: {log_e}")
                
            except ValueError:
                st.error("오류: 유효한 숫자를 입력해주세요.")
            except Exception as e:
                st.error(f"오류: 알 수 없는 오류가 발생했습니다. {e}")
        else:
            st.warning("두 숫자를 모두 입력해주세요.")

