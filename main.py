import streamlit as st
import math

# 웹앱 페이지 설정
st.set_page_config(page_title="공학용 계산기 웹앱", page_icon="🧮", layout="centered")

st.title("🧮 다기능 계산기 웹앱")
st.write("깃허브와 스트림릿을 이용한 연산기능 페이지입니다.")
st.markdown("---")

# 1. 연산 종류 선택
operation = st.selectbox(
    "원하는 연산 기능을 선택하세요:",
    ("사칙연산 (더하기, 빼기, 곱하기, 나누기)", "모듈러 연산 (나머지)", "지수 연산 (Power)", "로그 연산 (Logarithm)")
)

st.markdown("### 연산 입력")

# 2. 선택한 연산에 따른 입력 및 계산 로직
if operation == "사칙연산 (더하기, 빼기, 곱하기, 나누기)":
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("첫 번째 숫자 (X)", value=0.0, format="%f")
    with col2:
        num2 = st.number_input("두 번째 숫자 (Y)", value=0.0, format="%f")
    
    op_type = st.radio("연산자 선택:", ("+", "-", "×", "÷"), horizontal=True)
    
    if st.button("계산하기", key="calc_basic"):
        if op_type == "+":
            result = num1 + num2
            st.success(f"결과: {num1} + {num2} = **{result}**")
        elif op_type == "-":
            result = num1 - num2
            st.success(f"결과: {num1} - {num2} = **{result}**")
        elif op_type == "×":
            result = num1 * num2
            st.success(f"결과: {num1} × {num2} = **{result}**")
        elif op_type == "÷":
            if num2 != 0:
                result = num1 / num2
                st.success(f"결과: {num1} ÷ {num2} = **{result}**")
            else:
                st.error("오류: 0으로 나눌 수 없습니다.")

elif operation == "모듈러 연산 (나머지)":
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("피제수 (나눠지는 수, X)", value=0, step=1)
    with col2:
        num2 = st.number_input("제수 (나누는 수, Y)", value=1, step=1)
        
    if st.button("계산하기", key="calc_mod"):
        if num2 != 0:
            result = num1 % num2
            st.success(f"결과: {num1} % {num2} (나머지) = **{result}**")
        else:
            st.error("오류: 0으로 나눌 수 없습니다.")

elif operation == "지수 연산 (Power)":
    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("밑 (Base, X)", value=2.0, format="%f")
    with col2:
        exponent = st.number_input("지수 (Exponent, Y)", value=3.0, format="%f")
        
    if st.button("계산하기", key="calc_pow"):
        try:
            result = math.pow(base, exponent)
            st.success(f"결과: {base} ^ {exponent} = **{result}**")
        except OverflowError:
            st.error("오류: 계산 결과가 너무 커서 표시할 수 없습니다.")
        except ValueError:
            st.error("오류: 음수의 소수점 거듭제곱은 허용되지 않습니다.")

elif operation == "로그 연산 (Logarithm)":
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("진수 (X)", value=10.0, format="%f")
    with col2:
        log_type = st.selectbox("로그 종류 선택:", ("상용로그 (밑 10)", "자연로그 (밑 e)", "커스텀 밑 선택"))
    
    # 커스텀 밑 선택 시 추가 입력칸 등장
    base = 10.0
    if log_type == "커스텀 밑 선택":
        base = st.number_input("원하는 밑(Base) 입력", value=2.0, min_value=0.0001, format="%f")

    if st.button("계산하기", key="calc_log"):
        if x <= 0:
            st.error("오류: 로그의 진수는 0보다 커야 합니다.")
        elif base <= 0 or base == 1:
            st.error("오류: 로그의 밑은 0보다 크고 1이 아니어야 합니다.")
        else:
            if log_type == "상용로그 (밑 10)":
                result = math.log10(x)
                st.success(f"결과: log10({x}) = **{result}**")
            elif log_type == "자연로그 (밑 e)":
                result = math.log(x)
                st.success(f"결과: ln({x}) = **{result}**")
            else:
                result = math.log(x, base)
                st.success(f"결과: log_{base}({x}) = **{result}**")

st.markdown("---")
st.caption("Streamlit & GitHub을 활용한 오픈소스 계산기 프로젝트")
