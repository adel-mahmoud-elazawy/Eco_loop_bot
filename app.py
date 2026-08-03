import streamlit as st
import g4f

# 1. إعداد الواجهة
st.set_page_config(page_title="EcoLoop Bot", page_icon="🌿")
st.title("🌿 EcoLoop Campus - المساعد الذكي")
st.caption("جامعة المنصورة الأهلية - نظام الإدارة الذكي للنفايات")

SYSTEM_PROMPT = """
أنت المساعد الذكي المخصص والحصري لمشروع "EcoLoop Campus" (جامعة المنصورة الأهلية - نظام الإدارة الذكي للنفايات).
تقتصر إجاباتك فقط وحصرياً على:
1. مشروع EcoLoop Campus (الأدوار، النقاط، الخريطة، المتجر، التقنيات).
2. مفاهيم الاستدامة وإعادة التدوير.
أي سؤال خارج هذا النطاق يرجى الرفض بأسلوب مهذب باللغة العربية.
"""

# 2. سجل المحادثات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. استقبال السؤال
if prompt := st.chat_input("اسأل عن مشروع EcoLoop Campus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                # دمج التعليمات والسؤال لضمان عدم وجود أخطاء في الـ Headers
                full_prompt = f"{SYSTEM_PROMPT}\n\nسؤال المستخدم: {prompt}"
                
                # استخدام g4f بشكل مباشر لتفادي مشكلة الـ Unicode Header
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4o,
                    messages=[{"role": "user", "content": full_prompt}]
                )
                
                answer = str(response)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("حدث خطأ مؤقت في الاتصال بالخادم، يرجى المحاولة مرة أخرى.")