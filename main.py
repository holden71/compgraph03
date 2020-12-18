from PIL import Image, ImageDraw
from tkinter import Tk, PhotoImage, Canvas, NW

#В программе используется датасет DS2

def rotation(A, B, C):
  return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])


def jarvis_algoritm(data):#функция афинного преобразования
    count_points = len(data)
    num_points = list(range(count_points))
    for i in range(1,count_points):
        if data[num_points[i]][0]<data[num_points[0]][0]:
            num_points[i], num_points[0] = num_points[0], num_points[i]
    result = [num_points[0]]
    del num_points[0]
    num_points.append(result[0])


    while True:
        right = 0
        for i in range(1, len(num_points)):
            if rotation(data[result[-1]], data[num_points[right]], data[num_points[i]]) < 0:
                right = i
        if num_points[right] == result[0]:
            break
        else:
            result.append(num_points[right])
            del num_points[right]

            
    return result


def algoritm (txtname, imagename, size = (960,540)): # Создание преобразованного изображения
    img = Image.new("RGB", size, "white")
    f = open(txtname,"r")
    dot_data = f.read().split("\n")
   
    for i in range(len(dot_data)-1):
        dot_data[i] = dot_data[i].split(" ")
        dot_data[i][0]=int(dot_data[i][0])
        dot_data[i][1] = int(dot_data[i][1])
        img.putpixel((int(dot_data[i][1]), 540 - int(dot_data[i][0])), (0, 0, 0))



    dots = jarvis_algoritm(dot_data[:-1])
    draw = ImageDraw.Draw(img)


    for dot in dots:
        draw.line([dot_data[dots[dots.index(dot)-1]][1], 540 - int(dot_data[dots[dots.index(dot)-1]][0]),
                   dot_data[dot][1], 540 - int(dot_data[dot][0])], fill="blue")
    img.save(f"{imagename}.png")



    return size



def main_menu():
    print("Программа афинного преобрезования множества точек.\n")
    dataset_name = input("Введите название датасета. (Пример: dataset.txt)\n> ")
    image_name = input("Введите название нового изображения:\n> ")


    size = algoritm(dataset_name, image_name) #создание картинки и возврат размера
    show_image = input("Хотите просмотреть фотографию? {Y/N}:\n> ") #просмотр результата


    if show_image.lower() == "y": #Отображение созданной картинки
        windowMain = Tk()
        windowMain.geometry(f'{size[0]}x{size[1]}+50+50')
        ph_im = PhotoImage(file=f'{image_name}.png')
        canv = Canvas(windowMain, width=size[0], height=size[1])
        canv.create_image(1, 1, anchor=NW, image=ph_im)
        canv.place(x=10, y=10)
        windowMain.mainloop()


    do_again = input("Хотите продолжить тестирование? {Y/N}:\n> ")
    if do_again.lower() == "y":
        main_menu()
    else:
      print("Тестирование программы успешно завершено!")

main_menu()

