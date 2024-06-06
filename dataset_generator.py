from openai import OpenAI
import csv
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMPT_TEMPLATES = {
    "street_1": (
        "Generate 20 random sentences in Turkish expressing the emotion '{emotion}' in a subtle and realistic manner, using colloquial and street language. Each sentence should include exactly three different emotions in descending order of relevance, separated by commas. Only use these emotions: {valid_emotions}. "
        "Avoid using direct expressions that explicitly mention the emotion itself, such as 'kızgın'. Instead, imply the emotions through context, like 'geçen gün beni çok kırdın' or 'geçen gün orada zor durdum'. While it is acceptable to use the emotion word occasionally, it should not be common. "
        "Use informal language, slang, and everyday expressions to make the sentences sound more natural and authentic. "
        "Please do not include any numbering or double quotes at the beginning of the lines. "
        "Format each line exactly like this (without double quotes): "
        "sentence;emotion1,emotion2,emotion3\n"
        "Example:\n"
        "Projeyi inceledim bir eksiklik göremedim.;mutlu,heyecanlı,şaşkın\n"
        "Arkadaşlarla buluşmak beni çok mutlu etti.;mutlu,heyecanlı,neşeli\n"
    )
}

EMOTIONS = [
    "neşeli",
    "kızgın",
    "mutlu",
    "kıskanç",
    "sürpriz",
    "üzgün",
    "heyecanlı",
    "inatçı",
    "şaşkın",
    "korku"
]
TOTAL_BUDGET = 4.00
COST_PER_1K_TOKENS = 0.002  # Maliyet tahmini, güncel fiyatları kontrol edin
TOKENS_PER_CALL = 1500  # 10 cümle için yaklaşık token sayısı
NUM_OF_CALLS = int((TOTAL_BUDGET / COST_PER_1K_TOKENS) / (TOKENS_PER_CALL / 1000) / len(PROMPT_TEMPLATES) / len(EMOTIONS))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

generated_sentences = set()  # Tekrarı önlemek için set kullanıyoruz

def generate_text(emotion, style):
    valid_emotions = ", ".join(EMOTIONS)
    prompt = PROMPT_TEMPLATES[style].format(emotion=emotion, valid_emotions=valid_emotions)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=1,
    max_tokens=TOKENS_PER_CALL)
    return response.choices[0].message.content.strip()

def save_to_csv(data, file_name):
    with open(file_name, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    data = []
    total_calls = 0
    total_cost = 0.0

    try:
        for _ in range(NUM_OF_CALLS):
            for emotion in EMOTIONS:
                for style in PROMPT_TEMPLATES.keys():
                    if total_cost >= TOTAL_BUDGET:
                        print("Bütçe limitine ulaşıldı.")
                        break
                    response = generate_text(emotion, style)
                    lines = response.split("\n")
                    for line in lines:
                        if line and line not in generated_sentences:
                            try:
                                sentence, labels = line.rsplit(";", 1)
                                label_list = labels.split(",")
                                if len(label_list) == 3 and all(label in EMOTIONS for label in label_list):
                                    data.append((sentence.strip(), labels.strip()))
                                    generated_sentences.add(line)
                                    print(f"Generated Sentence: {sentence.strip()};{labels.strip()}")
                            except ValueError:
                                print(f"Skipping line due to invalid format: '{line}'")
                    total_calls += 1
                    total_cost += (TOKENS_PER_CALL / 1000) * COST_PER_1K_TOKENS
                    print(f"Completed API call for emotion '{emotion}' with style '{style}'")
                    print(f"Total Sentences Generated: {len(data)}")
                    print(f"Total Cost: ${total_cost:.2f}")
                    print("=" * 50)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving partial data to the CSV file...")

    finally:
        save_to_csv(data, "testdata.csv")
        print("Data saved to 'testdata.csv'.")
        print(f"\nFinal Total Sentences Generated: {len(data)}")
        print(f"Final Total Cost: ${total_cost:.2f}")
        print("\nSample Sentences:")
        for i in range(min(10, len(data))):
            print(f"{data[i][0]};{data[i][1]}")
