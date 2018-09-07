import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import scipy.misc


from matplotlib.patches import Rectangle

def rgb2gray(I):
    return 0.299*I[:,:,0] + 0.587*I[:,:,1] + 0.114*I[:,:,2]


I = plt.imread('mandril.jpg')
#plt.figure(1)        # stworzenie figury
fig,ax = plt.subplots(1)                                # zamiast plt. figure(1)
rect = Rectangle((50,50),50,100,fill=False, ec='r')    # ec - kolor krawedzi

plt.imshow(I)        # dodanie do niej obrazka
plt.title('Mandril') # dodanie tytulu
plt.axis('off')      # wylaczenie wyswietlania ukladu wspolrzednych
x = [ 100, 150, 200, 250]
y = [ 50, 100, 150, 200]
plt.plot(x,y,'r.', markersize=10)
ax.add_patch(rect)               # wyswietlenie

plt.figure(2)
plt.title('Mandril - gray') # dodanie tytulu
plt.gray()
plt.imshow(rgb2gray(I))

plt.figure(3)
plt.title('Mandril - HSV') # dodanie tytulu
plt.hsv()
plt.imshow(plt_colors.rgb_to_hsv(I))

plt.figure(4)
plt.title('Mandril - big')
plt.colors()
plt.imshow(scipy.misc.imresize(I, 0.5))

plt.show()

