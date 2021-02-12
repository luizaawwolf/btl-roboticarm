import random 

## THIS DOESN'T TAKE INTO ACCOUNT A FULL RANGE OF POSSIBLE VALUES
coeffs_elbow_g140 = [ 2.26881720e-02, -8.59107527e+00,  9.45229032e+02]
coeffs_elbow_l40 = [-3.72727273e-02  ,5.69090909e-01,  6.02181818e+01]

def elbow_angle(shoulder_angle):
    maximum_elbow_theta = 180 
    minimum_elbow_theta = 0
    if shoulder_angle >= 140:
        maximum_elbow_theta = coeffs_elbow_g140[0]*(x**2) + coeffs_elbow_g140[1]*x + coeffs_elbow_g140[2] 
        minimum_elbow_theta = 0 #find relationship
    elif shoulder_angle <= 40:
        maximum_elbow_theta = 180 
        minimum_elbow_theta = coeffs_elbow_l40[0]*(x**2) + coeffs_elbow_l40[1]*x + coeffs_elbow_l40[2] #find relationship
    return random.randint(minimum_elbow_theta, int(maximum_elbow_theta))

def wrist_angle(shoulder_angle, elbow_angle):
    maximum_wrist_theta = 180 #find relationship
    minimum_wrist_theta = 0 #find relationship
    return random.randint(minimum_wrist_theta, maximum_wrist_theta)

def random_arm_position():
    theta_shoulder = random.randint(0,180) #alternatively, this could be (50, 140), the other values can be any random from (0, 180) and it shouldn't hit
    theta_elbow = elbow_angle(theta_shoulder)
    theta_wrist = wrist_angle(theta_shoulder, theta_elbow)
    return [theta_shoulder, theta_elbow, theta_wrist]

for x in range(10):
    print(random_arm_position())