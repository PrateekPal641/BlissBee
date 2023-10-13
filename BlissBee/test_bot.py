with open('plan1.txt', 'r') as f:
  content = f.read()

paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

# Rejoin the paragraphs to remove extra empty lines
cleaned_text = '\n'.join(paragraphs)

print(cleaned_text)