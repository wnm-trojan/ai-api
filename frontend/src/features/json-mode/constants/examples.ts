export interface JSONExample {
  label: string;
  prompt: string;
  schema: string;
}

export const JSON_EXAMPLES: JSONExample[] = [
  {
    label: "Entity Extraction",
    prompt:
      "Extract person info from: 'Dr. Sarah Chen, 34, is a neuroscientist at MIT in Cambridge.'",
    schema:
      '{"name": "string", "age": "number", "title": "string", "workplace": "string", "city": "string"}',
  },
  {
    label: "Sentiment Analysis",
    prompt:
      "Analyze sentiment of: 'The product is decent but shipping was incredibly slow and packaging was damaged.'",
    schema:
      '{"overall": "positive|negative|mixed", "score": "0-10", "aspects": [{"name": "string", "sentiment": "string"}]}',
  },
  {
    label: "Recipe Parser",
    prompt:
      "Parse this recipe: 'Pasta Carbonara: 200g spaghetti, 100g pancetta, 2 eggs, 50g parmesan. Cook pasta al dente. Fry pancetta. Mix eggs+cheese. Combine off heat.'",
    schema:
      '{"name": "string", "ingredients": [{"item": "string", "amount": "string"}], "steps": ["string"]}',
  },
];
