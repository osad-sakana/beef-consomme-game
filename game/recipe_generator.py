import openai
import os
from dotenv import load_dotenv
# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAIクライアントの初期化
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class RecipeGenerator:
    @staticmethod
    def generate_recipe(ingredients_count):
        try:
            # 食材の種類ごとのカウントを取得
            ingredient_counts = {
                'meat': 0,
                'cheese': 0,
                'fish': 0,
                'vegetable': 0,
                'fruit': 0,
                'herb': 0,
                'spice': 0,
                'soup': 0,
                'chocolate': 0,
                'ice': 0,
                'sugar': 0,
                'milk': 0
            }

            # 食材のカウントを更新
            for ingredient_type, count in ingredients_count.items():
                if ingredient_type in ingredient_counts:
                    ingredient_counts[ingredient_type] = count

            prompt = f"""
            返答は全て日本語で行ってください。
            あなたは料理の審査を行う審査員です。
            以下の食材を全て一つの鍋に入れて一つの料理を作ります。
            素材は偏りがある場合やマッチしない食材がある場合がありますが、それも加味して厳密に考えてください。
            不味そうな料理が完成した場合には不味そうな料理名と不味そうな説明を追加してください。もちろん美味しそうな料理の場合は美味しそうな料理名と美味しそうな説明を追加してください。

            食材の内訳:
            ビーフコンソメ: 適量
            肉: {ingredient_counts['meat']}個
            チーズ: {ingredient_counts['cheese']}個
            魚: {ingredient_counts['fish']}個
            野菜: {ingredient_counts['vegetable']}個
            果物: {ingredient_counts['fruit']}個
            ハーブ: {ingredient_counts['herb']}個
            スパイス: {ingredient_counts['spice']}個
            スープ: {ingredient_counts['soup']}個
            チョコ: {ingredient_counts['chocolate']}個
            氷: {ingredient_counts['ice']}個
            砂糖: {ingredient_counts['sugar']}個
            牛乳: {ingredient_counts['milk']}個

            以下の形式で1つだけ作成してください。
            料理名: <料理名>
            説明: <料理の説明>
            美味しさ: <美味しさの評価(星の個数 5が最大)>
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは料理の専門家です。"},
                    {"role": "user", "content": prompt}
                ]
            )

            # レシピを整形（20文字で改行）
            def wrap_text(text, width=35):
                result = []
                for i in range(0, len(text), width):
                    result.append(text[i:i + width])
                return '\n'.join(result)

            recipe = response.choices[0].message.content
            return wrap_text(recipe)

        except Exception as e:
            print(f"レシピ生成エラー: {e}")
            return "レシピの生成に失敗しました。"
