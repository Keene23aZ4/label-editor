import streamlit as st
import json
import os
from utils.video_utils import save_temp_video, get_frame_count

st.title("🎬 スキー動画ラベル編集ツール")

# 動画アップロード
uploaded_file = st.file_uploader("動画をアップロード", type=["mp4"])
if uploaded_file:
    video_path = save_temp_video(uploaded_file)
    frame_count = get_frame_count(video_path)
    st.video(uploaded_file)

    # 区間選択
    st.subheader("📝 ラベル区間の指定")
    start = st.number_input("開始フレーム", min_value=0, max_value=frame_count-1, value=0)
    end = st.number_input("終了フレーム", min_value=start, max_value=frame_count-1, value=min(start+29, frame_count-1))
    label = st.text_input("ラベル名", value="flat_ski")

    # 保存先ファイル
    label_file = "label_data.json"
    if os.path.exists(label_file):
        with open(label_file, "r") as f:
            label_data = json.load(f)
    else:
        label_data = {}

    # 保存ボタン
    if st.button("💾 ラベルを保存"):
        video_name = uploaded_file.name
        if video_name not in label_data:
            label_data[video_name] = []
        label_data[video_name].append({"start": int(start), "end": int(end), "label": label})
        with open(label_file, "w") as f:
            json.dump(label_data, f, indent=2)
        st.success("ラベルを保存しました！")

    # 既存ラベル表示
    st.subheader("📋 現在のラベル区間")
    if video_name in label_data:
        for entry in label_data[video_name]:
            st.write(f"{entry['start']}〜{entry['end']} : {entry['label']}")