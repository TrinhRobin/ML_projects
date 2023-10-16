from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    genre:str
    height: int
    publisher :str
    publication_year: int


def damerau_levenshtein_distance(s1, s2):
    """
    Calcule la distance de Damerau-Levenshtein entre deux chaînes de caractères.
    
    Args:
        s1 (str): Première chaîne de caractères.
        s2 (str): Deuxième chaîne de caractères.
        
    Returns:
        int: Distance de Damerau-Levenshtein entre les deux chaînes.
    """
    len_s1, len_s2 = len(s1), len(s2)
    d = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]
    
    for i in range(len_s1 + 1):
        d[i][0] = i
    
    for j in range(len_s2 + 1):
        d[0][j] = j
    
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,  # Deletion
                d[i][j - 1] + 1,  # Insertion
                d[i - 1][j - 1] + cost  # Substitution
            )
            
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)  # Transposition
    
    return d[len_s1][len_s2]