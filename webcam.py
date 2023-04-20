import cv2

def show_webcam(mirror=False, width=600, height=600):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()

        #Espelha a imagem
        if mirror: 
            img = cv2.flip(img, 1)

        # Faço o pré processamento da imagem 
        # Blur - Filtro da média
        img_blur = cv2.blur(img, (7, 7))

        # Blur - Filtro da Gaussiano
        img_blur_gauss = cv2.GaussianBlur(img, (7, 7), 1)

        # Unsharpening (nitidez)
        img_out = cv2.addWeighted(img, 1.5, img_blur_gauss, -0.5, 0);

        # Configura o output de imagem borrada
        # cv2.imshow('PDI - Webcam', img_blur)

        # Configura o output de imagem borrada
        cv2.imshow('PDI - Webcam', img_out)

        cv2.namedWindow('PDI - Webcam',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('PDI - Webcam', width, height)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

show_webcam()