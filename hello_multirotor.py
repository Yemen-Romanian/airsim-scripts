import airsim
import time
import numpy as np
import cv2
import math

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print("Taking off...")
client.takeoffAsync().join()

# Target trajectory: (x, y, z, velocity)
target_x = 20  # 20 meters North
target_y = 0   # 0 meters East
target_z = -5  # 5 meters altitude (NED coordinate, negative is up)
velocity = 5   # 5 m/s

print(f"Flying to trajectory point: {target_x}, {target_y}, {target_z} at {velocity}m/s")
# Start moving
client.moveToPositionAsync(target_x, target_y, target_z, velocity)

try:
    while True:
        # Check distance to target to know when to stop
        state = client.getMultirotorState()
        pos = state.kinematics_estimated.position
        dist = math.sqrt((pos.x_val - target_x)**2 + (pos.y_val - target_y)**2 + (pos.z_val - target_z)**2)
        
        if dist < 1.0: # If within 1 meter of target
            print("Target reached.")
            break

        # Get camera images from the drone
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        
        if responses:
            response = responses[0]
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            
            if img1d.size == response.height * response.width * 3:
                img_rgb = img1d.reshape(response.height, response.width, 3)
                cv2.imshow("Drone Camera - Front Center", img_rgb)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(0.01)

except KeyboardInterrupt:
    print("User interrupted.")

print("Landing...")
client.landAsync().join()

print("Disarming...")
client.armDisarm(False)
client.enableApiControl(False)

cv2.destroyAllWindows()
print("Done.")

