import subprocess

prompt = "Tengo hambre dame ideas de cena, soy vegano y celiaco e intolerante a la lactosa"
result = subprocess.run(
    ["ollama", "run", "deepseek-r1:1.5b", prompt],
    capture_output=True,
    text=True
)
print(result.stdout)
    