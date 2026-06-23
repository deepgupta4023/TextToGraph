EXTRACTION_PROMPT = """
Extract entities and relationships from the text.

Return ONLY valid JSON.

Format:

{{
 "entities":[
  {{"name":"","type":""}}
 ],
 "relations":[
  {{"source":"","target":"","relation":""}}
 ]
}}

Text:
{text}
"""