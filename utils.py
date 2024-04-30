def detect_codes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray)
    return [obj.data.decode("utf-8") for obj in decoded_objects]


@router.post("/detect/")
async def detect_codes(file: UploadFile = File(...)):
    contents = await file.read()
    image = cv2.imdecode(np.fromstring(contents, np.uint8), cv2.IMREAD_UNCHANGED)
    codes = detect_codes(image)
    return {"codes": codes}
