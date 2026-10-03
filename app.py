import streamlit as st
import pandas as pd
import urllib.request
import io
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="لیگ کلاس",
    page_icon="🏆",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Vazirmatn', sans-serif;
}

.stApp {
    direction: rtl;
}

h1, h2, h3, h4 {
    font-family: 'Vazirmatn', sans-serif;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
">
    <div style="font-size: 45px;">🏆</div>
    <div style="font-size: 34px; font-weight: bold;">
    لیگ دبستان شاهد امام رضا(ع)
    </div>
    <div style="
        font-size: 17px;
        margin-top: 8px;
        opacity: 0.9;
    ">
        رقابت، تلاش و پیشرفت؛ هر آزمون یک قدم جلوتر 🚀
    </div>
</div>
""", unsafe_allow_html=True)

# لینک Google Sheet
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT6_OX4RjsqOMTPwVBYSovjqC8g3q94KQp_iNnPDsd38xEpM2SthQZiTWLTJDFmwlyvqQSOeO4FIvJ4/pub?gid=0&single=true&output=csv"


# دریافت اطلاعات
try:
    data = urllib.request.urlopen(url, timeout=20).read()
    df = pd.read_csv(io.BytesIO(data), encoding="utf-8-sig")
    st.success("✅ اطلاعات Google Sheet با موفقیت دریافت شد.")
    df.columns = df.columns.str.strip()

except Exception as e:
    st.error("❌ دریافت اطلاعات با مشکل مواجه شد.")
    st.write(e)
    st.stop()


# تبدیل سلول‌های خالی به عدد خالی
score_columns = [col for col in df.columns if "آزمون" in col]

for col in score_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# محاسبه امتیاز هر دانش‌آموز
def calculate_points(row):

    total_points = 0
    participation = 0

    previous_academic = None
    previous_tizhooshan = None

    exam_points = {}

    # پیدا کردن آزمون‌ها
    exam_numbers = sorted(
        set(
            int(col.split("آزمون ")[1].split(" ")[0])
            for col in score_columns
        )
    )

    for exam in exam_numbers:

        academic_col = f"آزمون {exam} - درسی"
        tiz_col = f"آزمون {exam} - تیزهوشان"

        academic = row.get(academic_col)
        tizhooshan = row.get(tiz_col)

        points = 0

        # -------------------------
        # مشارکت
        # -------------------------

        if pd.notna(academic) or pd.notna(tizhooshan):
            participation = 1

        # -------------------------
        # امتیاز درسی
        # -------------------------

        if pd.notna(academic):

            # امتیاز سطح نمره
            if academic >= 6500:
                points += 6
            elif academic >= 6000:
                points += 5
            elif academic >= 5500:
                points += 4

            # امتیاز پیشرفت
            if previous_academic is not None:

                improvement = academic - previous_academic

                if improvement >= 200:
                    points += 3
                elif improvement >= 100:
                    points += 2

            previous_academic = academic

        # -------------------------
        # امتیاز تیزهوشان
        # -------------------------

        if pd.notna(tizhooshan):

            # امتیاز سطح نمره
            if tizhooshan >= 6500:
                points += 7
            elif tizhooshan >= 6000:
                points += 6
            elif tizhooshan >= 5500:
                points += 5

            # امتیاز پیشرفت
            if previous_tizhooshan is not None:

                improvement = tizhooshan - previous_tizhooshan

                if improvement >= 200:
                    points += 4
                elif improvement >= 100:
                    points += 3

            previous_tizhooshan = tizhooshan

        # مشارکت فقط یک بار در هر آزمون
        if pd.notna(academic) or pd.notna(tizhooshan):
            points += 1

        exam_points[f"آزمون {exam}"] = points
        total_points += points

    return total_points, exam_points

def calculate_exam_details(row):

    previous_academic = None
    previous_tizhooshan = None

    details = {}

    exam_numbers = sorted(
        set(
            int(col.split("آزمون ")[1].split(" ")[0])
            for col in score_columns
        )
    )

    for exam in exam_numbers:

        academic_col = f"آزمون {exam} - درسی"
        tiz_col = f"آزمون {exam} - تیزهوشان"

        academic = row.get(academic_col)
        tizhooshan = row.get(tiz_col)

        academic_points = 0
        tizhooshan_points = 0
        participation_points = 0

        # امتیاز درسی
        if pd.notna(academic):

            if academic >= 6500:
                academic_points += 6
            elif academic >= 6000:
                academic_points += 5
            elif academic >= 5500:
                academic_points += 4

            if previous_academic is not None:
                improvement = academic - previous_academic

                if improvement >= 200:
                    academic_points += 3
                elif improvement >= 100:
                    academic_points += 2

            previous_academic = academic

        # امتیاز تیزهوشان
        if pd.notna(tizhooshan):

            if tizhooshan >= 6500:
                tizhooshan_points += 7
            elif tizhooshan >= 6000:
                tizhooshan_points += 6
            elif tizhooshan >= 5500:
                tizhooshan_points += 5

            if previous_tizhooshan is not None:
                improvement = tizhooshan - previous_tizhooshan

                if improvement >= 200:
                    tizhooshan_points += 4
                elif improvement >= 100:
                    tizhooshan_points += 3

            previous_tizhooshan = tizhooshan

        # مشارکت فقط یک امتیاز برای کل آزمون
        if pd.notna(academic) or pd.notna(tizhooshan):
            participation_points = 1

        details[f"آزمون {exam}"] = {
            "درسی": academic_points,
            "تیزهوشان": tizhooshan_points,
            "مشارکت": participation_points,
            "جمع": academic_points + tizhooshan_points + participation_points
        }

    return details

# محاسبه برای همه دانش‌آموزان
results = []

for _, row in df.iterrows():

    total, exam_points = calculate_points(row)

    result = {
        "نام": row["نام و نام خانوادگی"],
        "امتیاز کل": total
    }

    for exam, points in exam_points.items():
        result[exam] = points

    results.append(result)


# ساخت جدول نهایی
ranking_df = pd.DataFrame(results)

# مرتب‌سازی بر اساس امتیاز
ranking_df = ranking_df.sort_values(
    by="امتیاز کل",
    ascending=False
).reset_index(drop=True)

# رتبه
ranking_df.insert(
    0,
    "رتبه",
    range(1, len(ranking_df) + 1)
)
def get_title(rank):
    if rank == 1:
        return "👑 فرمانده لیگ"
    elif rank == 2:
        return "🏆 قهرمان بزرگ"
    elif rank == 3:
        return "⭐ ستاره طلایی"
    elif rank == 4:
        return "🧠 نابغه میدان"
    elif rank == 5:
        return "🎯 شکارچی رتبه"
    elif rank <= 10:
        return "🔥 رقبای سرسخت"
    else:
        return "⚔️ در حال رقابت"


ranking_df["عنوان"] = ranking_df["رتبه"].apply(get_title)

# 🏆 سکوی قهرمانی سه نفر اول

st.markdown("""
<style>
.podium-card {
    padding: 22px 10px;
    border-radius: 20px;
    text-align: center;
    min-height: 190px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 15px;
}

.podium-first {
    background: linear-gradient(135deg, #FFD700, #FFF3A3);
}

.podium-second {
    background: linear-gradient(135deg, #C0C0C0, #F2F2F2);
}

.podium-third {
    background: linear-gradient(135deg, #CD7F32, #FFE0B2);
}

.podium-medal {
    font-size: 45px;
}

.podium-name {
    font-size: 22px;
    font-weight: 900;
    margin-top: 8px;
}

.podium-score {
    font-size: 18px;
    font-weight: bold;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.subheader("🏆 قهرمانان لیگ")

if len(ranking_df) >= 3:

    second = ranking_df.iloc[1]
    first = ranking_df.iloc[0]
    third = ranking_df.iloc[2]

    col2, col1, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown(f"""
        <div class="podium-card podium-second">
            <div class="podium-medal">🥈</div>
            <div class="podium-name">{second["نام"]}</div>
            <div class="podium-score">⭐ {second["امتیاز کل"]} امتیاز</div>
            <div>{second["عنوان"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        st.markdown(f"""
        <div class="podium-card podium-first">
            <div class="podium-medal">🥇</div>
            <div class="podium-name">{first["نام"]}</div>
            <div class="podium-score">⭐ {first["امتیاز کل"]} امتیاز</div>
            <div>{first["عنوان"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="podium-card podium-third">
            <div class="podium-medal">🥉</div>
            <div class="podium-name">{third["نام"]}</div>
            <div class="podium-score">⭐ {third["امتیاز کل"]} امتیاز</div>
            <div>{third["عنوان"]}</div>
        </div>
        """, unsafe_allow_html=True)

# نمایش
# آمار کلی لیگ
student_count = len(ranking_df)
top_student = ranking_df.iloc[0]["نام"]
top_score = ranking_df.iloc[0]["امتیاز کل"]

exam_columns = [col for col in ranking_df.columns if col.startswith("آزمون ")]
exam_count = len(exam_columns)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 شرکت‌کنندگان", student_count)

with col2:
    st.metric("👑 نفر اول", top_student)

with col3:
    st.metric("🏆 بالاترین امتیاز", top_score)

with col4:
    st.metric("📝 تعداد آزمون‌ها", exam_count)
    # نمودار ۱۰ نفر برتر
st.subheader("📊 ۱۰ نفر برتر لیگ")

top10 = ranking_df.head(10).copy()

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    top10["نام"],
    top10["امتیاز کل"]
)

ax.set_ylabel("امتیاز کل")
ax.set_xlabel("دانش‌آموز")
ax.set_title("🏆 جدول امتیاز ۱۰ نفر برتر")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)
st.subheader("📈 روند امتیاز دانش‌آموز")

selected_student = st.selectbox(
    "دانش‌آموز را انتخاب کنید:",
    ranking_df["نام"].tolist()
)
selected_data = ranking_df[
    ranking_df["نام"] == selected_student
].iloc[0]

student_rank = selected_data["رتبه"]
student_total = selected_data["امتیاز کل"]
student_title = selected_data["عنوان"]
original_student_data = df[
    df["نام و نام خانوادگی"] == selected_student
].iloc[0]

exam_details = calculate_exam_details(original_student_data)
st.subheader("📋 جزئیات امتیازهای آزمون")

details_rows = []

for exam, values in exam_details.items():
    details_rows.append({
        "آزمون": exam,
        "📚 درسی": values["درسی"],
        "🧠 تیزهوشان": values["تیزهوشان"],
        "👥 مشارکت": values["مشارکت"],
        "⭐ جمع": values["جمع"]
    })

details_df = pd.DataFrame(details_rows)

st.dataframe(
    details_df,
    use_container_width=True,
    hide_index=True
)
profile1, profile2, profile3 = st.columns(3)

with profile1:
    st.metric(
        "🏆 رتبه",
        f"{student_rank}"
    )

with profile2:
    st.metric(
        "⭐ امتیاز کل",
        f"{student_total}"
    )

with profile3:
    st.metric(
        "🎖️ عنوان",
        student_title
    )
student_data = ranking_df[
    ranking_df["نام"] == selected_student
].iloc[0]

exam_names = [
    col for col in ranking_df.columns
    if col.startswith("آزمون ")
]

exam_scores = [
    student_data[col]
    for col in exam_names
]

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    exam_names,
    exam_scores,
    marker="o",
    linewidth=2
)

ax.set_title(f"📈 روند امتیاز {selected_student}")
ax.set_xlabel("آزمون")
ax.set_ylabel("امتیاز لیگ")

plt.tight_layout()

st.pyplot(fig)
st.subheader("🏆 جدول لیگ")

def color_rank(row):
    rank = row["رتبه"]

    if rank == 1:
        return ["background-color: #FFE066; font-weight: bold;"] * len(row)

    elif rank == 2:
        return ["background-color: #A5D8FF; font-weight: bold;"] * len(row)

    elif rank == 3:
        return ["background-color: #FFB3C6; font-weight: bold;"] * len(row)

    elif rank == 4:
        return ["background-color: #D0BFFF; font-weight: bold;"] * len(row)

    elif rank == 5:
        return ["background-color: #B2F2BB; font-weight: bold;"] * len(row)

    elif rank <= 10:
        return ["background-color: #FFD8A8;"] * len(row)

    else:
        return ["background-color: #E7F5FF;"] * len(row)


styled_ranking = ranking_df.style.apply(color_rank, axis=1)

st.dataframe(
    styled_ranking,
    use_container_width=True,
    hide_index=True
)