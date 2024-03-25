import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.read_csv(sys.argv[1], encoding="utf-8")
print(df)

fig, ax = plt.subplots(figsize=(12, 4))
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans JP']

ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc='center', fontsize=9)

pp = PdfPages("out.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()

plt.show()
