#####################################################################################
# SHOWCASE                                                                          #
#####################################################################################

import cv2

VIDEO_NAME    = 'video.mp4'
WINDOW_NAME   = 'showcase'
WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500

#####################################################################################

def detectMovement(original, detector):
	
	#copia imagem original
	frame = original.copy()
	#return frame
	
	#converte tons de cinza
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#return frame
	
	#equaliza histograma
	frame = cv2.equalizeHist(frame)
	#return frame
	
	#pega suaviacao
	blur = cv2.GaussianBlur(frame, (9, 9), 33)
	#return blur
	
	#usa suavizacao para aumentar nitidez
	frame = cv2.addWeighted(frame, 1.5, blur, -0.5, 0);
	#return frame
	
	#pega mascara pelo modo canny
	#mask = cv2.Canny(frame, 30, 200)
	#return mask
		
	#pega mascara pela deteccao de background
	mask = detector.apply(frame)
	#return mask
	
	#aplica treshold na mascara
	_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
	#return mask
	
	#pega contornos na mascara
	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	#desenha todos os contornos em ciano
	#cv2.drawContours(original, contours, -1, (255,255,0), 1)
	#return original
	
	#variaveis para guardar area total dos contornos
	minX, minY, maxX, maxY = 0, 0, 0, 0
	
	#percorre os contornos
	for contour in contours:
		
		#pega area do contorno
		area = cv2.contourArea(contour)
		
		#usa apenas contorno maior que certo tamanho
		if area > 50:
			
			#pega area do contorno
			x, y, w, h = cv2.boundingRect(contour)
			
			#atualiza a area total ocupada pelos contornos
			if minX == 0 or x <= minX:
				minX = x
			if minY == 0 or y <= minY:
				minY = y
			if x + w > maxX:
				maxX = x + w
			if y + h > maxY:
				maxY = y + h
			
			#desenha contorno em magenta
			#cv2.drawContours(original, [contour], -1, (255,0,255), 1)
			
			#desenha area do contorno em azul
			#cv2.rectangle(original, (x, y), (x + w, y + h), (255,0,0), 1)
	
	#desenha area total na regiao de movimento em vermelho
	#cv2.rectangle(original, (minX, minY), (maxX, maxY), (0,0,255), 1)
	
	return minX, minY, maxX - minX, maxY - minY

#####################################################################################

def showcase():
	
	#inicializa captura
	shouldFlip = False
	if(len(VIDEO_NAME) > 0):
		capture = cv2.VideoCapture(VIDEO_NAME)
	else:
		capture = cv2.VideoCapture(0)
		shouldFlip = True
	
	#constroi detector
	detector = cv2.createBackgroundSubtractorMOG2(varThreshold=20)
	
	#constroi tracker
	tracker = cv2.TrackerMIL_create() #forgets overlapped object
	#tracker = cv2.TrackerCSRT_create() #switches overlapped object
	
	#permite escolher uma regiao de tracking qualquer
	#ret, frame = capture.read()
	#if ret == False:
	#	return;
	#box = cv2.selectROI(frame, False)
	#ret = tracker.init(frame, box)
	#if ret == False:
	#	return
	
	isTracking = False
	
	while True:
		
		#captura frame
		ret, frame = capture.read()
		if ret == True:
		
			#flipa se for de webcam
			if shouldFlip == True:
				frame = cv2.flip(frame, 1)
			
			#detecta movimento
			if isTracking == False:
				x, y, w, h = detectMovement(frame, detector)
				area = w * h
				#testa se area detectada eh adequada
				if h > w and area > 10000 and area < 100000:
					#imprime area na imagem em verde
					#cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
					#inicializa tracker
					if tracker.init(frame, (x, y, w, h)) == False:
						break
					isTracking = True
			
			#rastreia area detectada
			if isTracking == True:
				ret, box = tracker.update(frame)
				if ret == True:
					x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
					#cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 1, 1)
			
			#exibe imagem
			cv2.imshow(WINDOW_NAME, frame)
			cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
			cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)
			cv2.moveWindow(WINDOW_NAME, 0, 0)
		
		#sai com a tecla esc
		if cv2.waitKey(12) == 27:
			break
	
	#finaliza
	capture.release()
	cv2.destroyAllWindows()

#####################################################################################

showcase()

#####################################################################################
