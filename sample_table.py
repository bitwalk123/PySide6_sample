import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'B': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'C': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
})

plt.rcParams['font.family'] = plt.rcParams["font.monospace"][0]
fig, ax = plt.subplots(1, 1)
ax.table(
    cellText=df.values,
    colLabels=df.columns,
    rowLabels=df.index,
    loc='center'
)
ax.axis('tight')
ax.axis('off')

pp = PdfPages('out.pdf')
pp.savefig(fig, bbox_inches='tight')
pp.close()

plt.show()
