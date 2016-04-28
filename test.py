import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

mypdf = PdfPages('pdfTest.pdf')
for j in range(0, 3):
    mypdf.attach_note(str(j), positionRect=[0, 0, 100, 100])
    for i in range(1, 7):
        plt.subplot(3, 2, i)
        plt.plot(range(i))
    mypdf.savefig()
    plt.close()
mypdf.close()
plt.close()

