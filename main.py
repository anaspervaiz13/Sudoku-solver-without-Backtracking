
import Sudoku

import pandas as pd

df = pd.read_csv("./sudoku.csv")

input = df.iloc[160548][0]
answer = df.iloc[160548][1]

# input = "004300209005009001070060043006002087190007400050083000600000105003508690042910300"

result = Sudoku.Sudoku(input).solve()

print(input)
print("correct" if result == answer else "incorrect")
print(result)
print(answer)
