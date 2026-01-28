import airsim
import time
import numpy as np
import cv2

# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

while True:
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

    # set the controls for car
    car_controls.throttle = 1
    car_controls.steering = 1
    client.setCarControls(car_controls)

    # let car drive a bit
    time.sleep(1)
    
    # # get camera images from the car
    # 0 - front_center
    # 1 - front_right
    # 2 - front_left
    # 3 - fpv
    # 4 - back_center
    responses = client.simGetImages([
        airsim.ImageRequest(0, airsim.ImageType.Scene, False, False)])
    response = responses[0]
    print('Retrieved images: %d', len(responses))
    
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    cv2.imshow("AirSim", img_rgb)
    cv2.waitKey(25)

cv2.destroyAllWindows()
