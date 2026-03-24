"""
石垣島 社会シミュレーション
claude CLIを使ってAPIキー不要で動作
"""

import subprocess
import sys
from dataclasses import dataclass, field


# ============================================================
# Claude CLI 呼び出し
# ============================================================

def ask_claude(prompt: str, max_words: int = 150) -> str:
    """claude CLIを使ってレスポンスを取得"""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        return f"[エラー: {result.stderr.strip()}]"
    return result.stdout.strip()


# ============================================================
# データ定義
# ============================================================

@dataclass
class Memory:
    events: list[str] = field(default_factory=list)
    interactions: list[str] = field(default_factory=list)

    def add_event(self, event: str):
        self.events.append(event)

    def add_interaction(self, interaction: str):
        self.interactions.append(interaction)

    def summary(self) -> str:
        parts = []
        if self.events:
            parts.append("【今日の出来事】\n" + "\n".join(f"  - {e}" for e in self.events))
        if self.interactions:
            parts.append("【会話の記憶】\n" + "\n".join(f"  - {i}" for i in self.interactions))
        return "\n".join(parts) if parts else "  （まだ何も起きていない）"


@dataclass
class Agent:
    name: str
    age: int
    job: str
    personality: str
    goal: str
    location: str
    memory: Memory = field(default_factory=Memory)

    def persona_text(self) -> str:
        return (
            f"名前: {self.name}（{self.age}歳）\n"
            f"職業: {self.job}\n"
            f"性格: {self.personality}\n"
            f"今日の目標: {self.goal}\n"
            f"現在地: {self.location}"
        )

    def decide_action(self, time_slot: str, world_state: str) -> str:
        prompt = f"""あなたは石垣島にいる一人の人間です。以下のペルソナで行動してください。

{self.persona_text()}

{self.memory.summary()}

【現在の状況】
{world_state}

この時間帯（{time_slot}）に何をするか、1〜3文で具体的に描写してください。
思考・感情・行動を含め、リアルな人物として書いてください。余計な説明は不要です。"""

        action = ask_claude(prompt)
        self.memory.add_event(f"{time_slot}: {action}")
        return action

    def interact_with(self, other: "Agent", context: str) -> str:
        prompt = f"""石垣島で2人が出会い、短い会話をします。

【{self.name}のプロフィール】
{self.persona_text()}

【{other.name}のプロフィール】
{other.persona_text()}

【出会いの状況】
{context}

2人の自然な会話を書いてください。各自2〜3セリフ程度。
形式:
{self.name}:「...」
{other.name}:「...」
（続けてOK）

余計な説明は不要です。会話だけ書いてください。"""

        dialogue = ask_claude(prompt)
        self.memory.add_interaction(f"{other.name}と会話（{context}）")
        other.memory.add_interaction(f"{self.name}と会話（{context}）")
        return dialogue


# ============================================================
# 世界の状態
# ============================================================

WORLD = {
    "date": "2026年3月23日（月曜日）",
    "weather": "晴れ、気温25℃、南風が心地よい",
    "events": [
        "川平湾でシュノーケルツアー開催中",
        "公設市場は朝8時から営業",
        "夕方は離島ターミナル近くで美しい夕日が見える",
    ],
}

def world_state(time_slot: str) -> str:
    return (
        f"日付: {WORLD['date']}\n"
        f"天気: {WORLD['weather']}\n"
        f"島の情報: {' / '.join(WORLD['events'])}\n"
        f"時間帯: {time_slot}"
    )


# ============================================================
# メイン実行
# ============================================================

def print_header(text: str, char: str = "=", width: int = 60):
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}")

def print_section(text: str, width: int = 60):
    print(f"\n{'─' * width}")
    print(f"⏰ {text}")
    print(f"{'─' * width}")


def run():
    print_header("石垣島 社会シミュレーション", "=")
    print(f"  日付: {WORLD['date']}")
    print(f"  天気: {WORLD['weather']}")

    # ── 3人のペルソナ ──────────────────────────────────────
    agents = [
        Agent(
            name="田中健一",
            age=52,
            job="漁師（石垣島生まれ）",
            personality="口数は少なく実直。海を愛し、観光地化が進む島の変化に複雑な思いを抱く。地元コミュニティを大切にしている",
            goal="早朝漁を終えて港で魚を売り、夕方は孫と過ごす",
            location="石垣漁港",
        ),
        Agent(
            name="鈴木美咲",
            age=27,
            job="東京のIT企業勤務（3泊4日の一人旅）",
            personality="SNS好きでアクティブ。インスタ映えも意識するが、本物の体験や地元の人との交流を求めている",
            goal="川平湾でシュノーケル体験と地元グルメの開拓",
            location="市内のホテル",
        ),
        Agent(
            name="山田拓海",
            age=34,
            job="3年前に東京から移住、ゲストハウス経営",
            personality="自由を求めて移住したが経営は苦しい。島の人間関係を大切にしており、観光客と地元民の橋渡し役を自任",
            goal="宿の清掃・運営をこなしつつ、夜は居酒屋で地元情報を仕入れる",
            location="自分のゲストハウス（登野城地区）",
        ),
    ]

    agent_map = {a.name: a for a in agents}

    # ── 時間帯とインタラクション定義 ─────────────────────────
    schedule = [
        {
            "time": "早朝 6:00〜8:00",
            "interaction": None,
        },
        {
            "time": "午前 9:00〜12:00",
            "interaction": None,
        },
        {
            "time": "昼 12:00〜14:00",
            "interaction": {
                "a": "田中健一",
                "b": "鈴木美咲",
                "context": "港の食堂で偶然隣の席になった。鈴木は地元の魚料理を食べていて、田中に「この魚は何ですか？」と聞いた",
            },
        },
        {
            "time": "午後 14:00〜17:00",
            "interaction": None,
        },
        {
            "time": "夕方 17:00〜19:00",
            "interaction": {
                "a": "鈴木美咲",
                "b": "山田拓海",
                "context": "川平湾からの帰り道、山田のゲストハウスの看板が目に入り、鈴木が明日の宿として興味を持って立ち寄った",
            },
        },
        {
            "time": "夜 19:00〜21:00",
            "interaction": {
                "a": "田中健一",
                "b": "山田拓海",
                "context": "行きつけの居酒屋「珊瑚」で偶然同席になった。最近の島の変化について話が盛り上がった",
            },
        },
    ]

    # ── シミュレーション実行 ──────────────────────────────────
    for slot in schedule:
        time_slot = slot["time"]
        print_section(time_slot)

        ws = world_state(time_slot)

        # 各エージェントの行動
        for agent in agents:
            print(f"\n👤 {agent.name}（{agent.job}）")
            sys.stdout.flush()
            action = agent.decide_action(time_slot, ws)
            print(f"   {action}")
            sys.stdout.flush()

        # インタラクション
        if slot["interaction"]:
            info = slot["interaction"]
            agent_a = agent_map[info["a"]]
            agent_b = agent_map[info["b"]]
            print(f"\n💬 【会話シーン】{info['a']} × {info['b']}")
            print(f"   状況: {info['context']}")
            sys.stdout.flush()
            dialogue = agent_a.interact_with(agent_b, info["context"])
            for line in dialogue.split("\n"):
                if line.strip():
                    print(f"   {line}")
            sys.stdout.flush()

    # ── 1日の振り返り ─────────────────────────────────────
    print_header("1日の振り返り（各エージェントの記憶）")
    for agent in agents:
        print(f"\n📋 {agent.name}")
        print(agent.memory.summary())

    print_header("シミュレーション完了")


if __name__ == "__main__":
    run()
