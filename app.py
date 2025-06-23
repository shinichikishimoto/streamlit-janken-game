import streamlit as st
import random
from collections import Counter

# --- 初期化 ---
for key, init in [
    ("game_count", 0),
    ("win_count", 0),
    ("lose_count", 0),
    ("draw_count", 0),
    ("boss_mode", False),
    ("boss_finished", False),
    ("history", []),
]:
    if key not in st.session_state:
        st.session_state[key] = init

# --- ボス用予測関数 ---
def predict_next_move(history):
    if not history:
        return random.randint(0, 2)
    most = Counter(history).most_common(1)[0][0]
    win_map = {0: 2, 1: 0, 2: 1}
    return win_map[most]

# --- 10回戦終了チェック（通常モードのみ）＋再スタート ---
if not st.session_state["boss_mode"] and st.session_state["game_count"] >= 10:
    st.write("10回戦が終了しました。")
    st.write(
        f"最終成績 → "
        f"{st.session_state['win_count']}勝 "
        f"{st.session_state['lose_count']}敗 "
        f"{st.session_state['draw_count']}引き分け"
    )
    if st.button("再スタート"):
        st.session_state.update({
            "game_count": 0,
            "win_count": 0,
            "lose_count": 0,
            "draw_count": 0,
            "boss_mode": False,
            "boss_finished": False,
            "history": []
        })
        st.rerun()
    st.stop()

# --- タイトル表示 ---
if st.session_state["boss_mode"]:
    st.title("最終ボス戦：じゃんけんバトル")
else:
    st.title("じゃんけんゲーム")

# --- 通常モード：5勝未満の場合の対戦処理 ---
if not st.session_state["boss_mode"] and st.session_state["win_count"] < 5:
    # プレイヤーの手選択
    player_choice = st.radio("手を選んでください", ["グー", "チョキ", "パー"])
    if st.button("勝負！"):
        # カウント更新
        st.session_state["game_count"] += 1
        st.write(f"{st.session_state['game_count']} 回目の対戦です。")

        # 判定前準備
        choices = ["グー", "チョキ", "パー"]
        player_index = choices.index(player_choice)
        st.session_state["history"].append(player_index)

        # コンピュータの手（通常モード）
        computer_index = random.randint(0, 2)
        st.write(f"あなた：{choices[player_index]}  VS  コンピュータ：{choices[computer_index]}")

        # 勝敗判定
        if player_index == computer_index:
            st.write("引き分け")
            st.session_state["draw_count"] += 1
        elif (player_index == 0 and computer_index == 1) or \
             (player_index == 1 and computer_index == 2) or \
             (player_index == 2 and computer_index == 0):
            st.write("あなたの勝ち")
            st.session_state["win_count"] += 1
        else:
            st.write("コンピュータの勝ち")
            st.session_state["lose_count"] += 1

        # 成績表示
        st.write(
            f"現在の成績 → "
            f"{st.session_state['win_count']}勝 "
            f"{st.session_state['lose_count']}敗 "
            f"{st.session_state['draw_count']}引き分け"
        )

# --- 5勝到達時：ボス戦へ誘導（通常モードのみ） ---
if not st.session_state["boss_mode"] and st.session_state["win_count"] >= 5:
    st.success("最終ボスに挑戦する権利を獲得しました！")
    if st.button("ボス戦に進む", key="to_boss"):
         st.session_state["boss_mode"] = True
         st.rerun()

# --- ボスモード：1回だけ勝負し、その後再スタートのみ ---
if st.session_state["boss_mode"]:
    # ボス戦開始前：まだ勝負していない状態
    if not st.session_state["boss_finished"]:
        # ボス戦用の手選択
        player_choice = st.radio("ボス戦：手を選んでください", ["グー", "チョキ", "パー"])
        if st.button("勝負！", key="boss_battle"):
            choices = ["グー", "チョキ", "パー"]
            player_index = choices.index(player_choice)
            st.session_state["history"].append(player_index)

            # 予測ロジックでボスの手
            computer_index = predict_next_move(st.session_state["history"])
            st.write(f"あなた：{choices[player_index]}  VS  ボス：{choices[computer_index]}")

            # ボス戦の勝敗判定
            if player_index == computer_index:
                st.write("引き分け")
            elif (player_index == 0 and computer_index == 1) or \
                 (player_index == 1 and computer_index == 2) or \
                 (player_index == 2 and computer_index == 0):
                st.write("あなたの勝ち！ボスを倒しました！")
            else:
                st.write("あなたは負けました…")

            # ボス戦終了フラグ
            st.session_state["boss_finished"] = True

    # ボス戦終了後：再スタートのみ表示streamlit run app.py

    else:
        if st.button("再スタート"):
            st.session_state.update({
                "game_count": 0,
                "win_count": 0,
                "lose_count": 0,
                "draw_count": 0,
                "boss_mode": False,
                "boss_finished": False,
                "history": []
            })
            st.rerun()
