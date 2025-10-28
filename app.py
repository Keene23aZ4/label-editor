import streamlit as st
import json
import os
from utils.video_utils import save_temp_video, get_video_info

st.set_page_config(page_title="ラベル編集ツール", layout="wide")
st.title("🎿 スキー動画ラベル編集ツール")

# ラベル保存先ファイル
LABEL_FILE = "label_data.json"

# 動画アップロード
uploaded_file = st.file_uploader("動画をアップロード", type=["mp4"])
if uploaded_file:
    video_path = save_temp_video(uploaded_file)
    frame_count, fps, duration = get_video_info(video_path)
    video_name = uploaded_file.name

    st.video(uploaded_file)
    st.markdown(f"**動画情報**: {frame_count}フレーム / {fps:.2f} fps / {duration:.2f} 秒")

    # 区間指定（秒数ベース）
    st.subheader("📝 ラベル区間の指定")
    col1, col2 = st.columns(2)
    with col1:
        start_sec = st.slider("開始秒", 0.0, duration, 0.0, step=0.1)
    with col2:
        end_sec = st.slider("終了秒", start_sec, duration, start_sec + 1.0, step=0.1)

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    label = st.text_input("ラベル名", value="flat_ski")

    # ラベル保存処理
    if os.path.exists(LABEL_FILE):
        with open(LABEL_FILE, "r") as f:
            label_data = json.load(f)
    else:
        label_data = {}

    if st.button("💾 ラベルを保存"):
        entry = {"start": start_frame, "end": end_frame, "label": label}
        if video_name not in label_data:
            label_data[video_name] = []
        label_data[video_name].append(entry)
        with open(LABEL_FILE, "w") as f:
            json.dump(label_data, f, indent=2)
        st.success(f"ラベルを保存しました: {entry}")

    # 既存ラベル表示
    st.subheader("📋 現在のラベル区間")
    if video_name in label_data:
        for i, entry in enumerate(label_data[video_name]):
            st.write(f"{i+1}. フレーム {entry['start']}〜{entry['end']} : `{entry['label']}`")
